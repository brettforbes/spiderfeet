"""P0 acceptance: sketch gap notes inventory is complete."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = ROOT / ".governance" / "project" / "SPEC007_SKETCH_GAP_NOTES.md"
SEED_12B = ROOT / ".seed" / "12B_Workflow_DSL_Description.md"


def test_gap_notes_file_exists():
    assert GAP.is_file()


def test_gap_notes_lists_required_sketch_defects():
    text = GAP.read_text(encoding="utf-8")
    required = [
        "concat({{IP_ADDRESS}}",
        "SUBDOMAIN",
        "sum({{domains}}",
        "sequence:",
        "sfp_",
        "cli_options",
        "ip_port_list",
        "all_domains",
    ]
    for token in required:
        assert token in text, f"missing gap note for: {token}"


def test_12b_links_gap_notes():
    text = SEED_12B.read_text(encoding="utf-8")
    assert "SPEC007_SKETCH_GAP_NOTES.md" in text


def test_gap_notes_per_step_table_covers_six_tools():
    text = GAP.read_text(encoding="utf-8")
    for step in (
        "subfinder_enum",
        "nmap_ports",
        "nerva_services",
        "httpx_live",
        "katana_crawl",
        "nuclei_vulns",
    ):
        assert step in text
