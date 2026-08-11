"""Persist scan_step four forms + scan_result_graph via AL CRUD (R10-27 / AL)."""

from __future__ import annotations

import json
import logging
from threading import Lock
from typing import Any, Dict, List, Mapping, Optional
from uuid import UUID, uuid5

from spiderfeet_v2.engine.status import scan_status_for_module
from spiderfeet_v2.engine.temporary_viewer_graph import (
    new_temporary_subgraph_id,
    stamp_viewer_graph,
    step_scan_description,
    step_scan_name,
)
from spiderfeet_v2.workflow.context_export import (
    empty_context,
    step_exports_scan_graph,
)
from spiderfeet_v2.workflow.typedb_convert import dump_canonical_yaml

_RESULT_NS = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
_TEMP_CONTEXT_LOCK = Lock()
_LOG = logging.getLogger(__name__)


def scan_result_id_for(scan_instance_id: str) -> str:
    return f"scan-result--{uuid5(_RESULT_NS, scan_instance_id)}"


def temporary_subgraph_id_for(project_id: str) -> str:
    """Legacy singleton id (SPEC-016). Prefer ``new_temporary_subgraph_id`` (SPEC-017)."""
    return f"temporary-subgraph--{uuid5(_RESULT_NS, project_id)}"


def project_context_id_for(project_id: str) -> str:
    return f"project-context--{uuid5(_RESULT_NS, project_id)}"


def list_project_temporary_subgraphs(store: Any, project_id: str) -> List[Dict[str, Any]]:
    """Return all temporary_subgraph rows for a project (best-effort)."""
    rows: List[Dict[str, Any]] = []
    if hasattr(store, "list_subgraphs"):
        try:
            for row in store.list_subgraphs("temporary_subgraph") or []:
                if row and row.get("project_id") == project_id:
                    rows.append(row)
            return rows
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("list_subgraphs temporary failed: %s", exc)
    # FakeCrudStore / dict fallback
    subgraphs = getattr(store, "subgraphs", None)
    if isinstance(subgraphs, dict):
        for key, row in subgraphs.items():
            if not str(key).startswith("temporary_subgraph:"):
                continue
            if row and row.get("project_id") == project_id:
                rows.append(dict(row))
    return rows


def reset_temporary_context(
    store: Any,
    *,
    project_id: str,
    existing_subgraph_id: Optional[str] = None,
) -> Optional[str]:
    """Delete all temporary_subgraph rows for the project (SPEC-017 R17-04).

    Returns None (no singleton id). ``existing_subgraph_id`` deleted if still present.
    """
    if not project_id:
        raise ValueError("project_id is required to reset temporary context")
    ids = {
        str(r.get("temporary_subgraph_id"))
        for r in list_project_temporary_subgraphs(store, project_id)
        if r.get("temporary_subgraph_id")
    }
    if existing_subgraph_id:
        ids.add(str(existing_subgraph_id))
    # Also drop legacy singleton if present.
    ids.add(temporary_subgraph_id_for(project_id))
    for sg_id in sorted(ids):
        try:
            store.delete_subgraph("temporary_subgraph", sg_id)
        except Exception:  # noqa: BLE001 — missing row is fine
            pass
    return None


def _workflow_scan_instance_ids(workflow_row: Mapping[str, Any]) -> List[str]:
    ids: set[str] = set()
    if workflow_row.get("first_step_id"):
        ids.add(str(workflow_row["first_step_id"]))
    for key in ("prior_step_ids", "next_step_ids"):
        for sid in workflow_row.get(key) or []:
            if sid:
                ids.add(str(sid))
    return sorted(ids)


