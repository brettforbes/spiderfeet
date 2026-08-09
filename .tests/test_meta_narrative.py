"""SPEC-014 R14-02/04/05 — meta_narrative progressive-disclosure primitives."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.meta_concept_registry import clear_registry_cache, get_meta_concept  # noqa: E402
from core.meta_narrative import (  # noqa: E402
    append_appendix,
    category_example_mermaid,
    category_table,
    concept_overview_mermaid,
    concept_prose,
    count_mermaid_shapes,
    detect_meta_concepts,
)


PIUS_LIKE = {
    "nodes": [
        {"id": "s1", "nugget_id": "SCAN_RECORD", "nugget_data": "pius:org:cmd"},
        {"id": "cli", "nugget_id": "SCAN_CLI", "nugget_data": "pius run --org X"},
        {"id": "c1", "nugget_id": "COMPANY_NAME", "nugget_data": "The Upside Pty Ltd"},
        {"id": "doms", "nugget_id": "DOMAINS", "nugget_data": "DOMAINS"},
        {"id": "d1", "nugget_id": "DOMAIN_NAME", "nugget_data": "theupside.com.au"},
        {"id": "d2", "nugget_id": "DOMAIN_NAME", "nugget_data": "www.theupside.com.au"},
        {"id": "d3", "nugget_id": "DOMAIN_NAME", "nugget_data": "mail.theupside.com.au"},
        {"id": "d4", "nugget_id": "DOMAIN_NAME", "nugget_data": "dev.theupside.com.au"},
        {"id": "d5", "nugget_id": "DOMAIN_NAME", "nugget_data": "test.theupside.com.au"},
    ],
    "edges": [
        {"source": "s1", "target": "cli", "relation": "had"},
        {"source": "s1", "target": "c1", "relation": "contains"},
        {"source": "c1", "target": "doms", "relation": "contains"},
        {"source": "doms", "target": "d1", "relation": "contains"},
        {"source": "doms", "target": "d2", "relation": "contains"},
        {"source": "doms", "target": "d3", "relation": "contains"},
        {"source": "doms", "target": "d4", "relation": "contains"},
        {"source": "doms", "target": "d5", "relation": "contains"},
        {"source": "d1", "target": "d2", "relation": "contains"},
        # Duplicate type edges (same as the old recital bug).
        {"source": "doms", "target": "d2", "relation": "contains"},
        {"source": "doms", "target": "d2", "relation": "contains"},
    ],
}


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_registry_cache()
    yield
    clear_registry_cache()


def test_detect_meta_concepts_orders_present_only():
    found = detect_meta_concepts(PIUS_LIKE)
    ids = [c["id"] for c in found]
    assert ids == ["scan", "org", "domain"]


def test_concept_overview_mermaid_type_only_and_capped():
    org = get_meta_concept("org")
    md = concept_overview_mermaid(PIUS_LIKE, org)
    assert "```mermaid" in md
    assert "COMPANY_NAME" in md
    assert "DOMAINS" in md
    assert "The Upside" not in md
    assert count_mermaid_shapes(md) <= 12


def test_category_example_mermaid_cap_and_more():
    org = get_meta_concept("org")
    md = category_example_mermaid(PIUS_LIKE, org, "DOMAINS", example_cap=3)
    assert "+2 more" in md
    assert "DOMAIN_NAME:" in md
    assert count_mermaid_shapes(md) <= 12
    # Full inventory still available via table.
    table = category_table(PIUS_LIKE, org, "DOMAINS")
    assert "theupside.com.au" in table
    assert "test.theupside.com.au" in table
    assert table.count("DOMAIN_NAME") >= 5


def test_concept_prose_includes_counts():
    org = get_meta_concept("org")
    prose = concept_prose(PIUS_LIKE, org)
    assert "1" in prose
    assert "The Upside Pty Ltd" in prose


def test_append_appendix_dedupes_edges():
    lines: list[str] = []
    append_appendix(lines, PIUS_LIKE)
    text = "\n".join(lines)
    assert "## Appendix" in text
    # Type-level edge DOMAINS contains DOMAIN_NAME should appear once.
    assert text.count("| `DOMAINS` | `contains` | `DOMAIN_NAME` |") == 1
