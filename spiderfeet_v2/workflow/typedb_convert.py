"""YAML-DSL ↔ TypeDB conversion for workflows (SPEC-010 AM2 / R10-21).

Uses AL1 ``CrudStore`` for persistence and AM1 ``validate_workflow_dict`` for
DSL validation. ``*_yaml`` attributes hold the string DSL shadow; entity/
relation attributes + role links hold the typed TypeDB form.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence
from uuid import UUID, uuid5

import yaml

from spiderfeet_v2.workflow.loader import (
    WorkflowLoadError,
    schedule_waves,
    validate_workflow_dict,
)

# Deterministic ids for target / scan_step derived from workflow + local key.
_WORKFLOW_ID_NS = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

API_WORKFLOW_KEYS = (
    "workflow_id",
    "target",
    "first_step",
    "prior_step",
    "next_step",
    "workflow_yaml",
)


class WorkflowConvertError(ValueError):
    """YAML ↔ TypeDB conversion failure."""


@dataclass
class TypedbWorkflowForms:
    """CRUD payloads for target + scan_steps + workflow (plus yaml shadows)."""

    target: Optional[Dict[str, Any]]
    steps: List[Dict[str, Any]]
    workflow: Dict[str, Any]
    step_id_by_scan_instance: Dict[str, str] = field(default_factory=dict)

    @property
    def workflow_id(self) -> str:
        return str(self.workflow["workflow_id"])

    @property
    def workflow_yaml(self) -> str:
        return str(self.workflow["workflow_yaml"])


def dump_canonical_yaml(data: Any) -> str:
    """Dump a mapping/list to a stable YAML string (trailing newline)."""
    text = yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    )
    return text if text.endswith("\n") else text + "\n"


def parse_yaml_string(text: str) -> Any:
    return yaml.safe_load(text)


def canonical_workflow_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a workflow document for equality (YAML round-trip shape)."""
    if not isinstance(doc, dict):
        raise WorkflowConvertError("workflow document must be a mapping")
    # Round-trip through dump/load so multiline scalars and defaults match.
    return parse_yaml_string(dump_canonical_yaml(doc))


def workflows_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return canonical_workflow_dict(a) == canonical_workflow_dict(b)


def scan_instance_id_for(workflow_id: str, step_id: str) -> str:
    return f"scan_step--{uuid5(_WORKFLOW_ID_NS, f'{workflow_id}:{step_id}')}"


def target_id_for(workflow_id: str, target_key: str) -> str:
    return f"target--{uuid5(_WORKFLOW_ID_NS, f'{workflow_id}:{target_key}')}"


def module_id_for_step(step: Dict[str, Any]) -> str:
    """Map a DSL step to an osint-service ``module_id`` (``sfp_cli_*``)."""
    sid = str(step.get("id") or "")
    if sid.startswith("sfp_cli_"):
        return sid
    uses = str(step.get("uses") or "")
    if uses.startswith("tool."):
        return f"sfp_cli_{uses.split('.', 1)[1]}"
    raise WorkflowConvertError(f"cannot derive module_id for step {sid!r}")


def _primary_target_values(doc: Dict[str, Any]) -> tuple[str, List[str], Dict[str, Any]]:
    inputs = doc.get("inputs") or {}
    if "targets" in inputs:
        key = "targets"
        spec = inputs["targets"]
    else:
        key = sorted(inputs.keys())[0]
        spec = inputs[key]
    values = list(spec.get("values") or spec.get("default") or [])
    if not values:
        raise WorkflowConvertError("workflow inputs must provide at least one target value")
    return key, values, spec


def _dag_role_step_ids(steps: Sequence[Dict[str, Any]]) -> tuple[str, List[str], List[str]]:
    """Return (first_step_id, prior_step_ids, next_step_ids) as DSL step ids."""
    waves = schedule_waves(list(steps))
    first = waves[0][0]
    depended_upon = sorted({dep for s in steps for dep in (s.get("needs") or [])})
    all_ids = {s["id"] for s in steps}
    leaves = sorted(all_ids - set(depended_upon)) if depended_upon else [first]
    # Roots with no dependents still count as prior when they are the only step.
    prior = depended_upon or [first]
    return first, prior, leaves


