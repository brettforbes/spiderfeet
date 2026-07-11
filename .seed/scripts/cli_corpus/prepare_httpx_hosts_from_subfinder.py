#!/usr/bin/env python3
"""Extract host lists from subfinder examination bundles for httpx input."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SUBFINDER_EXAM = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/subfinder"
HOST_OUT = REPO_ROOT / ".docs/docs-for-cli-tools/exploration_scratch/httpx/hosts"

# httpx scenario_id -> subfinder scenario_id
PIPELINE_MAP: dict[str, str] = {
    "from_subfinder_upside_au": "corporate_upside_au_passive_cs",
    "from_subfinder_squarepeg": "corporate_squarepeg_passive_cs",
    "from_subfinder_vcof_sparse": "corporate_vcof_sparse_passive",
    "from_subfinder_k2am_passive": "corporate_k2am_passive_cs",
    "from_subfinder_k2am_active": "corporate_k2am_active_oI",
    "from_subfinder_upside_com": "corporate_upside_com_passive_cs",
    "from_subfinder_sbs": "enterprise_sbs_passive_cs",
    "from_subfinder_invalid_clean_miss": "invalid_domain_clean_miss",
}


def load_subfinder_hosts(subfinder_scenario_id: str) -> list[str]:
    for manifest_path in sorted(SUBFINDER_EXAM.glob("*_manifest.json")):
        meta = json.loads(manifest_path.read_text(encoding="utf-8"))
        if meta.get("scenario_id") != subfinder_scenario_id:
            continue
        prefix = manifest_path.name.replace("_manifest.json", "")
        struct_path = SUBFINDER_EXAM / f"{prefix}_output_structured.json"
        doc = json.loads(struct_path.read_text(encoding="utf-8"))
        hosts = sorted(
            {
                str(rec.get("host", "")).strip().lower().rstrip(".")
                for rec in doc.get("records", [])
                if str(rec.get("host", "")).strip()
            }
        )
        return hosts
    raise FileNotFoundError(f"No subfinder examination for scenario {subfinder_scenario_id!r}")


def write_host_file(httpx_scenario_id: str, hosts: list[str]) -> Path:
    HOST_OUT.mkdir(parents=True, exist_ok=True)
    out = HOST_OUT / f"{httpx_scenario_id}_hosts.txt"
    if hosts:
        out.write_text("\n".join(hosts) + "\n", encoding="utf-8")
    else:
        # Placeholder for clean-miss httpx run (invalid apex)
        out.write_text("not-a-real-domain-xyzzy.invalid\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare httpx host lists from subfinder exams")
    parser.add_argument("--scenario", help="httpx scenario id only")
    args = parser.parse_args()
    items = PIPELINE_MAP.items()
    if args.scenario:
        if args.scenario not in PIPELINE_MAP:
            raise SystemExit(f"Unknown httpx scenario: {args.scenario}")
        items = [(args.scenario, PIPELINE_MAP[args.scenario])]
    summary: list[dict[str, object]] = []
    for httpx_id, subfinder_id in items:
        hosts = load_subfinder_hosts(subfinder_id)
        path = write_host_file(httpx_id, hosts)
        summary.append(
            {"httpx_scenario": httpx_id, "subfinder_scenario": subfinder_id, "host_count": len(hosts), "path": str(path.relative_to(REPO_ROOT))}
        )
        print(f"{httpx_id}: {len(hosts)} hosts -> {path.relative_to(REPO_ROOT)}")
    index_path = HOST_OUT / "pipeline_index.json"
    index_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
