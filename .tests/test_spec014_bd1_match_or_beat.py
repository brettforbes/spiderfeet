"""BD1: reference fixtures + match-or-beat criteria exist for R14-06."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REF = REPO / ".seed" / "scripts" / "cli_corpus" / "fixtures" / "spec014_bd1_narrative_reference"
GATE = REPO / ".seed" / "scripts" / "cli_corpus" / "match_or_beat.py"


def test_bd1_manifest_and_criteria_present():
    assert (REF / "MATCH_OR_BEAT.md").is_file()
    manifest = json.loads((REF / "MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["count"] >= 30
    assert manifest["requirement"] == "R14-06"
    for entry in manifest["files"]:
        assert (REF / entry["file"]).is_file(), entry["file"]
        assert entry["tool"] in {"nmap", "netdiscover"}
        assert entry["sha256"]


def test_bd1_baseline_gate_script():
    proc = subprocess.run(
        [sys.executable, str(GATE), "--baseline-only"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "BD1_OK" in proc.stdout
