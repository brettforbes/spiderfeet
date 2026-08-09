#!/usr/bin/env python3
"""B3-2 / R13-08 — verify SPEC-013 seed projects on spiderfeet-actual."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spiderfeet_v2.db.bootstrap import ACTUAL_DATABASE_NAME
from spiderfeet_v2.db.config import load_connection_config
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.workflow.seed_projects import (
    SEED_SPECS,
    seed_project_id,
    seed_workflow_id,
)

EXPECTED_12A = {
    "sfp_cli_subfinder",
    "sfp_cli_nmap",
    "sfp_cli_nerva",
    "sfp_cli_httpx",
    "sfp_cli_katana",
    "sfp_cli_nuclei",
}


def main() -> int:
    cfg = load_connection_config()
    store = CrudStore(cfg=cfg, database=ACTUAL_DATABASE_NAME)
    projects = store.list_projects()
    seed_pids = {seed_project_id(s.key) for s in SEED_SPECS}
    seeded = [p for p in projects if p["project_id"] in seed_pids]
    print(f"database={ACTUAL_DATABASE_NAME}")
    print(f"total_projects={len(projects)} seed_projects={len(seeded)}")
    if len(seeded) != 5:
        print(f"FAIL: expected 5 seed projects, got {len(seeded)}")
        return 1

    for spec in SEED_SPECS:
        pid = seed_project_id(spec.key)
        wid = seed_workflow_id(spec.key)
        p = store.get_project(pid)
        w = store.get_workflow(wid)
        assert p is not None and w is not None, (pid, wid)
        assert wid in (p.get("workflow_ids") or [])
        step_ids = set(w.get("prior_step_ids") or []) | set(
            w.get("next_step_ids") or []
        )
        if w.get("first_step_id"):
            step_ids.add(w["first_step_id"])
        modules = []
        result_hits = []
        for sid in sorted(step_ids):
            st = store.get_scan_step(sid)
            assert st is not None, sid
            modules.append(st.get("step_module_id"))
            if (
                st.get("scan_ui_text_form")
                or st.get("scan_ui_graph_form")
                or st.get("scan_results")
            ):
                result_hits.append(sid)
        print("---")
        print(f"key={spec.key}")
        print(f"project={p['project_id']} name={p.get('project_name')}")
        print(f"workflow={w['workflow_id']} target_id={w.get('target_id')}")
        print(f"steps={len(step_ids)} modules={modules}")
        print(f"result_hits={result_hits}")
        if spec.template == "12A2":
            assert len(step_ids) == 1
            assert modules == ["sfp_cli_netdiscover"]
            assert not w.get("target_id")
            yaml_head = (w.get("workflow_yaml") or "").split("steps:")[0]
            assert "inputs:" not in yaml_head
        else:
            assert len(step_ids) == 6
            assert set(modules) == EXPECTED_12A
            assert w.get("target_id")
            t = store.get_target(w["target_id"])
            assert t["target_value"] == f"https://{spec.input_host}"
            assert w.get("first_step_id")
            assert w.get("prior_step_ids")
            assert w.get("next_step_ids")
        assert not result_hits, result_hits

    print("VERIFIED_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
