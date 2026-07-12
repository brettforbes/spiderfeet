"""SPEC-004 D7 visual review checklist artifact checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = REPO_ROOT / ".governance" / "project" / "SPEC004_VISUAL_REVIEW_CHECKLIST.md"


def test_visual_review_checklist_exists_with_required_sections():
    text = CHECKLIST.read_text(encoding="utf-8")

    assert "R4-01-08" in text
    assert "Do **not** lock golden" in text
    assert "## Per-tool review matrix" in text
    assert "## Refinement follow-ups" in text
    assert "## Sign-off" in text
    for tool in ("netdiscover", "nmap", "nerva", "pius", "subfinder", "httpx", "katana", "nuclei"):
        assert tool in text
