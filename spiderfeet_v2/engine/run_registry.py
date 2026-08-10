"""In-memory async workflow run registry (SPEC-015 R15-01).

Background runs use a dedicated thread pool and each job creates its own
``CrudStore`` via ``store_factory`` (default: TypeDB connect). Tests inject
a factory that returns the FakeCrudStore.
"""

from __future__ import annotations

import threading
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from spiderfeet_v2.db.config import load_connection_config
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.engine import OrchestratorError, run_single_step, run_workflow

StoreFactory = Callable[[], Any]

STATE_QUEUED = "queued"
STATE_RUNNING = "running"
STATE_SUCCESS = "success"
STATE_ERROR = "error"
STATE_CANCELLED = "cancelled"

_TERMINAL = frozenset({STATE_SUCCESS, STATE_ERROR, STATE_CANCELLED})


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_store_factory() -> CrudStore:
    return CrudStore.connect(load_connection_config())


@dataclass
class RunRecord:
    run_id: str
    workflow_id: str
    project_id: Optional[str] = None
    kind: str = "workflow"  # workflow | step
    step_id: Optional[str] = None
    state: str = STATE_QUEUED
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error: Optional[str] = None
    cancel_flag: bool = False
    result: Optional[Dict[str, Any]] = None
    dry_run: bool = False
    temporary_subgraph_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "project_id": self.project_id,
            "kind": self.kind,
            "step_id": self.step_id,
            "state": self.state,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "error": self.error,
            "dry_run": self.dry_run,
            "temporary_subgraph_id": self.temporary_subgraph_id,
            "result": self.result,
        }


