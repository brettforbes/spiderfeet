#!/usr/bin/env python3
"""One-off dedupe: canonical CLI help + nmap graph format variants."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DOCS = REPO / ".docs" / "docs-for-cli-tools"
NUGGET = DOCS / "nugget_structure"
CLI_HELP = DOCS / "cli_help_text"

NMAP_BASES = [
    "capstone_permissive",
    "host_discovery_corporate",
    "host_discovery_local_subnet",
    "host_discovery_permissive",
    "nse_default_permissive",
    "os_aggressive_permissive",
    "service_version_corporate",
    "service_version_permissive",
    "skip_ping_permissive",
    "tcp_top_ports_corporate",
    "tcp_top_ports_local",
    "tcp_top_ports_permissive",
    "traceroute_permissive",
    "udp_top_permissive",
    "windows_enrich_local",
]


def consolidate_nmap_xml_variants() -> list[str]:
    actions: list[str] = []
    for base in NMAP_BASES:
        canonical_graph = NUGGET / f"nmap_{base}_proposed_nuggets_edges.json"
        canonical_md = NUGGET / f"nmap_{base}_proposed_nuggets_edges_description.md"
        xml_graph = NUGGET / f"nmap_{base}_xml_proposed_nuggets_edges.json"
        xml_md = NUGGET / f"nmap_{base}_xml_proposed_nuggets_edges_description.md"

        if not xml_graph.is_file():
            continue

        canonical_graph.write_text(xml_graph.read_text(encoding="utf-8"), encoding="utf-8")
        actions.append(f"promote xml graph -> {canonical_graph.name}")

        if xml_md.is_file():
            canonical_md.write_text(xml_md.read_text(encoding="utf-8"), encoding="utf-8")
            actions.append(f"promote xml narrative -> {canonical_md.name}")

        for path in (xml_graph, xml_md):
            if path.is_file():
                path.unlink()
                actions.append(f"deleted {path.name}")
    return actions


def remove_cli_help_text_dir() -> list[str]:
    actions: list[str] = []
    if not CLI_HELP.is_dir():
        return actions
    for path in sorted(CLI_HELP.iterdir()):
        if path.is_file():
            path.unlink()
            actions.append(f"deleted {path.relative_to(REPO)}")
    CLI_HELP.rmdir()
    actions.append("removed cli_help_text/")
    return actions


def remove_nmap_text_examination_bundles() -> list[str]:
    """Drop legacy text-only nmap captures; XML bundles retain derived text."""
    actions: list[str] = []
    tool_dir = DOCS / "app_examination_docs" / "nmap"
    if not tool_dir.is_dir():
        return actions
    import json

    for manifest_path in sorted(tool_dir.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sid = manifest.get("scenario_id") or ""
        if not sid.endswith("_text"):
            continue
        exam_id = manifest_path.name.split("_", 1)[0]
        for path in sorted(tool_dir.glob(f"{exam_id}_*")):
            path.unlink()
            actions.append(f"deleted {path.relative_to(REPO)}")
    return actions


def remove_orphan_exam_graphs() -> list[str]:
    actions: list[str] = []
    for name in (
        "17_adapter_proposed_nuggets_edges.json",
        "17_adapter_proposed_nuggets_edges_description.md",
    ):
        path = DOCS / "app_examination_docs" / "nmap" / name
        if path.is_file():
            path.unlink()
            actions.append(f"deleted {path.relative_to(REPO)}")
    return actions


def main() -> None:
    all_actions: list[str] = []
    all_actions.extend(consolidate_nmap_xml_variants())
    all_actions.extend(remove_nmap_text_examination_bundles())
    all_actions.extend(remove_orphan_exam_graphs())
    all_actions.extend(remove_cli_help_text_dir())
    for line in all_actions:
        print(line)
    print(f"done ({len(all_actions)} actions)")


if __name__ == "__main__":
    main()
