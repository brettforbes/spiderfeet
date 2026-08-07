"""S1 — tempfile manager tests."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.runtime.tempfile_mgr import TempFileManager  # noqa: E402


def test_write_line_text_matches_input_length():
    mgr = TempFileManager()
    path = mgr.write_line_text(["alpha", "beta", "gamma"])
    assert len(path.read_text(encoding="utf-8").strip().splitlines()) == 3
    mgr.cleanup()
