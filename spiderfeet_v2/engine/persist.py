"""Persist scan_step four forms + scan_result_graph via AL CRUD (R10-27 / AL)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Optional
from uuid import UUID, uuid5

from spiderfeet_v2.engine.status import scan_status_for_module
from spiderfeet_v2.workflow.context_export import (
    apply_context_export,
    empty_context,
    step_exports_scan_graph,
)
from spiderfeet_v2.workflow.typedb_convert import dump_canonical_yaml

_RESULT_NS = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def scan_result_id_for(scan_instance_id: str) -> str:
    return f"scan-result--{uuid5(_RESULT_NS, scan_instance_id)}"


def temporary_subgraph_id_for(project_id: str) -> str:
    return f"temporary-subgraph--{uuid5(_RESULT_NS, project_id)}"


def _json_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _command_text(command: Any) -> str:
    if command is None:
        return ""
    if isinstance(command, str):
        return command
    if isinstance(command, (list, tuple)):
        return " ".join(str(p) for p in command)
    return str(command)


def graph_node_ids(graph: Mapping[str, Any] | None) -> List[str]:
    ids: List[str] = []
    for node in (graph or {}).get("nodes") or []:
        if not isinstance(node, Mapping):
            continue
        nid = node.get("nugget_instance_id") or node.get("id")
        if nid:
            ids.append(str(nid))
    return sorted(set(ids))


def four_form_attrs(
    *,
    module_result: Mapping[str, Any],
    scan_status: str,
    step: Mapping[str, Any] | None = None,
    output_vars: Mapping[str, List[str]] | None = None,
) -> Dict[str, Any]:
    """Build scan_step attribute payload (four UI forms + metadata)."""
    graph = module_result.get("graph") or {"nodes": [], "edges": []}
    counts = module_result.get("counts") or {}
    nugget_count = int(counts.get("nodes") or len(graph.get("nodes") or []))
    results_payload = {
        "status": scan_status,
        "module_status": module_result.get("status"),
        "counts": counts,
        "vars": dict(output_vars or {}),
        "error": module_result.get("error"),
        "exit_code": module_result.get("exit_code"),
    }
    by_type: Dict[str, int] = {}
    for node in graph.get("nodes") or []:
        if isinstance(node, Mapping) and node.get("nugget_id"):
            nid = str(node["nugget_id"])
            by_type[nid] = by_type.get(nid, 0) + 1

    text = str(module_result.get("text") or "")
    narrative = str(module_result.get("narrative") or "")
    err = module_result.get("error")
    if not text and err:
        text = f"ERROR: {err}\n"
    if not narrative and err:
        narrative = f"# Scan error\n\n{err}\n"

    attrs: Dict[str, Any] = {
        "scan_status": scan_status,
        "scan_nugget_count": nugget_count,
        "scan_duration": float(module_result.get("duration") or 0.0),
        "scan_timestamp": module_result.get("timestamp") or None,
        "scan_ui_cli_command": _command_text(module_result.get("command")),
        "scan_ui_text_form": text,
        "scan_ui_structured_form": _json_text(module_result.get("structured")),
        "scan_ui_structured_form_type": str(
            module_result.get("structured_type") or "json"
        ),
        "scan_ui_graph_form": _json_text(graph),
        "scan_ui_markdown_narrative_form": narrative,
        "scan_results": _json_text(results_payload),
        "scan_results_by_type": _json_text(by_type),
    }
    if step is not None:
        attrs["scan_yaml"] = dump_canonical_yaml(dict(step))
    # Drop None timestamp so CRUD skips unset datetime attrs.
    if not attrs.get("scan_timestamp"):
        attrs.pop("scan_timestamp", None)
    return attrs


def _is_json_string_schema_gap(exc: BaseException) -> bool:
    """True when TypeDB schema lacks dual-form ``json_string`` (stale spiderfeet-actual)."""
    msg = str(exc)
    return "json_string" in msg or "SubgraphCodec" in type(exc).__name__


def _persist_scan_result_graph(
    store: Any,
    *,
    scan_instance_id: str,
    scan_result_id: str,
    graph: Mapping[str, Any],
) -> bool:
    """Create/update scan_result_graph with dual-form when the schema supports it.

    Returns True when dual-form graph payload was stored. On schema drift
    (e.g. missing ``json_string`` in an older ``spiderfeet-actual`` load),
    returns False without failing the step — four forms remain on ``scan_step``.
    """
    try:
        existing_rg = store.get_subgraph("scan_result_graph", scan_result_id)
    except Exception as exc:  # noqa: BLE001
        if _is_json_string_schema_gap(exc):
            return False
        raise

    try:
        if existing_rg is None:
            store.create_subgraph(
                {
                    "kind": "scan_result_graph",
                    "scan_result_id": scan_result_id,
                    "scan_instance_id": scan_instance_id,
                    "graph": graph,
                }
            )
        else:
            store.update_subgraph(
                "scan_result_graph",
                scan_result_id,
                {"graph": graph},
            )
        return True
    except Exception as exc:  # noqa: BLE001 — TypeDB schema / codec failures
        if not _is_json_string_schema_gap(exc):
            raise
        # Partial shell insert may already exist; do not re-query (get_subgraph
        # also touches json_string). Four forms on scan_step are authoritative.
        return False


def ensure_scan_step(
    store: Any,
    *,
    scan_instance_id: str,
    module_id: str,
    step: Mapping[str, Any],
    scan_status: str,
) -> Dict[str, Any]:
    """Create or update a scan_step shell row for lifecycle tracking."""
    payload = {
        "scan_instance_id": scan_instance_id,
        "step_module_id": module_id,
        "service_module_id": module_id,
        "scan_status": scan_status,
        "scan_yaml": dump_canonical_yaml(dict(step)),
    }
    existing = store.get_scan_step(scan_instance_id)
    if existing is None:
        return store.create_scan_step(payload)
    return store.update_scan_step(scan_instance_id, payload)


def persist_module_result(
    store: Any,
    *,
    scan_instance_id: str,
    module_id: str,
    step: Mapping[str, Any],
    module_result: Mapping[str, Any],
    output_vars: Mapping[str, List[str]] | None = None,
) -> Dict[str, Any]:
    """Write four forms onto the scan_step and dual-form scan_result_graph."""
    module_status = str(module_result.get("status") or "ERROR")
    scan_status = scan_status_for_module(module_status)
    attrs = four_form_attrs(
        module_result=module_result,
        scan_status=scan_status,
        step=step,
        output_vars=output_vars,
    )
    attrs["step_module_id"] = module_id

    existing = store.get_scan_step(scan_instance_id)
    if existing is None:
        store.create_scan_step(
            {
                "scan_instance_id": scan_instance_id,
                "service_module_id": module_id,
                **attrs,
            }
        )
    else:
        store.update_scan_step(scan_instance_id, attrs)

    graph = module_result.get("graph") or {"nodes": [], "edges": []}
    rg_id = scan_result_id_for(scan_instance_id)
    dual_ok = _persist_scan_result_graph(
        store,
        scan_instance_id=scan_instance_id,
        scan_result_id=rg_id,
        graph=graph,
    )

    # Link produced nuggets after dual-form materialization (nuggets now exist).
    produced = graph_node_ids(graph) if dual_ok else []
    if produced and hasattr(store, "update_scan_step"):
        try:
            store.update_scan_step(
                scan_instance_id,
                {
                    "produced_ids": produced,
                    "service_module_id": module_id,
                },
            )
        except Exception:  # noqa: BLE001 — FakeCrud / schema may not allow links yet
            pass

    return {
        "scan_instance_id": scan_instance_id,
        "scan_result_id": rg_id,
        "scan_status": scan_status,
        "produced_ids": produced,
        "dual_form": dual_ok,
    }


def persist_temporary_export(
    store: Any,
    *,
    project_id: str,
    step: Mapping[str, Any],
    scan_graph: Mapping[str, Any],
    existing_subgraph_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Merge exported scan_graph into the project's temporary_subgraph when marked."""
    if not step_exports_scan_graph(step):
        return {"exported": False, "temporary_subgraph_id": existing_subgraph_id}

    sg_id = existing_subgraph_id or temporary_subgraph_id_for(project_id)
    context = empty_context()
    existing = None
    try:
        existing = store.get_subgraph("temporary_subgraph", sg_id)
    except Exception as exc:  # noqa: BLE001
        if not _is_json_string_schema_gap(exc):
            raise
        existing = None

    if existing is not None:
        dual = existing
        if hasattr(store, "get_subgraph_dual"):
            try:
                dual = store.get_subgraph_dual("temporary_subgraph", sg_id)
            except Exception:  # noqa: BLE001
                dual = existing
        graph = (dual or {}).get("graph")
        if isinstance(graph, dict):
            context["nodes"] = list(graph.get("nodes") or [])
            context["edges"] = list(graph.get("edges") or [])
        elif (dual or {}).get("nodes") is not None:
            context["nodes"] = list(dual.get("nodes") or [])
            context["edges"] = list(dual.get("edges") or [])

    result = apply_context_export(context, step, scan_graph)
    if not result["exported"]:
        return {"exported": False, "temporary_subgraph_id": sg_id}

    payload_graph = result["context"]
    try:
        if existing is None:
            store.create_subgraph(
                {
                    "kind": "temporary_subgraph",
                    "temporary_subgraph_id": sg_id,
                    "project_id": project_id,
                    "graph": payload_graph,
                }
            )
        else:
            store.update_subgraph(
                "temporary_subgraph",
                sg_id,
                {"graph": payload_graph},
            )
    except Exception as exc:  # noqa: BLE001 — schema drift on dual-form attrs
        if not _is_json_string_schema_gap(exc):
            raise
        return {
            "exported": True,
            "temporary_subgraph_id": sg_id,
            "node_count": len(payload_graph.get("nodes") or []),
            "edge_count": len(payload_graph.get("edges") or []),
            "persisted": False,
        }
    return {
        "exported": True,
        "temporary_subgraph_id": sg_id,
        "node_count": len(payload_graph.get("nodes") or []),
        "edge_count": len(payload_graph.get("edges") or []),
        "persisted": True,
    }