@dataclass
class RunRegistry:
    """Thread-safe registry + executor for background workflow/step runs."""

    max_workers: int = 2
    store_factory: StoreFactory = field(default=_default_store_factory)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False, repr=False)
    _runs: Dict[str, RunRecord] = field(default_factory=dict, init=False, repr=False)
    _by_workflow: Dict[str, List[str]] = field(default_factory=dict, init=False, repr=False)
    _executor: ThreadPoolExecutor = field(init=False, repr=False)
    _futures: Dict[str, Future] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self._executor = ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="sf-workflow-run",
        )

    def set_store_factory(self, factory: Optional[StoreFactory]) -> None:
        with self._lock:
            self.store_factory = factory or _default_store_factory

    def get(self, run_id: str) -> Optional[RunRecord]:
        with self._lock:
            rec = self._runs.get(run_id)
            return rec

    def latest_for_workflow(self, workflow_id: str) -> Optional[RunRecord]:
        with self._lock:
            ids = self._by_workflow.get(workflow_id) or []
            if not ids:
                return None
            return self._runs.get(ids[-1])

    def active_for_workflow(self, workflow_id: str) -> Optional[RunRecord]:
        with self._lock:
            ids = self._by_workflow.get(workflow_id) or []
            for rid in reversed(ids):
                rec = self._runs.get(rid)
                if rec and rec.state in (STATE_QUEUED, STATE_RUNNING):
                    return rec
            return None

    def request_cancel(self, run_id: str) -> bool:
        with self._lock:
            rec = self._runs.get(run_id)
            if rec is None:
                return False
            if rec.state in _TERMINAL:
                return False
            rec.cancel_flag = True
            return True

    def cancel_workflow(self, workflow_id: str) -> Optional[str]:
        """Cancel the active run for a workflow. Returns run_id if cancelled."""
        with self._lock:
            rec = None
            ids = self._by_workflow.get(workflow_id) or []
            for rid in reversed(ids):
                candidate = self._runs.get(rid)
                if candidate and candidate.state in (STATE_QUEUED, STATE_RUNNING):
                    rec = candidate
                    break
            if rec is None:
                return None
            rec.cancel_flag = True
            return rec.run_id

    def is_cancelled(self, run_id: str) -> bool:
        with self._lock:
            rec = self._runs.get(run_id)
            return bool(rec and rec.cancel_flag)

    def submit_workflow(
        self,
        *,
        workflow_id: str,
        project_id: Optional[str] = None,
        dry_run: bool = False,
        temporary_subgraph_id: Optional[str] = None,
    ) -> RunRecord:
        run_id = f"run--{uuid.uuid4()}"
        rec = RunRecord(
            run_id=run_id,
            workflow_id=workflow_id,
            project_id=project_id,
            kind="workflow",
            dry_run=dry_run,
            temporary_subgraph_id=temporary_subgraph_id,
        )
        with self._lock:
            self._runs[run_id] = rec
            self._by_workflow.setdefault(workflow_id, []).append(run_id)
            fut = self._executor.submit(self._run_workflow_job, run_id)
            self._futures[run_id] = fut
        return rec

    def submit_step(
        self,
        *,
        workflow_id: str,
        step_id: str,
        project_id: Optional[str] = None,
        dry_run: bool = False,
        temporary_subgraph_id: Optional[str] = None,
    ) -> RunRecord:
        run_id = f"run--{uuid.uuid4()}"
        rec = RunRecord(
            run_id=run_id,
            workflow_id=workflow_id,
            project_id=project_id,
            kind="step",
            step_id=step_id,
            dry_run=dry_run,
            temporary_subgraph_id=temporary_subgraph_id,
        )
        with self._lock:
            self._runs[run_id] = rec
            self._by_workflow.setdefault(workflow_id, []).append(run_id)
            fut = self._executor.submit(self._run_step_job, run_id)
            self._futures[run_id] = fut
        return rec

    def _mark_running(self, run_id: str) -> Optional[RunRecord]:
        with self._lock:
            rec = self._runs.get(run_id)
            if rec is None:
                return None
            if rec.cancel_flag:
                rec.state = STATE_CANCELLED
                rec.finished_at = _utc_now()
                rec.error = "cancelled before start"
                return None
            rec.state = STATE_RUNNING
            rec.started_at = _utc_now()
            return rec

    def _finish(
        self,
        run_id: str,
        *,
        state: str,
        error: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._lock:
            rec = self._runs.get(run_id)
            if rec is None:
                return
            if rec.cancel_flag and state != STATE_CANCELLED:
                # Prefer cancelled when the flag was set mid-run.
                if state == STATE_SUCCESS:
                    state = STATE_CANCELLED
                    error = error or "cancelled"
            rec.state = state
            rec.error = error
            rec.result = result
            rec.finished_at = _utc_now()

    def _run_workflow_job(self, run_id: str) -> None:
        rec = self._mark_running(run_id)
        if rec is None:
            return
        store = None
        try:
            store = self.store_factory()
            if self.is_cancelled(run_id):
                self._finish(run_id, state=STATE_CANCELLED, error="cancelled")
                return
            result = run_workflow(
                store,
                workflow_id=rec.workflow_id,
                project_id=rec.project_id,
                dry_run=rec.dry_run,
                existing_temporary_subgraph_id=rec.temporary_subgraph_id,
                stop_on_error=False,
                should_cancel=lambda: self.is_cancelled(run_id),
            )
            api = result.to_api_dict()
            if result.status == "CANCELLED" or self.is_cancelled(run_id):
                self._finish(
                    run_id,
                    state=STATE_CANCELLED,
                    error="cancelled",
                    result=api,
                )
                return
            if result.status == "ERROR":
                self._finish(
                    run_id,
                    state=STATE_ERROR,
                    error=result.error or result.message,
                    result=api,
                )
            else:
                self._finish(run_id, state=STATE_SUCCESS, result=api)
        except OrchestratorError as exc:
            self._finish(run_id, state=STATE_ERROR, error=str(exc))
        except Exception as exc:  # noqa: BLE001 — background boundary
            self._finish(run_id, state=STATE_ERROR, error=str(exc))

    def _run_step_job(self, run_id: str) -> None:
        rec = self._mark_running(run_id)
        if rec is None:
            return
        try:
            store = self.store_factory()
            if self.is_cancelled(run_id):
                self._finish(run_id, state=STATE_CANCELLED, error="cancelled")
                return
            result = run_single_step(
                store,
                workflow_id=rec.workflow_id,
                step_id=str(rec.step_id),
                project_id=rec.project_id,
                dry_run=rec.dry_run,
                existing_temporary_subgraph_id=rec.temporary_subgraph_id,
            )
            api = result.to_api_dict()
            if self.is_cancelled(run_id):
                self._finish(
                    run_id,
                    state=STATE_CANCELLED,
                    error="cancelled",
                    result=api,
                )
                return
            if result.status == "ERROR":
                self._finish(
                    run_id,
                    state=STATE_ERROR,
                    error=result.error or result.message,
                    result=api,
                )
            else:
                self._finish(run_id, state=STATE_SUCCESS, result=api)
        except OrchestratorError as exc:
            self._finish(run_id, state=STATE_ERROR, error=str(exc))
        except Exception as exc:  # noqa: BLE001 — background boundary
            self._finish(run_id, state=STATE_ERROR, error=str(exc))

    def wait(self, run_id: str, timeout: Optional[float] = None) -> Optional[RunRecord]:
        """Block until the run finishes (tests / reset guard)."""
        with self._lock:
            fut = self._futures.get(run_id)
        if fut is not None:
            try:
                fut.result(timeout=timeout)
            except Exception:  # noqa: BLE001
                pass
        return self.get(run_id)

    def reset_for_tests(self) -> None:
        """Clear registry state between tests (does not shut down the pool)."""
        with self._lock:
            self._runs.clear()
            self._by_workflow.clear()
            self._futures.clear()


_REGISTRY: Optional[RunRegistry] = None
_REGISTRY_LOCK = threading.Lock()


def get_run_registry() -> RunRegistry:
    global _REGISTRY
    with _REGISTRY_LOCK:
        if _REGISTRY is None:
            _REGISTRY = RunRegistry()
        return _REGISTRY


def set_run_registry(registry: Optional[RunRegistry]) -> None:
    """Test DI: replace or clear the process-wide registry."""
    global _REGISTRY
    with _REGISTRY_LOCK:
        _REGISTRY = registry
