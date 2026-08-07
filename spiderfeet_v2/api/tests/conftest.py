"""Fixtures: in-memory Crud/Projection fakes + TestClient with DI overrides."""

from __future__ import annotations

import copy
import json
from typing import Any, Dict, List, Optional

import pytest
from fastapi.testclient import TestClient

from spiderfeet.api import bootstrap
from spiderfeet.api.app import create_app
from spiderfeet_v2.api import deps
from spiderfeet_v2.db.crud import CrudError


class FakeCrudStore:
    """Minimal in-memory stand-in for CrudStore used by route tests."""

    def __init__(self) -> None:
        self.targets: Dict[str, Dict[str, Any]] = {}
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.scan_steps: Dict[str, Dict[str, Any]] = {}
        self.subgraphs: Dict[str, Dict[str, Any]] = {}  # kind:id → row

    # --- targets ---
    def create_target(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tid = data.get("target_id")
        if not tid:
            raise CrudError("target_id is required")
        if tid in self.targets:
            raise CrudError(f"target already exists: {tid}")
        row = dict(data)
        self.targets[tid] = row
        return copy.deepcopy(row)

    def get_target(self, target_id: str, **_: Any) -> Optional[Dict[str, Any]]:
        row = self.targets.get(target_id)
        return copy.deepcopy(row) if row else None

    def update_target(self, target_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if target_id not in self.targets:
            raise CrudError(f"target not found: {target_id}")
        self.targets[target_id].update(data)
        return copy.deepcopy(self.targets[target_id])

    def delete_target(self, target_id: str) -> bool:
        return self.targets.pop(target_id, None) is not None

    def list_targets(self) -> List[Dict[str, Any]]:
        return [copy.deepcopy(self.targets[k]) for k in sorted(self.targets)]

    # --- workflows ---
    def create_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        wid = data.get("workflow_id")
        if not wid:
            raise CrudError("workflow_id is required")
        if not (
            data.get("target_id")
            or data.get("first_step_id")
            or data.get("prior_step_ids")
            or data.get("next_step_ids")
        ):
            raise CrudError("workflow create requires at least one player")
        if wid in self.workflows:
            raise CrudError(f"workflow already exists: {wid}")
        row = {
            **data,
            "prior_step_ids": list(data.get("prior_step_ids") or []),
            "next_step_ids": list(data.get("next_step_ids") or []),
        }
        self.workflows[wid] = row
        return copy.deepcopy(row)

    def get_workflow(self, workflow_id: str, **_: Any) -> Optional[Dict[str, Any]]:
        row = self.workflows.get(workflow_id)
        return copy.deepcopy(row) if row else None

    def update_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if workflow_id not in self.workflows:
            raise CrudError(f"workflow not found: {workflow_id}")
        self.workflows[workflow_id].update(data)
        return copy.deepcopy(self.workflows[workflow_id])

    def delete_workflow(self, workflow_id: str) -> bool:
        return self.workflows.pop(workflow_id, None) is not None

    def list_workflows(self) -> List[Dict[str, Any]]:
        return [copy.deepcopy(self.workflows[k]) for k in sorted(self.workflows)]

    # --- projects ---
    def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pid = data.get("project_id")
        if not pid:
            raise CrudError("project_id is required")
        wids = list(data.get("workflow_ids") or [])
        if not wids:
            raise CrudError("project create requires at least one workflow_id")
        if pid in self.projects:
            raise CrudError(f"project already exists: {pid}")
        row = {**data, "workflow_ids": wids}
        self.projects[pid] = row
        return copy.deepcopy(row)

    def get_project(self, project_id: str, **_: Any) -> Optional[Dict[str, Any]]:
        row = self.projects.get(project_id)
        return copy.deepcopy(row) if row else None

    def update_project(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if project_id not in self.projects:
            raise CrudError(f"project not found: {project_id}")
        self.projects[project_id].update(data)
        return copy.deepcopy(self.projects[project_id])

    def delete_project(self, project_id: str) -> bool:
        return self.projects.pop(project_id, None) is not None

    def list_projects(self) -> List[Dict[str, Any]]:
        return [copy.deepcopy(self.projects[k]) for k in sorted(self.projects)]

    # --- scan steps ---
    def create_scan_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sid = data.get("scan_instance_id")
        if not sid:
            raise CrudError("scan_instance_id is required")
        if sid in self.scan_steps:
            raise CrudError(f"scan_step already exists: {sid}")
        row = {
            **data,
            "consumed_ids": list(data.get("consumed_ids") or []),
            "produced_ids": list(data.get("produced_ids") or []),
        }
        self.scan_steps[sid] = row
        return copy.deepcopy(row)

    def get_scan_step(self, scan_instance_id: str, **_: Any) -> Optional[Dict[str, Any]]:
        row = self.scan_steps.get(scan_instance_id)
        return copy.deepcopy(row) if row else None

    def update_scan_step(
        self, scan_instance_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        if scan_instance_id not in self.scan_steps:
            raise CrudError(f"scan_step not found: {scan_instance_id}")
        self.scan_steps[scan_instance_id].update(data)
        if "consumed_ids" in data:
            self.scan_steps[scan_instance_id]["consumed_ids"] = list(
                data.get("consumed_ids") or []
            )
        if "produced_ids" in data:
            self.scan_steps[scan_instance_id]["produced_ids"] = list(
                data.get("produced_ids") or []
            )
        return copy.deepcopy(self.scan_steps[scan_instance_id])

    def delete_scan_step(self, scan_instance_id: str) -> bool:
        return self.scan_steps.pop(scan_instance_id, None) is not None

    def list_scan_steps(self) -> List[Dict[str, Any]]:
        return [copy.deepcopy(self.scan_steps[k]) for k in sorted(self.scan_steps)]

    # --- subgraphs ---
    def _sg_key(self, kind: str, sg_id: str) -> str:
        return f"{kind}:{sg_id}"

    def get_subgraph(
        self, kind: str, subgraph_id: str, **_: Any
    ) -> Optional[Dict[str, Any]]:
        row = self.subgraphs.get(self._sg_key(kind, subgraph_id))
        return copy.deepcopy(row) if row else None

    def get_subgraph_dual(
        self, kind: str, subgraph_id: str, **_: Any
    ) -> Dict[str, Any]:
        row = self.get_subgraph(kind, subgraph_id)
        if row is None:
            raise CrudError(f"{kind} not found: {subgraph_id}")
        return row

    def create_subgraph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        kind = data["kind"]
        id_attr = {
            "temporary_subgraph": "temporary_subgraph_id",
            "project_context": "project_context_id",
            "scan_result_graph": "scan_result_id",
        }[kind]
        sg_id = data[id_attr]
        graph = data.get("graph") or {
            "nodes": data.get("nodes") or [],
            "edges": data.get("edges") or [],
        }
        row = {
            "kind": kind,
            id_attr: sg_id,
            "project_id": data.get("project_id"),
            "scan_instance_id": data.get("scan_instance_id"),
            "graph": copy.deepcopy(graph),
            "json_string": json.dumps(graph),
            "nodes": copy.deepcopy(graph.get("nodes") or []),
            "edges": copy.deepcopy(graph.get("edges") or []),
        }
        self.subgraphs[self._sg_key(kind, sg_id)] = row
        return copy.deepcopy(row)

    def update_subgraph(
        self, kind: str, subgraph_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        key = self._sg_key(kind, subgraph_id)
        if key not in self.subgraphs:
            raise CrudError(f"{kind} not found: {subgraph_id}")
        graph = data.get("graph")
        if graph is None and ("nodes" in data or "edges" in data):
            graph = {"nodes": data.get("nodes") or [], "edges": data.get("edges") or []}
        if graph is not None:
            self.subgraphs[key]["graph"] = copy.deepcopy(graph)
            self.subgraphs[key]["nodes"] = copy.deepcopy(graph.get("nodes") or [])
            self.subgraphs[key]["edges"] = copy.deepcopy(graph.get("edges") or [])
            self.subgraphs[key]["json_string"] = json.dumps(graph)
        return copy.deepcopy(self.subgraphs[key])


class FakeProjectionStore:
    def __init__(self, crud: FakeCrudStore) -> None:
        self.crud = crud

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        if project_id not in self.crud.projects:
            return None
        temp_ids = sorted(
            {
                row["temporary_subgraph_id"]
                for key, row in self.crud.subgraphs.items()
                if key.startswith("temporary_subgraph:")
                and row.get("project_id") == project_id
            }
        )
        pc_ids = sorted(
            {
                row["project_context_id"]
                for key, row in self.crud.subgraphs.items()
                if key.startswith("project_context:")
                and row.get("project_id") == project_id
            }
        )
        wids = list(self.crud.projects[project_id].get("workflow_ids") or [])
        targets = []
        for wid in wids:
            wf = self.crud.workflows.get(wid) or {}
            tid = wf.get("target_id")
            if tid and tid not in targets:
                targets.append(tid)
        return {
            "project_id": project_id,
            "workflows": sorted(wids),
            "targets": sorted(targets),
            "project_context": pc_ids,
            "temporary_subgraph": temp_ids,
        }

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        wf = self.crud.workflows.get(workflow_id)
        if wf is None:
            return None
        return {
            "workflow_id": workflow_id,
            "target": wf.get("target_id"),
            "first_step": wf.get("first_step_id"),
            "prior_step": list(wf.get("prior_step_ids") or []),
            "next_step": list(wf.get("next_step_ids") or []),
            "workflow_yaml": wf.get("workflow_yaml"),
        }

    def get_scan_step(self, scan_instance_id: str) -> Optional[Dict[str, Any]]:
        step = self.crud.scan_steps.get(scan_instance_id)
        if step is None:
            return None
        return {
            "scan_instance_id": scan_instance_id,
            "cli_command": step.get("scan_ui_cli_command"),
            "text_form": step.get("scan_ui_text_form"),
            "structured_form": step.get("scan_ui_structured_form"),
            "graph_form": step.get("scan_ui_graph_form"),
            "markdown_narrative_form": step.get("scan_ui_markdown_narrative_form"),
            "consumed": list(step.get("consumed_ids") or []),
            "produced": list(step.get("produced_ids") or []),
            "scan_result_graph": list(step.get("scan_result_graph_ids") or []),
        }


@pytest.fixture
def fake_stores():
    crud = FakeCrudStore()
    proj = FakeProjectionStore(crud)
    deps.set_crud_store(crud)  # type: ignore[arg-type]
    deps.set_projection_store(proj)  # type: ignore[arg-type]
    yield crud, proj
    deps.set_crud_store(None)
    deps.set_projection_store(None)


@pytest.fixture
def client(fake_stores):
    bootstrap._runtime = None
    with TestClient(create_app()) as c:
        yield c
