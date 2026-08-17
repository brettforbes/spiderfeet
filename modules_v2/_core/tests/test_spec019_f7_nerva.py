"""SPEC-019 F7 — Nerva apex COMPANY wrap."""

from __future__ import annotations

from modules_v2.adapters.nerva import to_graph


def test_nerva_wraps_scan_target_with_company() -> None:
    doc = {
        "target": "scanme.nmap.org",
        "records": [
            {
                "host": "scanme.nmap.org",
                "ip": "45.33.32.156",
                "port": 22,
                "protocol": "ssh",
                "transport": "tcp",
                "metadata": {"banner": "SSH-2.0-OpenSSH"},
            }
        ],
    }
    graph = to_graph(doc)
    nodes = graph["nodes"]
    assert any(n["nugget_id"] == "COMPANY" and n["nugget_data"] == "company:scanme.nmap.org" for n in nodes)
    assert any(n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "scanme.nmap.org" for n in nodes)
