"""Idempotent seed of 5 SPEC-013 projects (R13-07 / B3-1).

Project 1: 12A2 (netdiscover, no inputs/target).
Projects 2–5: 12A clones with distinct targets/names.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid5

import yaml

from spiderfeet_v2.db.bootstrap import ACTUAL_DATABASE_NAME
from spiderfeet_v2.db.config import load_connection_config
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.workflow.typedb_convert import (
    _delete_workflow_bundle,
    persist_workflow_yaml,
)

ROOT = Path(__file__).resolve().parents[2]
SEED_NS = UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
TEMPLATE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
TEMPLATE_12A2 = ROOT / ".seed" / "12A2_Workflow_YAML_Example.yaml"


@dataclass(frozen=True)
class SeedSpec:
    key: str
    project_name: str
    project_description: str
    template: str  # "12A2" | "12A"
    input_host: Optional[str] = None


SEED_SPECS: List[SeedSpec] = [
    SeedSpec(
        key="simple-wireless",
        project_name="Simple Wireless Scan",
        project_description=(
            "Simple local-network wireless/ARP discovery scan"
        ),
        template="12A2",
    ),
    SeedSpec(
        key="recon-sbs",
        project_name="Attack Surface Recon — www.sbs.com.au",
        project_description="Twin-fork attack-surface recon of www.sbs.com.au",
        template="12A",
        input_host="www.sbs.com.au",
    ),
    SeedSpec(
        key="recon-k2am",
        project_name="Attack Surface Recon — www.k2am.com.au",
        project_description="Twin-fork attack-surface recon of www.k2am.com.au",
        template="12A",
        input_host="www.k2am.com.au",
    ),
    SeedSpec(
        key="recon-vcopportunities",
        project_name=(
            "Attack Surface Recon — www.venturecapitalopportunitiesfund.com.au"
        ),
        project_description=("Twin-fork attack-surface recon of that domain"),
        template="12A",
        input_host="www.venturecapitalopportunitiesfund.com.au",
    ),
    SeedSpec(
        key="recon-squarepeg",
        project_name="Attack Surface Recon — www.squarepeg.vc",
        project_description="Twin-fork attack-surface recon of www.squarepeg.vc",
        template="12A",
        input_host="www.squarepeg.vc",
    ),
]


def seed_project_id(key: str) -> str:
    return f"project--{uuid5(SEED_NS, f'project:{key}')}"


def seed_workflow_id(key: str) -> str:
    return f"workflow--{uuid5(SEED_NS, f'workflow:{key}')}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _load_template(template: str) -> Dict[str, Any]:
    path = TEMPLATE_12A2 if template == "12A2" else TEMPLATE_12A
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"template root must be a mapping: {path}")
    return doc


def build_seed_workflow_doc(spec: SeedSpec) -> Dict[str, Any]:
    """Clone template YAML with stable ids + project-facing info/target."""
    doc = copy.deepcopy(_load_template(spec.template))
    wid = seed_workflow_id(spec.key)
    doc["id"] = wid
    info = dict(doc.get("info") or {})
    info["name"] = spec.project_name
    info["description"] = spec.project_description
    info.setdefault("author", "spiderfeet")
    info.setdefault("created", _now_iso())
    doc["info"] = info
    if spec.template == "12A":
        if not spec.input_host:
            raise ValueError(f"12A seed {spec.key} requires input_host")
        inputs = dict(doc.get("inputs") or {})
        targets = dict(inputs.get("targets") or {})
        targets["type"] = "string_list"
        targets["values"] = [f"https://{spec.input_host}"]
        inputs["targets"] = targets
        doc["inputs"] = inputs
    else:
        doc.pop("inputs", None)
    return doc


def _purge_project(store: Any, project_id: str) -> None:
    row = store.get_project(project_id)
    if row is None:
        return
    for wid in list(row.get("workflow_ids") or []):
        _delete_workflow_bundle(store, wid)
    store.delete_project(project_id)


def seed_one(store: Any, spec: SeedSpec, *, replace: bool = True) -> Dict[str, Any]:
    """Materialize one seed project + workflow (no scan results)."""
    pid = seed_project_id(spec.key)
    wid = seed_workflow_id(spec.key)
    doc = build_seed_workflow_doc(spec)

    existing = store.get_project(pid)
    if existing is not None:
        if not replace:
            return {
                "project_id": pid,
                "workflow_id": wid,
                "skipped": True,
                "project_name": existing.get("project_name"),
            }
        _purge_project(store, pid)

    store.create_project(
        {
            "project_id": pid,
            "project_name": spec.project_name,
            "project_description": spec.project_description,
            "project_created": _now_iso(),
            "workflow_ids": [],
        }
    )
    forms = persist_workflow_yaml(
        store,
        doc,
        validate=True,
        replace=True,
        project_id=pid,
    )
    project = store.get_project(pid)
    return {
        "project_id": pid,
        "workflow_id": forms.workflow_id,
        "project_name": spec.project_name,
        "template": spec.template,
        "input_host": spec.input_host,
        "step_count": len(forms.steps),
        "has_target": forms.target is not None,
        "workflow_ids": (project or {}).get("workflow_ids") or [wid],
        "skipped": False,
    }


def seed_all(store: Any, *, replace: bool = True) -> List[Dict[str, Any]]:
    return [seed_one(store, spec, replace=replace) for spec in SEED_SPECS]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Idempotent seed of 5 SPEC-013 projects into spiderfeet-actual "
            "(R13-07 / B3-1)."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build docs and print planned ids without writing TypeDB",
    )
    parser.add_argument(
        "--no-replace",
        action="store_true",
        help="Skip seeds whose project_id already exists",
    )
    parser.add_argument(
        "--database",
        default=ACTUAL_DATABASE_NAME,
        help=f"TypeDB database (default: {ACTUAL_DATABASE_NAME})",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        for spec in SEED_SPECS:
            doc = build_seed_workflow_doc(spec)
            print(
                f"{spec.key}: project={seed_project_id(spec.key)} "
                f"workflow={doc['id']} template={spec.template} "
                f"steps={len(doc.get('steps') or [])} "
                f"input={spec.input_host or '-'}"
            )
        return 0

    cfg = load_connection_config()
    database = args.database or ACTUAL_DATABASE_NAME
    store = CrudStore(cfg=cfg, database=database)
    results = seed_all(store, replace=not args.no_replace)
    for row in results:
        status = "skipped" if row.get("skipped") else "seeded"
        print(
            f"{status}: {row['project_name']} "
            f"({row['project_id']}) workflow={row['workflow_id']} "
            f"steps={row.get('step_count', '?')} target={row.get('has_target')}"
        )
    print(f"done: {len(results)} seed rows against {database}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