def yaml_to_typedb_forms(doc: Dict[str, Any], *, validate: bool = True) -> TypedbWorkflowForms:
    """Convert a YAML-DSL workflow document into AL1 CRUD payloads."""
    if validate:
        try:
            validate_workflow_dict(doc)
        except WorkflowLoadError as exc:
            raise WorkflowConvertError(str(exc)) from exc

    workflow_id = doc.get("id")
    if not workflow_id:
        raise WorkflowConvertError("workflow id is required")

    info = doc.get("info") or {}
    steps = list(doc.get("steps") or [])
    if not steps:
        raise WorkflowConvertError("workflow must have at least one step")

    # No-input workflows (e.g. 12A2 netdiscover) materialize steps without a target.
    inputs = doc.get("inputs") or {}
    target: Optional[Dict[str, Any]] = None
    tid: Optional[str] = None
    if inputs:
        input_key, values, target_spec = _primary_target_values(doc)
        target_value = values[0]
        tid = target_id_for(workflow_id, f"{input_key}:{target_value}")
        target_yaml = dump_canonical_yaml(
            {
                "key": input_key,
                "type": target_spec.get("type", "string_list"),
                "description": target_spec.get("description"),
                "values": values,
            }
        )
        target = {
            "target_id": tid,
            "target_value": target_value,
            "target_description": target_spec.get("description")
            or info.get("description")
            or input_key,
            "target_yaml": target_yaml,
        }
        if info.get("created"):
            target["target_created"] = info["created"]

    first_dsl, prior_dsl, next_dsl = _dag_role_step_ids(steps)
    step_rows: List[Dict[str, Any]] = []
    step_id_by_scan: Dict[str, str] = {}
    for step in steps:
        sid_dsl = step["id"]
        scan_id = scan_instance_id_for(workflow_id, sid_dsl)
        module_id = module_id_for_step(step)
        step_rows.append(
            {
                "scan_instance_id": scan_id,
                "step_module_id": module_id,
                "service_module_id": module_id,
                "scan_status": "UNKNOWN",
                "scan_yaml": dump_canonical_yaml(step),
            }
        )
        step_id_by_scan[scan_id] = sid_dsl

    def _scan(dsl_id: str) -> str:
        return scan_instance_id_for(workflow_id, dsl_id)

    workflow_yaml = dump_canonical_yaml(doc)
    workflow: Dict[str, Any] = {
        "workflow_id": workflow_id,
        "name": info.get("name"),
        "description": info.get("description"),
        "author": info.get("author"),
        "created": info.get("created"),
        "workflow_yaml": workflow_yaml,
        "first_step_id": _scan(first_dsl),
        "prior_step_ids": [_scan(i) for i in prior_dsl],
        "next_step_ids": [_scan(i) for i in next_dsl],
    }
    if tid:
        workflow["target_id"] = tid
    return TypedbWorkflowForms(
        target=target,
        steps=step_rows,
        workflow=workflow,
        step_id_by_scan_instance=step_id_by_scan,
    )


