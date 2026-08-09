"""SPEC-014 BH1/BH2 — nuclei batching + progress (R14-11/R14-12)."""

from __future__ import annotations

import math
from types import SimpleNamespace

from modules_v2.sfp_cli_nuclei import (
    DEFAULT_BATCH_SIZE,
    chunk_targets,
    option_passes_from_spec,
    plan_batch_jobs,
    progress_totals,
    sfp_cli_nuclei,
)


def test_chunk_targets_15000_urls_into_blocks_of_20():
    urls = [f"https://example.com/{i}" for i in range(15_000)]
    chunks = chunk_targets(urls, batch_size=20)
    assert len(chunks) == 750
    assert all(len(c) == 20 for c in chunks)
    assert chunks[0][0].endswith("/0")
    assert chunks[-1][-1].endswith("/14999")


def test_plan_batch_jobs_fans_out_passes_and_chunks():
    urls = [f"https://t/{i}" for i in range(45)]
    passes = [{"tags": "tech"}, {"tags": "cve", "severity": "critical,high"}]
    jobs = plan_batch_jobs(urls, batch_size=20, option_passes=passes)
    assert len(jobs) == 3 * 2  # 3 chunks × 2 passes
    assert jobs[0]["pass"]["tags"] == "tech"
    assert len(jobs[0]["targets"]) == 20
    assert len(jobs[2]["targets"]) == 5


def test_progress_totals_for_15k_synthetic():
    urls = [f"https://example.com/{i}" for i in range(15_000)]
    passes = [{"tags": "tech"}, {"tags": "exposure"}]
    prog = progress_totals(urls, batch_size=20, option_passes=passes)
    assert prog["chunks"] == 750
    assert prog["passes"] == 2
    assert prog["batches_total"] == 1500
    assert prog["batch_size"] == DEFAULT_BATCH_SIZE
    assert prog["targets"] == 15_000


def test_option_passes_from_spec_defaults_and_explicit():
    assert option_passes_from_spec({})[0]["tags"] == "tech"
    assert option_passes_from_spec({"tags": "cve", "severity": "high"}) == [
        {"tags": "cve", "severity": "high"}
    ]
    multi = option_passes_from_spec({"option_passes": [{"tags": "a"}, {"tags": "b"}]})
    assert [p["tags"] for p in multi] == ["a", "b"]


def test_run_batched_aggregates_jsonl_without_real_binary(monkeypatch):
    mod = sfp_cli_nuclei()
    calls: list[list[str]] = []

    def fake_timed(argv, timeout=180.0):  # noqa: ARG001
        calls.append(list(argv))
        # One JSONL record per batch
        n = len(calls)
        stdout = (
            '{"template-id":"t","info":{"name":"n","severity":"info"},'
            f'"host":"h{n}","matched-at":"https://h{n}/"}}\n'
        )
        completed = SimpleNamespace(stdout=stdout, stderr="", returncode=0)
        return completed, 0.01, None

    monkeypatch.setattr(mod, "_timed_run_argv", fake_timed)
    monkeypatch.setattr(
        "modules_v2.sfp_cli_nuclei._resolve_nuclei_executable",
        lambda: (["nuclei"], None),
    )

    events: list[dict] = []
    urls = [f"https://lab.example/{i}" for i in range(45)]
    result = mod.run(
        {
            "urls": urls,
            "batch_size": 20,
            "option_passes": [{"tags": "tech", "severity": "info"}],
            "timeout": 5,
            "progress_callback": events.append,
            "scenario_key": "batch_demo",
        }
    )
    assert result["status"] in {"SUCCESS", "success", result.get("status")}
    assert result["progress"]["batches_total"] == 3
    assert result["progress"]["bundles_scanned"] == 3
    assert "bundles scanned across all options: 3" in result["summary"]
    assert len(calls) == 3
    assert any("-u" in c for c in calls)
    assert events, "progress_callback should fire"
    records = (result.get("structured") or {}).get("records") or []
    assert len(records) == 3
