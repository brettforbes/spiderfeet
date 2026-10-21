"""Idempotent SPEC-020 schema delta for context jobs and revisions."""

from __future__ import annotations

import re
from pathlib import Path

CONTEXT_ENTITIES = (
    "context_merge_job",
    "context_revision",
    "context_hold",
    "context_active_pointer",
)
CONTEXT_ATTRIBUTES = (
    "context_job_id",
    "context_project_ref",
    "context_job_status",
    "context_parent_revision_id",
    "context_rule_release_id",
    "context_source_hash",
    "context_normalizer_version",
    "context_discard_reason",
    "context_revision_id",
    "context_revision_status",
    "context_corrective_of",
    "context_created",
    "context_hold_id",
    "context_hold_code",
    "context_pointer_id",
    "context_active_project_ref",
)

_ENTITY_BLOCK = re.compile(
    r"(?ms)^(\tentity (context_merge_job|context_revision|context_hold|context_active_pointer),.*?;)\n"
)
_ATTRIBUTE_LINE = re.compile(
    r"(?m)^(\tattribute (context_[a-z_]+), .*?;)\n"
)
_DECLARED = re.compile(r"(?m)^\s*(?:entity|attribute)\s+([A-Za-z0-9_-]+)\s*,")

CANONICAL_SCHEMA = (
    Path(__file__).resolve().parents[2] / ".seed" / "spiderfeet_v2_semantic.tql"
)


def declared_labels(schema_text: str) -> set[str]:
    return set(_DECLARED.findall(schema_text))


def context_schema_delta(
    live_schema: str,
    canonical_schema: str | None = None,
) -> str | None:
    """Return a define block for missing context types, or None when current."""
    canonical = canonical_schema
    if canonical is None:
        canonical = CANONICAL_SCHEMA.read_text(encoding="utf-8")
    present = declared_labels(live_schema)
    attributes = [
        line
        for line, name in _ATTRIBUTE_LINE.findall(canonical)
        if name not in present
    ]
    entities = [
        block
        for block, name in _ENTITY_BLOCK.findall(canonical)
        if name not in present
    ]
    if not attributes and not entities:
        return None
    body = "\n".join([*attributes, *entities])
    return f"define\n{body}\n"
