#!/usr/bin/env python3
"""Backfill modules_v2/content/<tool_id>/ bundles for all 8 adapter tools (V2)."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CLI_DOCS = REPO_ROOT / ".docs" / "docs-for-cli-tools"
NUGGET_ROOT = CLI_DOCS / "nugget_structure"
CONTENT_ROOT = REPO_ROOT / "modules_v2" / "content"

BUNDLES: dict[str, dict[str, str]] = {
    "nmap": {
        "options": "NMAP-CLI-Options.md",
        "zero_to_hero": "NMAP-Zero-to-Hero.md",
        "display_name": "Nmap",
        "executable": "nmap",
        "category": "network_scanner",
    },
    "netdiscover": {
        "options": "NetDiscover-CLI-Options.md",
        "zero_to_hero": "NetDiscover-Zero-to-Hero.md",
        "display_name": "Netdiscover",
        "executable": "netdiscover",
        "category": "network_discovery",
    },
    "nerva": {
        "options": "Nerva-CLI-Options.md",
        "zero_to_hero": "Nerva-Zero-to-Hero.md",
        "display_name": "Nerva",
        "executable": "nerva",
        "category": "service_fingerprint",
    },
    "pius": {
        "options": "PIUS-CLI-Options.md",
        "zero_to_hero": "PIUS-Zero-to-Hero.md",
        "display_name": "Pius",
        "executable": "pius",
        "category": "org_intelligence",
    },
    "subfinder": {
        "options": "SubFinder-CLI-Options.md",
        "zero_to_hero": "SubFinder-Zero-to-Hero.md",
        "display_name": "Subfinder",
        "executable": "subfinder",
        "category": "subdomain_enum",
    },
    "httpx": {
        "options": "Httpx-CLI-Options.md",
        "zero_to_hero": "Httpx-Zero-to-Hero.md",
        "display_name": "Httpx",
        "executable": "httpx",
        "category": "http_probe",
    },
    "katana": {
        "options": "katana-CLI-Options.md",
        "zero_to_hero": "katana-Zero-to-Hero.md",
        "display_name": "Katana",
        "executable": "katana",
        "category": "web_crawl",
    },
    "nuclei": {
        "options": "Nuclei-CLI-Options.md",
        "zero_to_hero": "Nuclei-Zero-to-Hero.md",
        "display_name": "Nuclei",
        "executable": "nuclei",
        "category": "vulnerability_scan",
    },
}


def copy_bundle(tool_id: str, meta: dict[str, str]) -> None:
    dest = CONTENT_ROOT / tool_id
    dest.mkdir(parents=True, exist_ok=True)

    for src_name, dest_name in (
        (meta["options"], "options.md"),
        (meta["zero_to_hero"], "zero_to_hero.md"),
    ):
        src = CLI_DOCS / src_name
        shutil.copy2(src, dest / dest_name)

    graph_src = NUGGET_ROOT / f"{tool_id}_nugget_graph_structure.md"
    shutil.copy2(graph_src, dest / "graph_structure.md")

    manifest = {
        "tool_id": tool_id,
        "display_name": meta["display_name"],
        "kind": "cli",
        "category": meta["category"],
        "executable": meta["executable"],
        "content_version": 1,
        "source_docs": {
            "options": f".docs/docs-for-cli-tools/{meta['options']}",
            "zero_to_hero": f".docs/docs-for-cli-tools/{meta['zero_to_hero']}",
            "graph_structure": f".docs/docs-for-cli-tools/nugget_structure/{tool_id}_nugget_graph_structure.md",
        },
    }
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    gen_script = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "generate_options_schema.py"
    subprocess.run(
        [sys.executable, str(gen_script), "--tool", tool_id, "--output-dir", str(dest)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", help="Single tool id; default all 8")
    args = parser.parse_args()
    tools = [args.tool] if args.tool else list(BUNDLES)
    for tool_id in tools:
        if tool_id not in BUNDLES:
            print(f"Unknown tool: {tool_id}", file=sys.stderr)
            return 2
        copy_bundle(tool_id, BUNDLES[tool_id])
        print(f"Backfilled {tool_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
