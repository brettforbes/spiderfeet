#!/usr/bin/env python3
"""SPEC-010 AP2 / R10-30 — reproduce the 12A acceptance run and assert invariants.

Usage (AP2 dry-run; does not require G3 / AP1 live evidence)::

    poetry run python spiderfeet_v2/acceptance/run_four_targets.py --target sbs.com.au

Live mode (after AP1 evidence / operator G3; talks to a running API)::

    poetry run python spiderfeet_v2/acceptance/run_four_targets.py --live --target sbs.com.au
    poetry run python spiderfeet_v2/acceptance/run_four_targets.py --live --all

Defaults favour dry-run + in-process TestClient so the harness can land and
pass without completing AP1. This script never marks AP1 done.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import yaml

from spiderfeet_v2.acceptance.assertions import (
    AcceptanceError,
    assert_graph_invariants,
    assert_queryable_json,
    assert_scan_step_artifacts,
    parse_graph_form,
)
from spiderfeet_v2.acceptance.client import (
    AcceptanceApi,
    HttpxApi,
    InProcessApi,
    api_reachable,
    build_inprocess_api,
)
from spiderfeet_v2.acceptance.targets import (
    DEFAULT_TARGETS,
    DOCUMENTED_TARGETS,
    is_documented,
    normalize_host,
)
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKFLOW_YAML = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
DEFAULT_EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence"
DEFAULT_BASE_URL = "http://127.0.0.1:8001/api/v1"


def _slug(host: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")


def _ids_for(host: str) -> Dict[str, str]:
    slug = _slug(host)
    return {
        "target_id": f"target--acceptance-{slug}",
        "workflow_id": f"workflow--acceptance-{slug}",
        "project_id": f"project--acceptance-{slug}",
    }


def load_workflow_yaml_for_target(
    host: str,
    *,
    workflow_yaml_path: Path,
    workflow_id: str,
) -> str:
    text = workflow_yaml_path.read_text(encoding="utf-8")
    doc = yaml.safe_load(text)
    if not isinstance(doc, dict):
        raise AcceptanceError(f"workflow YAML root must be a mapping: {workflow_yaml_path}")
    doc["id"] = workflow_id
    inputs = doc.setdefault("inputs", {})
    targets = inputs.setdefault("targets", {})
    targets["type"] = targets.get("type") or "string_list"
    targets["values"] = [f"https://{host}"]
    info = doc.setdefault("info", {})
    info["name"] = info.get("name") or "Recon Attack Surface"
    info["description"] = (
        f"Acceptance harness run for {host} (SPEC-010 R10-30). "
        + str(info.get("description") or "")
    ).strip()
    return yaml.safe_dump(doc, sort_keys=False)


def _require_ok(resp: Any, *, label: str) -> Any:
    if resp.status_code >= 400:
        raise AcceptanceError(
            f"{label}: HTTP {resp.status_code}: {getattr(resp, 'text', resp)}"
        )
    if resp.status_code == 204:
        return None
    try:
        return resp.json()
    except Exception as exc:
        raise AcceptanceError(f"{label}: response is not JSON: {exc}") from exc


def ensure_project_stack(
    api: AcceptanceApi,
    *,
    host: str,
    workflow_yaml: str,
    ids: Dict[str, str],
) -> None:
    """Idempotent create of target → workflow → project via the v2 API."""
    tid, wid, pid = ids["target_id"], ids["workflow_id"], ids["project_id"]

    existing = api.request("GET", f"/targets/{tid}")
    if existing.status_code == 404:
        _require_ok(
            api.request(
                "POST",
                "/targets",
                json={
                    "target_id": tid,
                    "target_value": host,
                    "target_description": f"SPEC-010 acceptance target {host}",
                },
            ),
            label=f"create target {tid}",
        )
    elif existing.status_code != 200:
        _require_ok(existing, label=f"get target {tid}")

    existing = api.request("GET", f"/workflows/{wid}")
    if existing.status_code == 404:
        _require_ok(
            api.request(
                "POST",
                "/workflows",
                json={
                    "workflow_id": wid,
                    "name": f"acceptance-{_slug(host)}",
                    "target_id": tid,
                    "workflow_yaml": workflow_yaml,
                },
            ),
            label=f"create workflow {wid}",
        )
    else:
        body = _require_ok(existing, label=f"get workflow {wid}")
        # Keep YAML aligned with the requested target.
        if body.get("workflow_yaml") != workflow_yaml or body.get("target_id") != tid:
            _require_ok(
                api.request(
                    "PATCH",
                    f"/workflows/{wid}",
                    json={"target_id": tid, "workflow_yaml": workflow_yaml},
                ),
                label=f"update workflow {wid}",
            )

    existing = api.request("GET", f"/projects/{pid}", params={"projection": "false"})
    if existing.status_code == 404:
        _require_ok(
            api.request(
                "POST",
                "/projects",
                json={
                    "project_id": pid,
                    "stix_incident_id": f"incident--acceptance-{_slug(host)}",
                    "workflow_ids": [wid],
                },
            ),
            label=f"create project {pid}",
        )
    else:
        body = _require_ok(existing, label=f"get project {pid}")
        wids = list(body.get("workflow_ids") or [])
        if wid not in wids:
            wids.append(wid)
            _require_ok(
                api.request(
                    "PATCH",
                    f"/projects/{pid}",
                    json={"workflow_ids": wids},
                ),
                label=f"update project {pid}",
            )


def assert_api_queryable(api: AcceptanceApi, ids: Dict[str, str]) -> Dict[str, Any]:
    """R10-30: project / workflow / step list / context JSON are queryable."""
    tid, wid, pid = ids["target_id"], ids["workflow_id"], ids["project_id"]

    target = assert_queryable_json(
        _require_ok(api.request("GET", f"/targets/{tid}"), label=f"GET target {tid}"),
        label="target",
    )
    workflow = assert_queryable_json(
        _require_ok(
            api.request("GET", f"/workflows/{wid}", params={"projection": "true"}),
            label=f"GET workflow {wid}",
        ),
        label="workflow",
    )
    project = assert_queryable_json(
        _require_ok(api.request("GET", f"/projects/{pid}"), label=f"GET project {pid}"),
        label="project",
    )
    steps = _require_ok(api.request("GET", "/scan-steps"), label="GET scan-steps")
    if not isinstance(steps, list):
        raise AcceptanceError("scan-steps list must be a JSON array")
    temporary = assert_queryable_json(
        _require_ok(
            api.request("GET", f"/projects/{pid}/contexts/temporary"),
            label="GET temporary context",
        ),
        label="temporary_context",
    )
    project_ctx = assert_queryable_json(
        _require_ok(
            api.request("GET", f"/projects/{pid}/contexts/project"),
            label="GET project context",
        ),
        label="project_context",
    )
    return {
        "target": target,
        "workflow": workflow,
        "project": project,
        "scan_steps": steps,
        "temporary_context": temporary,
        "project_context": project_ctx,
    }


def seed_synthetic_scan_step(api: InProcessApi, *, workflow_id: str, host: str) -> str:
    """Plant a connected four-form scan_step so dry-run still exercises R10-30 asserts."""
    from modules_v2._core.graph_builder import nugget_node

    scan_id = scan_instance_id_for(workflow_id, "sfp_cli_subfinder")
    domain = nugget_node("DOMAIN_NAME", host)
    parent = nugget_node("DOMAIN_NAME_PARENT", host)
    # Link domain → had → parent so neither node is an orphan.
    graph = {
        "nodes": [domain, parent],
        "edges": [
            {
                "id": f"edge--{uuid.uuid5(uuid.NAMESPACE_DNS, host + '|had')}",
                "source": domain["id"],
                "target": parent["id"],
                "reln": "had",
            }
        ],
    }
    assert_graph_invariants(graph, label="synthetic_seed")
    api.crud.scan_steps[scan_id] = {
        "scan_instance_id": scan_id,
        "step_module_id": "sfp_cli_subfinder",
        "scan_status": "FINISHED",
        "scan_ui_cli_command": f"subfinder -d {host} -oJ -silent",
        "scan_ui_text_form": f"{host}\n",
        "scan_ui_structured_form": json.dumps(
            {"host": host, "records": [{"host": host}]}, indent=2
        ),
        "scan_ui_structured_form_type": "json",
        "scan_ui_graph_form": json.dumps(graph),
        "scan_ui_markdown_narrative_form": (
            f"# Acceptance dry-run seed\n\nSynthetic four-form artifact for `{host}`.\n"
        ),
        "consumed_ids": [],
        "produced_ids": [],
        "scan_result_graph_ids": [],
    }
    return scan_id


def execute_workflow(
    api: AcceptanceApi,
    *,
    workflow_id: str,
    project_id: str,
    dry_run: bool,
) -> Dict[str, Any]:
    body = _require_ok(
        api.request(
            "POST",
            f"/workflows/{workflow_id}/execute",
            json={"project_id": project_id, "dry_run": dry_run},
        ),
        label=f"execute workflow {workflow_id}",
    )
    assert_queryable_json(body, label="execute_response")
    return body


def assert_execute_outcome(body: Mapping[str, Any], *, dry_run: bool) -> None:
    status = body.get("status")
    if dry_run:
        if status != "DRY_RUN":
            raise AcceptanceError(
                f"dry-run expected status DRY_RUN, got {status!r}: {body.get('message')}"
            )
        return
    if status not in ("SUCCESS",):
        raise AcceptanceError(
            f"live run expected SUCCESS, got {status!r}: "
            f"{body.get('error') or body.get('message')}"
        )


def collect_scan_steps_from_execute(
    api: AcceptanceApi, execute_body: Dict[str, Any]
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for step in execute_body.get("steps") or []:
        sid = step.get("scan_instance_id")
        if not sid:
            continue
        # Dry-run does not persist; skip missing.
        resp = api.request("GET", f"/scan-steps/{sid}")
        if resp.status_code == 404:
            continue
        out.append(
            assert_queryable_json(
                _require_ok(resp, label=f"GET scan-step {sid}"),
                label=f"scan_step {sid}",
            )
        )
    return out


def assert_live_scan_artifacts(steps: Sequence[Dict[str, Any]]) -> None:
    if not steps:
        raise AcceptanceError(
            "live run produced no queryable scan_steps with four forms"
        )
    for step in steps:
        # Only assert forms for finished / successful persisted steps.
        status = step.get("scan_status")
        if status and status not in ("FINISHED", "SUCCESS", None):
            continue
        if not any(step.get(k) for k in ("text_form", "graph_form", "structured_form")):
            continue
        assert_scan_step_artifacts(step, require_forms=True)


def write_evidence(
    evidence_dir: Path,
    *,
    host: str,
    dry_run: bool,
    execute_body: Dict[str, Any],
    queryable: Dict[str, Any],
    scan_steps: List[Dict[str, Any]],
) -> Path:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    mode = "dry_run" if dry_run else "live"
    path = evidence_dir / f"{_slug(host)}_{mode}_{stamp}.json"
    payload = {
        "schema": "spiderfeet_v2_acceptance_v1",
        "host": host,
        "documented_target": is_documented(host),
        "dry_run": dry_run,
        "ap1_complete": False,  # AP2 must never claim AP1 / G3
        "generated_at": stamp,
        "execute": execute_body,
        "queryable": {
            "target": queryable.get("target"),
            "workflow": {
                k: queryable.get("workflow", {}).get(k)
                for k in ("workflow_id", "target", "first_step")
            },
            "project": {
                k: queryable.get("project", {}).get(k)
                for k in ("project_id", "workflows", "targets", "stix_incident_id")
            },
            "temporary_context": queryable.get("temporary_context"),
            "project_context": queryable.get("project_context"),
        },
        "scan_steps": scan_steps,
        "documented_targets": DOCUMENTED_TARGETS,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def run_one(
    api: AcceptanceApi,
    *,
    host: str,
    dry_run: bool,
    workflow_yaml_path: Path,
    evidence_dir: Optional[Path],
) -> Dict[str, Any]:
    ids = _ids_for(host)
    yaml_text = load_workflow_yaml_for_target(
        host,
        workflow_yaml_path=workflow_yaml_path,
        workflow_id=ids["workflow_id"],
    )
    ensure_project_stack(api, host=host, workflow_yaml=yaml_text, ids=ids)
    execute_body = execute_workflow(
        api,
        workflow_id=ids["workflow_id"],
        project_id=ids["project_id"],
        dry_run=dry_run,
    )
    assert_execute_outcome(execute_body, dry_run=dry_run)

    queryable = assert_api_queryable(api, ids)
    scan_steps = collect_scan_steps_from_execute(api, execute_body)

    if dry_run and isinstance(api, InProcessApi):
        # Dry-run does not persist four forms; seed one connected artifact so
        # R10-30 graph/four-form validators still run without AP1/G3 live scans.
        seeded_id = seed_synthetic_scan_step(
            api, workflow_id=ids["workflow_id"], host=host
        )
        resp = api.request("GET", f"/scan-steps/{seeded_id}")
        seeded = assert_queryable_json(
            _require_ok(resp, label=f"GET seeded scan-step {seeded_id}"),
            label="seeded_scan_step",
        )
        assert_scan_step_artifacts(seeded, require_forms=True)
        scan_steps = [seeded]
    elif not dry_run:
        assert_live_scan_artifacts(scan_steps)
        # Also validate temporary context graph when present.
        temp = queryable.get("temporary_context") or {}
        graph = temp.get("nodes") is not None and {
            "nodes": temp.get("nodes") or [],
            "edges": temp.get("edges") or [],
        }
        if graph and (graph["nodes"] or graph["edges"]):
            assert_graph_invariants(graph, label="temporary_context")
        elif temp.get("graph"):
            assert_graph_invariants(
                parse_graph_form(temp.get("graph")), label="temporary_context"
            )

    evidence_path: Optional[Path] = None
    if evidence_dir is not None:
        evidence_path = write_evidence(
            evidence_dir,
            host=host,
            dry_run=dry_run,
            execute_body=execute_body,
            queryable=queryable,
            scan_steps=scan_steps,
        )

    return {
        "host": host,
        "ids": ids,
        "dry_run": dry_run,
        "execute_status": execute_body.get("status"),
        "step_count": execute_body.get("step_count"),
        "waves": execute_body.get("waves"),
        "scan_steps_checked": len(scan_steps),
        "evidence": str(evidence_path) if evidence_path else None,
        "documented_target": is_documented(host),
    }


def build_api(*, in_process: bool, base_url: str) -> AcceptanceApi:
    if in_process:
        return build_inprocess_api()
    return HttpxApi(base_url=base_url)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "SPEC-010 AP2 acceptance harness (R10-30). "
            "Default: dry-run in-process (no G3 / AP1 required)."
        )
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Host to run (repeatable). Defaults to documented four when --all.",
    )
    g.add_argument(
        "--all",
        action="store_true",
        help="Run all documented R10-29 targets "
        f"({', '.join(DEFAULT_TARGETS)}).",
    )
    p.add_argument(
        "--live",
        action="store_true",
        help="Execute live scans (requires running API + CLI tools). Not G3 sign-off.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Force dry-run (default when --live is absent).",
    )
    p.add_argument(
        "--in-process",
        action="store_true",
        help="Use FastAPI TestClient + in-memory stores (default for dry-run).",
    )
    p.add_argument(
        "--remote",
        action="store_true",
        help="Use --base-url even for dry-run (requires reachable API).",
    )
    p.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"v2 API base (default: {DEFAULT_BASE_URL})",
    )
    p.add_argument(
        "--workflow-yaml",
        type=Path,
        default=DEFAULT_WORKFLOW_YAML,
        help="Path to 12A (or compatible) workflow YAML.",
    )
    p.add_argument(
        "--evidence-dir",
        type=Path,
        default=DEFAULT_EVIDENCE_DIR,
        help="Directory for JSON evidence bundles (use --no-evidence to skip).",
    )
    p.add_argument(
        "--no-evidence",
        action="store_true",
        help="Do not write evidence JSON.",
    )
    p.add_argument(
        "--list-targets",
        action="store_true",
        help="Print documented targets and exit.",
    )
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.list_targets:
        for row in DOCUMENTED_TARGETS:
            print(f"{row['host']}\t{row['note']}")
        return 0

    if args.all:
        hosts = list(DEFAULT_TARGETS)
    elif args.targets:
        hosts = [normalize_host(t) for t in args.targets]
    else:
        # Plan verify: --target <one>. If omitted, run first documented target.
        hosts = [DEFAULT_TARGETS[0]]
        print(
            f"note: no --target/--all; defaulting to {hosts[0]} "
            "(use --all for the documented four)",
            file=sys.stderr,
        )

    dry_run = not args.live
    if args.dry_run:
        dry_run = True
    if args.live and args.dry_run:
        print("error: --live and --dry-run are mutually exclusive", file=sys.stderr)
        return 2

    in_process = args.in_process
    if dry_run and not args.remote and not args.in_process:
        # Prefer in-process dry-run so AP2 verify works without AN1 G2 / live API.
        in_process = True
    if args.remote:
        in_process = False
    if args.live:
        in_process = False
        if not api_reachable(args.base_url):
            print(
                f"error: --live requires a reachable API at {args.base_url}",
                file=sys.stderr,
            )
            return 2

    if not args.workflow_yaml.is_file():
        print(f"error: workflow YAML not found: {args.workflow_yaml}", file=sys.stderr)
        return 2

    evidence_dir: Optional[Path] = None if args.no_evidence else args.evidence_dir
    api = build_api(in_process=in_process, base_url=args.base_url)
    results: List[Dict[str, Any]] = []
    errors: List[str] = []
    try:
        mode = "dry-run/in-process" if (dry_run and in_process) else (
            "dry-run/remote" if dry_run else "live/remote"
        )
        print(f"acceptance harness mode={mode} base={args.base_url if not in_process else 'in-process'}")
        print(f"targets: {', '.join(hosts)}")
        print("note: AP2 only — does not claim AP1 / G3 complete")
        for host in hosts:
            try:
                summary = run_one(
                    api,
                    host=host,
                    dry_run=dry_run,
                    workflow_yaml_path=args.workflow_yaml,
                    evidence_dir=evidence_dir,
                )
                results.append(summary)
                print(
                    f"OK  {host}: status={summary['execute_status']} "
                    f"steps={summary['step_count']} "
                    f"checked={summary['scan_steps_checked']}"
                    + (
                        f" evidence={summary['evidence']}"
                        if summary.get("evidence")
                        else ""
                    )
                )
            except AcceptanceError as exc:
                errors.append(f"{host}: {exc}")
                print(f"FAIL {host}: {exc}", file=sys.stderr)
            except Exception as exc:  # noqa: BLE001 — surface harness faults
                errors.append(f"{host}: {type(exc).__name__}: {exc}")
                print(f"FAIL {host}: {type(exc).__name__}: {exc}", file=sys.stderr)
    finally:
        api.close()

    if errors:
        print(f"\n{len(errors)} target(s) failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"\nPASS: {len(results)} target(s) satisfied R10-30 assertions ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