def typedb_forms_to_yaml(
    workflow: Dict[str, Any],
    steps: Sequence[Dict[str, Any]] | None = None,
    target: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Rebuild a YAML-DSL document from TypeDB CRUD rows / yaml attrs.

    Prefers ``workflow_yaml`` when present (canonical string shadow). Falls back
    to assembling ``info`` + ``inputs`` + ``steps`` from typed attrs +
    ``scan_yaml`` / ``target_yaml``.
    """
    yaml_text = workflow.get("workflow_yaml")
    if yaml_text:
        doc = parse_yaml_string(yaml_text)
        if not isinstance(doc, dict):
            raise WorkflowConvertError("workflow_yaml did not parse to a mapping")
        return doc

    # Assemble from fragments when workflow_yaml is absent.
    if not steps:
        raise WorkflowConvertError(
            "cannot rebuild YAML without workflow_yaml or scan_step rows"
        )
    step_docs: List[Dict[str, Any]] = []
    for row in steps:
        frag = row.get("scan_yaml")
        if not frag:
            raise WorkflowConvertError(
                f"scan_step {row.get('scan_instance_id')} missing scan_yaml"
            )
        parsed = parse_yaml_string(frag)
        if not isinstance(parsed, dict):
            raise WorkflowConvertError("scan_yaml must parse to a mapping")
        step_docs.append(parsed)

    # Preserve DAG order via needs waves when possible.
    try:
        waves = schedule_waves(step_docs)
        order = {sid: i for i, sid in enumerate(x for wave in waves for x in wave)}
        step_docs.sort(key=lambda s: order.get(s["id"], 10_000))
    except Exception:  # noqa: BLE001
        step_docs.sort(key=lambda s: s.get("id") or "")

    inputs: Dict[str, Any] = {}
    if target and target.get("target_yaml"):
        tdoc = parse_yaml_string(target["target_yaml"])
        if isinstance(tdoc, dict) and tdoc.get("key"):
            key = tdoc["key"]
            inputs[key] = {
                "type": tdoc.get("type", "string_list"),
                "description": tdoc.get("description") or target.get("target_description"),
                "values": list(tdoc.get("values") or [target.get("target_value")]),
            }
    if not inputs and target:
        inputs["targets"] = {
            "type": "string_list",
            "description": target.get("target_description") or "targets",
            "values": [target["target_value"]],
        }
    if not inputs:
        raise WorkflowConvertError("cannot rebuild inputs without target_yaml/target")

    info: Dict[str, Any] = {"name": workflow.get("name") or "unnamed"}
    if workflow.get("description") is not None:
        info["description"] = workflow["description"]
    if workflow.get("author"):
        info["author"] = workflow["author"]
    if workflow.get("created"):
        info["created"] = workflow["created"]

    return {
        "apiVersion": "spiderfeet.workflow/v1",
        "kind": "Workflow",
        "id": workflow["workflow_id"],
        "info": info,
        "inputs": inputs,
        "steps": step_docs,
    }


def typedb_to_api_json(
    workflow: Dict[str, Any],
    *,
    prefer_projection_keys: bool = True,
) -> Dict[str, Any]:
    """Map a CRUD workflow row (or projection row) to the AL3 API JSON shape.

    Shape (SPEC010_FUN_PROJECTIONS §3)::

        {
          "workflow_id": "...",
          "target": "...",
          "first_step": "...",
          "prior_step": [...],
          "next_step": [...],
          "workflow_yaml": "..."
        }
    """
    if prefer_projection_keys and "target" in workflow and "first_step" in workflow:
        # Already projection-shaped.
        out = {
            "workflow_id": workflow.get("workflow_id"),
            "target": workflow.get("target"),
            "first_step": workflow.get("first_step"),
            "prior_step": list(workflow.get("prior_step") or []),
            "next_step": list(workflow.get("next_step") or []),
            "workflow_yaml": workflow.get("workflow_yaml"),
        }
        if workflow.get("project") is not None or workflow.get("project_id") is not None:
            out["project"] = workflow.get("project") or workflow.get("project_id")
        return out
    out = {
        "workflow_id": workflow.get("workflow_id"),
        "target": workflow.get("target_id"),
        "first_step": workflow.get("first_step_id"),
        "prior_step": list(workflow.get("prior_step_ids") or []),
        "next_step": list(workflow.get("next_step_ids") or []),
        "workflow_yaml": workflow.get("workflow_yaml"),
    }
    if workflow.get("project_id") is not None:
        out["project"] = workflow.get("project_id")
    return out


def _delete_workflow_bundle(store: Any, workflow_id: str) -> None:
    """Best-effort delete of workflow + its linked steps/target (replace path)."""
    current = store.get_workflow(workflow_id)
    if current is None:
        return
    scan_ids = set(current.get("prior_step_ids") or [])
    scan_ids.update(current.get("next_step_ids") or [])
    if current.get("first_step_id"):
        scan_ids.add(current["first_step_id"])
    tid = current.get("target_id")
    store.delete_workflow(workflow_id)
    for sid in sorted(scan_ids):
        store.delete_scan_step(sid)
    if tid:
        store.delete_target(tid)


def persist_workflow_yaml(
    store: Any,
    doc: Dict[str, Any],
    *,
    validate: bool = True,
    replace: bool = True,
    project_id: str | None = None,
) -> TypedbWorkflowForms:
    """Persist YAML-DSL → TypeDB via AL1 CRUD. Returns the forms written.

    When replacing an existing workflow, preserves its ``project_id`` link unless
    an explicit ``project_id`` argument is supplied.
    """
    forms = yaml_to_typedb_forms(doc, validate=validate)
    existing = store.get_workflow(forms.workflow_id)
    preserved_project_id = project_id
    if existing is not None:
        if preserved_project_id is None:
            preserved_project_id = existing.get("project_id")
        if not replace:
            raise WorkflowConvertError(
                f"workflow already exists: {forms.workflow_id}"
            )
        _delete_workflow_bundle(store, forms.workflow_id)

    if forms.target is not None:
        if store.get_target(forms.target["target_id"]) is None:
            store.create_target(forms.target)
        else:
            store.update_target(forms.target["target_id"], forms.target)

    for step in forms.steps:
        if store.get_scan_step(step["scan_instance_id"]) is None:
            store.create_scan_step(step)
        else:
            store.update_scan_step(step["scan_instance_id"], step)

    workflow_row = dict(forms.workflow)
    if preserved_project_id:
        workflow_row["project_id"] = preserved_project_id
    store.create_workflow(workflow_row)
    forms.workflow = workflow_row
    return forms


def load_workflow_yaml(store: Any, workflow_id: str) -> Dict[str, Any]:
    """Load TypeDB workflow → YAML-DSL document (via ``workflow_yaml`` / fragments)."""
    workflow = store.get_workflow(workflow_id)
    if workflow is None:
        raise WorkflowConvertError(f"workflow not found: {workflow_id}")

    step_ids = set(workflow.get("prior_step_ids") or [])
    step_ids.update(workflow.get("next_step_ids") or [])
    if workflow.get("first_step_id"):
        step_ids.add(workflow["first_step_id"])
    steps = []
    for sid in sorted(step_ids):
        row = store.get_scan_step(sid)
        if row is not None:
            steps.append(row)

    target = None
    if workflow.get("target_id"):
        target = store.get_target(workflow["target_id"])

    doc = typedb_forms_to_yaml(workflow, steps=steps, target=target)
    return doc


def load_workflow_api_json(
    store: Any,
    workflow_id: str,
    *,
    projection_store: Any = None,
) -> Dict[str, Any]:
    """TypeDB → API JSON. Uses ProjectionStore when provided (AL3 shape)."""
    if projection_store is not None:
        projected = projection_store.get_workflow(workflow_id)
        if projected is None:
            raise WorkflowConvertError(f"workflow not found: {workflow_id}")
        return typedb_to_api_json(projected, prefer_projection_keys=True)

    workflow = store.get_workflow(workflow_id)
    if workflow is None:
        raise WorkflowConvertError(f"workflow not found: {workflow_id}")
    return typedb_to_api_json(workflow, prefer_projection_keys=False)


def yaml_string_to_typedb_forms(text: str, *, validate: bool = True) -> TypedbWorkflowForms:
    doc = parse_yaml_string(text)
    if not isinstance(doc, dict):
        raise WorkflowConvertError("YAML root must be a mapping")
    return yaml_to_typedb_forms(doc, validate=validate)


# Re-export helpers useful to callers / tests
__all__ = [
    "API_WORKFLOW_KEYS",
    "TypedbWorkflowForms",
    "WorkflowConvertError",
    "canonical_workflow_dict",
    "dump_canonical_yaml",
    "load_workflow_api_json",
    "load_workflow_yaml",
    "module_id_for_step",
    "parse_yaml_string",
    "persist_workflow_yaml",
    "scan_instance_id_for",
    "target_id_for",
    "typedb_forms_to_yaml",
    "typedb_to_api_json",
    "workflows_equal",
    "yaml_string_to_typedb_forms",
    "yaml_to_typedb_forms",
]
