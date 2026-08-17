"""SPEC-019 F6 — Pius COMPANY wrap."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules_v2.adapters.pius import to_graph


def test_pius_company_wrap_has_name_descriptor_and_apex_domain() -> None:
    doc = {
        "org": "Linode",
        "target": "linode.com",
        "records": [
            {"Type": "domain", "Value": "status.linode.com", "Source": "crt-sh", "Data": {"org": "Linode"}},
        ],
    }
    graph = to_graph(doc)
    nodes = graph["nodes"]
    edges = graph["edges"]
    company = next(n for n in nodes if n["nugget_id"] == "COMPANY")
    apex = next(n for n in nodes if n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "linode.com")
    assert company["nugget_data"] == "company:linode.com"
    assert any(
        n["nugget_id"] == "COMPANY_NAME" and n["nugget_data"] == "Linode"
        for n in nodes
    )
    assert any(e["source"] == company["id"] and e["target"] == apex["id"] for e in edges)
