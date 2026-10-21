"""R20-09 and R20-10 revision schema and service contract."""

from __future__ import annotations

from pathlib import Path

import pytest

from spiderfeet_v2.context.revision_schema import (
    CANONICAL_SCHEMA,
    CONTEXT_ATTRIBUTES,
    CONTEXT_ENTITIES,
    context_schema_delta,
    declared_labels,
)
from spiderfeet_v2.context.revisions import (
    HoldRecord,
    RevisionContractError,
    RevisionStore,
)

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = (ROOT / ".seed" / "spiderfeet_v2_semantic.tql").read_text(encoding="utf-8")
LEGACY_SCHEMA = "define\n\tentity project,\n\t\towns project_id @key;\n"


def test_canonical_schema_declares_context_history_once() -> None:
    labels = declared_labels(SCHEMA)
    assert set(CONTEXT_ENTITIES).issubset(labels)
    assert set(CONTEXT_ATTRIBUTES).issubset(labels)
    assert SCHEMA.count("entity context_revision,") == 1
    assert CANONICAL_SCHEMA.is_file()


def test_schema_delta_is_idempotent() -> None:
    first = context_schema_delta(LEGACY_SCHEMA, SCHEMA)
    assert first is not None
    assert "entity context_merge_job" in first
    assert "attribute context_job_status" in first
    second = context_schema_delta(LEGACY_SCHEMA + "\n" + first, SCHEMA)
    assert second is None
    assert context_schema_delta(SCHEMA, SCHEMA) is None


def test_legacy_project_has_no_revision_and_keeps_context_id() -> None:
    store = RevisionStore()
    store.register_legacy_context("project--1", "project-context--legacy")
    view = store.context_view("project--1")
    assert view.active_revision_id is None
    assert view.revisions == ()
    assert view.legacy_project_context_id == "project-context--legacy"


def test_one_active_pointer_and_immutable_content() -> None:
    store = RevisionStore()
    store.create_job(
        job_id="job-1",
        project_id="project--1",
        parent_revision_id=None,
        rule_release_id="release-1",
        source_hash="hash-1",
        normalizer_version="identity-1",
    )
    first = store.save_revision(job_id="job-1", revision_id="rev-1")
    store.activate(first.revision_id)
    store.create_job(
        job_id="job-2",
        project_id="project--1",
        parent_revision_id="rev-1",
        rule_release_id="release-1",
        source_hash="hash-2",
        normalizer_version="identity-1",
    )
    second = store.save_revision(job_id="job-2", revision_id="rev-2")
    store.activate(second.revision_id)
    view = store.context_view("project--1")
    statuses = {item.revision_id: item.status for item in view.revisions}
    assert view.active_revision_id == "rev-2"
    assert statuses == {"rev-1": "superseded", "rev-2": "active"}
    with pytest.raises(RevisionContractError):
        store.replace_revision_content("rev-1", source_hash="changed")
    store.rollback("project--1", "rev-1")
    restored = store.context_view("project--1")
    assert restored.active_revision_id == "rev-1"
    rolled = next(item for item in restored.revisions if item.revision_id == "rev-1")
    assert rolled.source_hash == "hash-1"
    assert rolled.status == "active"


def test_discarded_job_has_no_revision_and_hold_stays_draft() -> None:
    store = RevisionStore()
    store.create_job(
        job_id="job-stale",
        project_id="project--1",
        parent_revision_id=None,
        rule_release_id="release-1",
        source_hash="hash-stale",
        normalizer_version="identity-1",
    )
    discarded = store.transition_job("job-stale", "discarded", reason="parent context advanced")
    assert discarded.revision_id is None
    with pytest.raises(RevisionContractError):
        store.save_revision(job_id="job-stale", revision_id="rev-stale")

    store.create_job(
        job_id="job-hold",
        project_id="project--1",
        parent_revision_id=None,
        rule_release_id="release-1",
        source_hash="hash-hold",
        normalizer_version="identity-1",
    )
    held = store.save_revision(
        job_id="job-hold",
        revision_id="rev-hold",
        holds=(HoldRecord("hold-1", "ambiguous-company", "two names"),),
    )
    with pytest.raises(RevisionContractError):
        store.activate(held.revision_id)
    view = store.context_view("project--1")
    assert view.active_revision_id is None
    assert view.revisions[0].status == "draft"
    assert len(view.jobs) == 2