def reset_workflow_execution(
    store: Any,
    *,
    workflow_id: str,
    project_id: Optional[str] = None,
    existing_temporary_subgraph_id: Optional[str] = None,
    cancel_wait_s: float = 30.0,
) -> Dict[str, Any]:
    """Reset a workflow to unscanned shells while keeping the same YAML (R15-04).

    Cancels any in-flight background run for the workflow first so it cannot
    repaint RUNNING after shells are rematerialized.
    """
    from spiderfeet_v2.engine.run_registry import get_run_registry
    from spiderfeet_v2.workflow.typedb_convert import (
        persist_workflow_yaml,
        scan_instance_id_for,
    )

    current = store.get_workflow(workflow_id)
    if current is None:
        raise ValueError(f"workflow not found: {workflow_id}")

    yaml_text = current.get("workflow_yaml")
    if not yaml_text or not str(yaml_text).strip():
        raise ValueError(f"workflow has no workflow_yaml to reset: {workflow_id}")

    import yaml

    doc = yaml.safe_load(yaml_text)
    if not isinstance(doc, dict) or not doc.get("steps"):
        raise ValueError(f"workflow_yaml is not a valid workflow document: {workflow_id}")

    cancelled_run_id: Optional[str] = None
    registry = get_run_registry()
    cancelled_run_id = registry.cancel_workflow(workflow_id)
    if cancelled_run_id:
        registry.wait(cancelled_run_id, timeout=cancel_wait_s)

    pid = project_id or current.get("project_id")
    scan_ids = set(_workflow_scan_instance_ids(current))
    for step in doc.get("steps") or []:
        if isinstance(step, Mapping) and step.get("id"):
            scan_ids.add(scan_instance_id_for(workflow_id, str(step["id"])))

    deleted_result_graphs = 0
    deleted_steps = 0
    for sid in sorted(scan_ids):
        rg_id = scan_result_id_for(sid)
        try:
            if store.delete_subgraph("scan_result_graph", rg_id):
                deleted_result_graphs += 1
        except Exception:  # noqa: BLE001 — missing subgraph is fine
            pass
        try:
            if store.delete_scan_step(sid):
                deleted_steps += 1
        except Exception:  # noqa: BLE001 — missing step is fine
            pass

    forms = persist_workflow_yaml(
        store,
        doc,
        validate=False,
        replace=True,
        project_id=pid,
    )

    temp_id: Optional[str] = None
    target_seed: Optional[Dict[str, Any]] = None
    if pid:
        reset_temporary_context(
            store,
            project_id=str(pid),
            existing_subgraph_id=existing_temporary_subgraph_id,
        )
        target_seed = ensure_project_target_temps(store, project_id=str(pid))
        temp_id = (target_seed.get("temporary") or {}).get("temporary_subgraph_id")

    return {
        "status": "RESET",
        "message": "Workflow scan results and temporary context cleared.",
        "workflow_id": workflow_id,
        "project_id": pid,
        "steps_reset": len(forms.steps),
        "scan_steps_deleted": deleted_steps,
        "scan_result_graphs_deleted": deleted_result_graphs,
        "temporary_subgraph_id": temp_id,
        "target_seed": target_seed,
        "cancelled_run_id": cancelled_run_id,
        "run_ready": True,
    }


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

    Returns True when dual-form graph payload was stored. Dual-form is best-effort:
    any TypeDB/schema/codec failure returns False without failing the step — the
    four UI forms on ``scan_step`` remain authoritative. Raising here previously
    let ``ensure_scan_step(ERROR-FAILED)`` clobber an already-persisted SUCCESS.
    """
    try:
        existing_rg = store.get_subgraph("scan_result_graph", scan_result_id)
    except Exception as exc:  # noqa: BLE001 — dual-form optional
        _LOG.warning(
            "scan_result_graph get failed for %s (%s); keeping scan_step forms",
            scan_result_id,
            exc,
        )
        return False

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
    except Exception as exc:  # noqa: BLE001 — dual-form optional
        _LOG.warning(
            "scan_result_graph write failed for %s (%s); keeping scan_step forms",
            scan_result_id,
            exc,
        )
        # Partial shell insert may already exist; do not re-query.
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


def _load_temporary_context(
    store: Any,
    *,
    sg_id: str,
) -> tuple[Dict[str, Any], Any]:
    """Return (context_graph, existing_row_or_None) for a temporary subgraph."""
    context = empty_context()
    existing = None
    try:
        existing = store.get_subgraph("temporary_subgraph", sg_id)
    except Exception as exc:  # noqa: BLE001
        if not _is_json_string_schema_gap(exc):
            raise
        return context, None

    if existing is None:
        return context, None

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
    return context, existing


def _create_temporary_subgraph_row(
    store: Any,
    *,
    project_id: str,
    sg_id: str,
    scan_name: str,
    payload_graph: Mapping[str, Any],
    scan_description: Optional[str] = None,
    scan_instance_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create one temporary_subgraph row; never raise (UI enrichment only)."""
    node_count = len(payload_graph.get("nodes") or [])
    edge_count = len(payload_graph.get("edges") or [])
    payload: Dict[str, Any] = {
        "kind": "temporary_subgraph",
        "temporary_subgraph_id": sg_id,
        "project_id": project_id,
        "scan_name": scan_name,
        "graph": dict(payload_graph),
    }
    if scan_description:
        payload["scan_description"] = scan_description
    if scan_instance_id:
        payload["scan_instance_id"] = scan_instance_id
    try:
        store.create_subgraph(payload)
    except Exception as exc:  # noqa: BLE001 — schema drift / TypeDB stall must not fail scans
        _LOG.warning(
            "temporary_subgraph write failed for %s (%s); continuing without persist",
            sg_id,
            exc,
        )
        return {
            "exported": True,
            "temporary_subgraph_id": sg_id,
            "scan_name": scan_name,
            "node_count": node_count,
            "edge_count": edge_count,
            "persisted": False,
        }
    return {
        "exported": True,
        "temporary_subgraph_id": sg_id,
        "scan_name": scan_name,
        "node_count": node_count,
        "edge_count": edge_count,
        "persisted": True,
    }


