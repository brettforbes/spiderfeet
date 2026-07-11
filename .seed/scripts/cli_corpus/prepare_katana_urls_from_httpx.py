#!/usr/bin/env python3
"""Extract seed URL lists from httpx examination bundles for katana input."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HTTPX_EXAM = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/httpx"
URL_OUT = REPO_ROOT / ".docs/docs-for-cli-tools/exploration_scratch/katana/urls"

# katana scenario_id -> httpx scenario_id (1:1 with httpx examination matrix)
PIPELINE_MAP: dict[str, str] = {
    "from_httpx_upside_au": "from_subfinder_upside_au",
    "from_httpx_squarepeg": "from_subfinder_squarepeg",
    "from_httpx_vcof_sparse": "from_subfinder_vcof_sparse",
    "from_httpx_k2am_passive": "from_subfinder_k2am_passive",
    "from_httpx_k2am_active": "from_subfinder_k2am_active",
    "from_httpx_upside_com": "from_subfinder_upside_com",
    "from_httpx_sbs": "from_subfinder_sbs",
    "from_httpx_invalid_clean_miss": "from_subfinder_invalid_clean_miss",
}


def load_httpx_urls(httpx_scenario_id: str) -> list[str]:
    for manifest_path in sorted(HTTPX_EXAM.glob("*_manifest.json")):
        meta = json.loads(manifest_path.read_text(encoding="utf-8"))
        if meta.get("scenario_id") != httpx_scenario_id:
            continue
        prefix = manifest_path.name.replace("_manifest.json", "")
        struct_path = HTTPX_EXAM / f"{prefix}_output_structured.json"
        doc = json.loads(struct_path.read_text(encoding="utf-8"))
        seen: set[str] = set()
        urls: list[str] = []
        for rec in doc.get("records", []):
            if rec.get("failed"):
                continue
            url = str(rec.get("url") or "").strip()
            if not url or url in seen:
                continue
            seen.add(url)
            urls.append(url)
        return urls
    raise FileNotFoundError(f"No httpx examination for scenario {httpx_scenario_id!r}")


def write_url_file(katana_scenario_id: str, urls: list[str]) -> Path:
    out = URL_OUT / f"{katana_scenario_id}_urls.txt"
    if urls:
        out.write_text("\n".join(urls) + "\n", encoding="utf-8")
    else:
        out.write_text("", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare katana seed URL lists from httpx exams")
    parser.add_argument("--scenario", help="katana scenario id only")
    args = parser.parse_args()
    URL_OUT.mkdir(parents=True, exist_ok=True)
    EXAM_OUT = REPO_ROOT / ".docs/docs-for-cli-tools/exploration_scratch/katana/exams"
    EXAM_OUT.mkdir(parents=True, exist_ok=True)
    items = PIPELINE_MAP.items()
    if args.scenario:
        if args.scenario not in PIPELINE_MAP:
            raise SystemExit(f"Unknown katana scenario: {args.scenario}")
        items = [(args.scenario, PIPELINE_MAP[args.scenario])]
    summary: list[dict[str, object]] = []
    for katana_id, httpx_id in items:
        urls = load_httpx_urls(httpx_id)
        path = write_url_file(katana_id, urls)
        summary.append(
            {
                "katana_scenario": katana_id,
                "httpx_scenario": httpx_id,
                "url_count": len(urls),
                "path": str(path.relative_to(REPO_ROOT)),
            }
        )
        print(f"{katana_id}: {len(urls)} urls (from {httpx_id}) -> {path.relative_to(REPO_ROOT)}")
    index_path = URL_OUT / "pipeline_index.json"
    index_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
