"""Service contract for immutable context revisions and merge jobs.

Content written on a revision cannot be replaced. Status transitions and the
single active pointer are the only later changes. A discarded job keeps its
audit record and never gains a revision.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

JOB_STATUSES = frozenset(
    {"queued", "running", "cancelling", "cancelled", "failed", "discarded"}
)
REVISION_STATUSES = frozenset({"draft", "active", "superseded"})
TERMINAL_JOB_STATUSES = frozenset(
    {"cancelled", "failed", "discarded"}
)


class RevisionContractError(ValueError):
    """Raised when a job or revision change breaks the persistence contract."""


@dataclass(frozen=True)
class HoldRecord:
    hold_id: str
    code: str
    detail: str


@dataclass(frozen=True)
class MergeJobRecord:
    job_id: str
    project_id: str
    status: str
    parent_revision_id: str | None
    rule_release_id: str
    source_hash: str
    normalizer_version: str
    discard_reason: str | None = None
    revision_id: str | None = None


@dataclass(frozen=True)
class RevisionRecord:
    revision_id: str
    project_id: str
    status: str
    parent_revision_id: str | None
    source_hash: str
    rule_release_id: str
    created_at: str
    holds: tuple[HoldRecord, ...] = ()
    corrective_of: str | None = None


@dataclass(frozen=True)
class ContextView:
    project_id: str
    legacy_project_context_id: str | None
    active_revision_id: str | None
    revisions: tuple[RevisionRecord, ...]
    jobs: tuple[MergeJobRecord, ...]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RevisionStore:
    """In-memory CRUD stand-in for the TypeDB context history types."""

    def __init__(self) -> None:
        self._jobs: dict[str, MergeJobRecord] = {}
        self._revisions: dict[str, RevisionRecord] = {}
        self._active: dict[str, str] = {}
        self._legacy: dict[str, str] = {}

    def register_legacy_context(self, project_id: str, project_context_id: str) -> None:
        self._legacy[project_id] = project_context_id

    def create_job(
        self,
        *,
        job_id: str,
        project_id: str,
        parent_revision_id: str | None,
        rule_release_id: str,
        source_hash: str,
        normalizer_version: str,
    ) -> MergeJobRecord:
        if job_id in self._jobs:
            raise RevisionContractError(f"job already exists: {job_id}")
        if parent_revision_id and parent_revision_id not in self._revisions:
            raise RevisionContractError("parent revision does not exist")
        job = MergeJobRecord(
            job_id=job_id,
            project_id=project_id,
            status="queued",
            parent_revision_id=parent_revision_id,
            rule_release_id=rule_release_id,
            source_hash=source_hash,
            normalizer_version=normalizer_version,
        )
        self._jobs[job_id] = job
        return job

    def transition_job(self, job_id: str, status: str, *, reason: str | None = None) -> MergeJobRecord:
        job = self._require_job(job_id)
        if status not in JOB_STATUSES or status == "queued":
            raise RevisionContractError(f"invalid job transition: {status}")
        if job.status in TERMINAL_JOB_STATUSES:
            raise RevisionContractError("terminal job cannot change")
        if status == "discarded" and not reason:
            raise RevisionContractError("discarded job requires a reason")
        if status == "discarded" and job.revision_id:
            raise RevisionContractError("a job with a revision cannot be discarded")
        updated = replace(
            job,
            status=status,
            discard_reason=reason if status == "discarded" else job.discard_reason,
        )
        self._jobs[job_id] = updated
        return updated

    def save_revision(
        self,
        *,
        job_id: str,
        revision_id: str,
        holds: tuple[HoldRecord, ...] = (),
        corrective_of: str | None = None,
        created_at: str | None = None,
    ) -> RevisionRecord:
        job = self._require_job(job_id)
        if job.status == "discarded":
            raise RevisionContractError("discarded job cannot create a revision")
        if job.revision_id:
            raise RevisionContractError("job already has an immutable revision")
        if revision_id in self._revisions:
            raise RevisionContractError(f"revision already exists: {revision_id}")
        if corrective_of and corrective_of not in self._revisions:
            raise RevisionContractError("corrective parent does not exist")
        revision = RevisionRecord(
            revision_id=revision_id,
            project_id=job.project_id,
            status="draft",
            parent_revision_id=job.parent_revision_id,
            source_hash=job.source_hash,
            rule_release_id=job.rule_release_id,
            created_at=created_at or _now(),
            holds=holds,
            corrective_of=corrective_of,
        )
        self._revisions[revision_id] = revision
        self._jobs[job_id] = replace(job, revision_id=revision_id, status="running")
        return revision

    def replace_revision_content(self, revision_id: str, **changes: object) -> None:
        """Content replacement is rejected. Status changes use activate."""
        if revision_id not in self._revisions:
            raise RevisionContractError("revision does not exist")
        raise RevisionContractError("revision content is immutable")

    def activate(self, revision_id: str) -> RevisionRecord:
        revision = self._require_revision(revision_id)
        if revision.holds:
            raise RevisionContractError("a held revision stays a non-current draft")
        current_id = self._active.get(revision.project_id)
        if current_id and current_id != revision_id:
            current = self._revisions[current_id]
            self._revisions[current_id] = replace(current, status="superseded")
        activated = replace(revision, status="active")
        self._revisions[revision_id] = activated
        self._active[revision.project_id] = revision_id
        return activated

    def rollback(self, project_id: str, revision_id: str) -> RevisionRecord:
        target = self._require_revision(revision_id)
        if target.project_id != project_id:
            raise RevisionContractError("revision belongs to another project")
        if target.holds:
            raise RevisionContractError("held draft cannot become the active pointer")
        return self.activate(revision_id)

    def context_view(self, project_id: str) -> ContextView:
        revisions = tuple(
            item for item in self._revisions.values() if item.project_id == project_id
        )
        jobs = tuple(item for item in self._jobs.values() if item.project_id == project_id)
        return ContextView(
            project_id=project_id,
            legacy_project_context_id=self._legacy.get(project_id),
            active_revision_id=self._active.get(project_id),
            revisions=revisions,
            jobs=jobs,
        )

    def _require_job(self, job_id: str) -> MergeJobRecord:
        try:
            return self._jobs[job_id]
        except KeyError as exc:
            raise RevisionContractError(f"unknown job: {job_id}") from exc

    def _require_revision(self, revision_id: str) -> RevisionRecord:
        try:
            return self._revisions[revision_id]
        except KeyError as exc:
            raise RevisionContractError(f"unknown revision: {revision_id}") from exc