def target_context_id_for(target_id: str) -> str:
    return f"target-context--{uuid5(_RESULT_NS, target_id)}"


def _hostnames_for_project(store: Any, project_id: str) -> List[str]:
    """Collect target hostnames from linked workflows (YAML inputs + target row)."""
    import yaml
    from spiderfeet_v2.workflow.loader import workflow_input_values
    from spiderfeet_v2.workflow.normalize import hostname_from_url

    hosts: List[str] = []
    seen: set[str] = set()
    project = store.get_project(project_id) or {}
    for wid in project.get("workflow_ids") or []:
        wf = store.get_workflow(wid) or {}
        tid = wf.get("target_id")
        if tid:
            tgt = store.get_target(tid) or {}
            for raw in (tgt.get("target_value"),):
                if not raw:
                    continue
                host = hostname_from_url(str(raw))
                if host and host not in seen:
                    seen.add(host)
                    hosts.append(host)
        yaml_text = wf.get("workflow_yaml")
        if not yaml_text:
            continue
        try:
            doc = yaml.safe_load(yaml_text)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(doc, dict):
            continue
        for raw in workflow_input_values(doc).get("targets") or []:
            host = hostname_from_url(str(raw))
            if host and host not in seen:
                seen.add(host)
                hosts.append(host)
    return hosts


