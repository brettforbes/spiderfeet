"""Create a new project + info-only workflow (SPEC-013 R13-04 / B2-1)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from spiderfeet_v2.workflow.typedb_convert import dump_canonical_yaml


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def new_project_id() -> str:
    return f"project--{uuid4()}"


def new_workflow_id() -> str:
    return f"workflow--{uuid4()}"


def build_info_only_workflow_doc(
    *,
    workflow_id: str,
    name: str,
    description: str,
    author: str = "User",
    created: Optional[str] = None,
) -> Dict[str, Any]:
    """Info-only YAML DSL: apiVersion/kind/id/info — no inputs/target/steps."""
    return {
        "apiVersion": "spiderfeet.workflow/v1",
        "kind": "Workflow",
        "id": workflow_id,
        "info": {
            "name": name,
            "description": description,
            "author": author,
            "created": created or _now_iso(),
        },
    }


def build_info_only_workflow_yaml(
    *,
    workflow_id: str,
    name: str,
    description: str,
    author: str = "User",
    created: Optional[str] = None,
) -> str:
    return dump_canonical_yaml(
        build_info_only_workflow_doc(
            workflow_id=workflow_id,
            name=name,
            description=description,
            author=author,
            created=created,
        )
    )


def create_new_project(
    store: Any,
    *,
    project_name: str,
    project_description: str = "",
    project_id: Optional[str] = None,
    project_created: Optional[str] = None,
    stix_incident_id: Optional[str] = None,
    workflow_id: Optional[str] = None,
    author: str = "User",
) -> Dict[str, Any]:
    """Persist project entity + info-only workflow linked to it.

    No target/steps and no placeholder target — the workflow's project link is
    the sole TypeDB role player (schema §0.1 / R13-04).
    """
    pid = project_id or new_project_id()
    wid = workflow_id or new_workflow_id()
    created = project_created or _now_iso()
    name = (project_name or "").strip() or "Untitled Project"
    description = project_description or ""

    yaml_text = build_info_only_workflow_yaml(
        workflow_id=wid,
        name=name,
        description=description,
        author=author,
        created=created,
    )

    project_row: Dict[str, Any] = {
        "project_id": pid,
        "project_name": name,
        "project_description": description,
        "project_created": created,
    }
    if stix_incident_id:
        project_row["stix_incident_id"] = stix_incident_id

    store.create_project(project_row)
    store.create_workflow(
        {
            "workflow_id": wid,
            "name": name,
            "description": description,
            "author": author,
            "created": created,
            "workflow_yaml": yaml_text,
            "project_id": pid,
        }
    )
    out = store.get_project(pid)
    if out is None:
        raise RuntimeError(f"project missing after create: {pid}")
    out["primary_workflow_id"] = wid
    out["workflow_yaml"] = yaml_text
    return out
