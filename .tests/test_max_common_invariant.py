"""SPEC-014 BE2 — max-common / min-specific invariant (R14-07)."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / ".seed" / "scripts" / "cli_corpus"
if str(CORPUS) not in sys.path:
    sys.path.insert(0, str(CORPUS))

from core import max_common_invariant as mci  # noqa: E402


def test_max_common_invariant_passes_on_repo_adapters():
    problems = mci.check_max_common_invariant()
    assert problems == [], problems


def test_synthetic_adapter_with_extra_narrative_python_fails(tmp_path, monkeypatch):
    adapters = tmp_path / "adapters"
    rules = tmp_path / "rules"
    tool = adapters / "badtool"
    tool.mkdir(parents=True)
    (rules / "badtool").mkdir(parents=True)
    (tool / "__init__.py").write_text(
        textwrap.dedent(
            """
            def _load_narrative_profile():
                return {}

            def to_narrative(graph, *, scenario_key=\"x\"):
                # invents local narrative logic instead of shared engine
                return \"# bad\\n\" + \"\\n\".join(n[\"id\"] for n in graph.get(\"nodes\", []))
            """
        ),
        encoding="utf-8",
    )
    (rules / "badtool" / "narrative.yaml").write_text(
        "tool: badtool\nunknown_key: true\ntool_name: Bad\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mci, "ADAPTERS", adapters)
    monkeypatch.setattr(mci, "RULES", rules)
    problems = mci.check_max_common_invariant()
    assert any("forbidden narrative helper" in p for p in problems)
    assert any("must call render_narrative" in p for p in problems)
    assert any("unknown_key" in p for p in problems)
