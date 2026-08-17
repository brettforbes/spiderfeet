"""SPEC-019 R19-03 — host-scoped ip_port_list GSE."""

from __future__ import annotations

from modules_v2._core.graph_builder import GraphBuilder
from modules_v2._core.topology import add_host_networks_port_service, add_scan_head
from spiderfeet_v2.workflow.gse_eval import evaluate_output_vars
from spiderfeet_v2.workflow.loader import load_workflow
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"


def _build_two_host_graph() -> dict:
    builder = GraphBuilder()
    scan = add_scan_head(builder, "nmap:synthetic-two-host")
    scan_id = scan["id"]
    add_host_networks_port_service(
        builder,
        scan_id,
        host="10.0.0.1",
        ip_address="10.0.0.1",
        transport="tcp",
        port=22,
        service="ssh",
    )
    add_host_networks_port_service(
        builder,
        scan_id,
        host="10.0.0.2",
        ip_address="10.0.0.2",
        transport="tcp",
        port=443,
        service="https",
    )
    return builder.build()


def test_ip_port_list_no_cross_host_cartesian() -> None:
    doc = load_workflow(EXAMPLE_12A, validate=True)
    step = next(s for s in doc["steps"] if s["id"] == "sfp_cli_nmap")
    graph = _build_two_host_graph()
    vars_out = evaluate_output_vars(step, graph)
    values = set(vars_out["ip_port_list"])
    assert values == {"10.0.0.1:22", "10.0.0.2:443"}
    assert len(values) == 2
