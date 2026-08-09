"""Workflow YAML loader + DAG schedule (SPEC-010 R10-20)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore

_SCHEMA_DIR = Path(__file__).resolve().parent / "schema"
_WORKFLOW_SCHEMA = _SCHEMA_DIR / "workflow_v1.schema.json"
_GSE_SCHEMA = _SCHEMA_DIR / "gse_v1.schema.json"

ADAPTER_TOOLS = {
    "nmap",
    "netdiscover",
    "nerva",
    "pius",
    "subfinder",
    "httpx",
    "katana",
    "nuclei",
}


class WorkflowLoadError(ValueError):
    pass


def _load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_gse_binding(binding: Dict[str, Any]) -> None:
    if jsonschema is None:
        raise WorkflowLoadError("jsonschema package required for validation")
    jsonschema.validate(instance=binding, schema=_load_schema(_GSE_SCHEMA))


def workflow_input_values(doc: Dict[str, Any]) -> Dict[str, List[str]]:
    """Return workflow input string lists (``values`` or ``default``)."""
    out: Dict[str, List[str]] = {}
    for key, spec in (doc.get("inputs") or {}).items():
        out[key] = list(spec.get("values") or spec.get("default") or [])
    return out


def topological_waves(steps: Sequence[Dict[str, Any]]) -> List[List[str]] | None:
    """Return parallel execution waves, or None if a cycle exists."""
    deps: Dict[str, Set[str]] = {s["id"]: set(s.get("needs") or []) for s in steps}
    remaining = set(deps)
    waves: List[List[str]] = []
    while remaining:
        ready = sorted(i for i in remaining if not deps[i])
        if not ready:
            return None
        waves.append(ready)
        for r in ready:
            remaining.remove(r)
        for i in remaining:
            deps[i] -= set(ready)
    return waves


def schedule_waves(steps: Sequence[Dict[str, Any]]) -> List[List[str]]:
    """Schedule steps by ``needs`` DAG; raise on cycles."""
    waves = topological_waves(steps)
    if waves is None:
        raise WorkflowLoadError("workflow steps contain a cycle")
    return waves


def validate_workflow_dict(doc: Dict[str, Any], *, validate_gse: bool = True) -> None:
    if jsonschema is None:
        raise WorkflowLoadError("jsonschema package required for validation")
    try:
        jsonschema.validate(instance=doc, schema=_load_schema(_WORKFLOW_SCHEMA))
    except jsonschema.ValidationError as exc:
        raise WorkflowLoadError(exc.message) from exc

    steps = doc.get("steps") or []
    ids = [s.get("id") for s in steps]
    if len(ids) != len(set(ids)):
        raise WorkflowLoadError("duplicate step ids")

    id_set = set(ids)
    for step in steps:
        for dep in step.get("needs") or []:
            if dep not in id_set:
                raise WorkflowLoadError(f"step {step.get('id')} needs unknown step {dep}")
        uses = step.get("uses", "")
        if uses.startswith("tool."):
            tool = uses.split(".", 1)[1]
            if tool not in ADAPTER_TOOLS:
                raise WorkflowLoadError(f"unknown adapter tool in uses: {uses}")
        if validate_gse:
            vars_map = (step.get("output") or {}).get("vars") or {}
            for name, binding in vars_map.items():
                try:
                    validate_gse_binding(binding)
                except Exception as exc:  # noqa: BLE001
                    raise WorkflowLoadError(
                        f"invalid GSE for {step.get('id')}.{name}: {exc}"
                    ) from exc

    schedule_waves(steps)


def load_workflow(path: str | Path, *, validate: bool = True) -> Dict[str, Any]:
    p = Path(path)
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise WorkflowLoadError("workflow root must be a mapping")
    if validate:
        validate_workflow_dict(doc)
    return doc