def ensure_project_target_temps(
    store: Any,
    *,
    project_id: str,
) -> Dict[str, Any]:
    """Materialize target_context + ``scan_name=target`` temp (SPEC-017 R17-03).

    Idempotent: if a project temporary_subgraph with ``scan_name=target`` already
    exists, leave it. Always upserts ``target_context`` when a target entity exists.
    """
    if not project_id:
        return {"ensured": False, "reason": "missing project_id"}

    hostnames = _hostnames_for_project(store, project_id)
    existing_target_temps = [
        r
        for r in list_project_temporary_subgraphs(store, project_id)
        if r.get("scan_name") == "target"
    ]

    # Upsert target_context for the first linked target entity (stable id).
    project = store.get_project(project_id) or {}
    target_id = None
    target_row = None
    for wid in project.get("workflow_ids") or []:
        wf = store.get_workflow(wid) or {}
        tid = wf.get("target_id")
        if tid:
            target_id = tid
            target_row = store.get_target(tid)
            break

    target_context_id = None
    if target_id and hostnames:
        from modules_v2._core.graph_builder import nugget_node

        seed_graph: Dict[str, Any] = {"nodes": [], "edges": []}
        for host in hostnames:
            seed_graph["nodes"].append(nugget_node("DOMAIN_NAME", host))
        tc_id = target_context_id_for(str(target_id))
        target_context_id = tc_id
        payload = {
            "kind": "target_context",
            "target_context_id": tc_id,
            "target_id": str(target_id),
            "graph": seed_graph,
        }
        try:
            existing_tc = store.get_subgraph("target_context", tc_id)
            if existing_tc is None:
                store.create_subgraph(payload)
            else:
                store.update_subgraph("target_context", tc_id, {"graph": seed_graph})
            # Best-effort attrs via update if store supports extra keys later.
            _ = target_row
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("target_context upsert failed for %s: %s", target_id, exc)

    temp_result: Dict[str, Any] = {"exported": False}
    if hostnames and not existing_target_temps:
        temp_result = seed_targets_into_temporary_context(
            store,
            project_id=project_id,
            hostnames=hostnames,
        )
    elif existing_target_temps:
        temp_result = {
            "exported": True,
            "temporary_subgraph_id": existing_target_temps[0].get(
                "temporary_subgraph_id"
            ),
            "scan_name": "target",
            "persisted": True,
            "already_present": True,
        }

    return {
        "ensured": True,
        "hostnames": hostnames,
        "target_id": target_id,
        "target_context_id": target_context_id,
        "temporary": temp_result,
    }


def seed_targets_into_temporary_context(
    store: Any,
    *,
    project_id: str,
    hostnames: List[str],
    existing_subgraph_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a dedicated ``scan_name=target`` temporary_subgraph (SPEC-017 R17-03).

    ``existing_subgraph_id`` is ignored for writes (legacy singleton arg retained
    for call-site compatibility).
    """
    del existing_subgraph_id  # unused — each seed is its own uuid4 row
    if not project_id or not hostnames:
        return {
            "exported": False,
            "temporary_subgraph_id": None,
            "scan_name": "target",
            "node_count": 0,
        }

    from modules_v2._core.graph_builder import nugget_node

    seed_graph: Dict[str, Any] = {"nodes": [], "edges": []}
    for host in hostnames:
        h = str(host or "").strip()
        if not h:
            continue
        seed_graph["nodes"].append(nugget_node("DOMAIN_NAME", h))
    if not seed_graph["nodes"]:
        return {
            "exported": False,
            "temporary_subgraph_id": None,
            "scan_name": "target",
            "node_count": 0,
        }

    stamped = stamp_viewer_graph(seed_graph, scan_name="target")
    sg_id = new_temporary_subgraph_id()
    with _TEMP_CONTEXT_LOCK:
        return _create_temporary_subgraph_row(
            store,
            project_id=project_id,
            sg_id=sg_id,
            scan_name="target",
            scan_description="Workflow target",
            payload_graph=stamped,
        )


def persist_temporary_export(
    store: Any,
    *,
    project_id: str,
    step: Mapping[str, Any],
    scan_graph: Mapping[str, Any],
    existing_subgraph_id: Optional[str] = None,
    scan_instance_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new stamped temporary_subgraph row for an exporting step (R17-02).

    Does not merge into a singleton blob. ``existing_subgraph_id`` ignored.
    """
    del existing_subgraph_id  # unused — SPEC-017 is one row per export
    if not step_exports_scan_graph(step):
        return {"exported": False, "temporary_subgraph_id": None}

    nodes = list((scan_graph or {}).get("nodes") or [])
    edges = list((scan_graph or {}).get("edges") or [])
    if not nodes and not edges:
        return {"exported": False, "temporary_subgraph_id": None}

    scan_name = step_scan_name(step)
    stamped = stamp_viewer_graph(
        {"nodes": nodes, "edges": edges},
        scan_name=scan_name,
    )
    sg_id = new_temporary_subgraph_id()
    with _TEMP_CONTEXT_LOCK:
        return _create_temporary_subgraph_row(
            store,
            project_id=project_id,
            sg_id=sg_id,
            scan_name=scan_name,
            scan_description=step_scan_description(step),
            scan_instance_id=scan_instance_id,
            payload_graph=stamped,
        )
