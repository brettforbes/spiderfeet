"""SPEC-016 A4 — seed workflow step timeouts."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"


def test_12a_long_steps_have_config_timeout():
    doc = yaml.safe_load(EXAMPLE_12A.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in doc["steps"]}
    assert by_id["sfp_cli_nmap"]["config"]["timeout"] == 900
    assert by_id["sfp_cli_nerva"]["config"]["timeout"] == 300
    assert by_id["sfp_cli_katana"]["config"]["timeout"] == 600
    assert by_id["sfp_cli_nuclei"]["config"]["timeout"] == 900
