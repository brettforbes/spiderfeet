"""AJ4 / R10-12 — parity harness for ported ``modules_v2._core``.

For each of the 8 CLI tools, load a recorded structured fixture, run the ported
RuleEngine / topology / narrative path, and compare against original
``cli_corpus`` goldens under ``.docs/docs-for-cli-tools/nugget_structure/``.

Full adapter+hooks parity is deferred to Epic AK — see ``PARITY_DIFFS.md``.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Literal

import pytest

from modules_v2._core.graph_builder import GraphBuilder, nugget_node, validate_graph
from modules_v2._core.narrative_engine import render_narrative
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2._core.topology import add_scan_head, add_system_l2

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CORPUS_DIR = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"

ParityMode = Literal["near_full", "scan_head"]

# Scan-level nugget ids produced by RuleEngine (+ SCAN_TOOL) without record hooks.
SCAN_LEVEL_IDS = frozenset(
    {
        "SCAN_RECORD",
        "SCAN_CLI",
        "SCAN_TOOL",
        "SCAN_TARGET",
        "SCAN_TARGET_ORG",
        "SCAN_START",
        "SCAN_ELAPSED",
        "SCAN_EXIT_STATUS",
        "SCAN_SUMMARY",
        "SCAN_VERSION",
        "SCAN_MODE",
        "SCAN_PROBE_PROFILE",
        "SCAN_HOST_INPUT_COUNT",
        "SCAN_CRAWL_PROFILE",
        "SCAN_URL_INPUT_COUNT",
        "SCAN_FINDING_COUNT",
        "SCAN_TIMESTAMP",
        "SCAN_END_TIME",
        "SCAN_TRIES",
        "SCAN_EMPTY_SCANS",
        "SCAN_DISCOVERED",
        "UPSTREAM_SCENARIO_ID",
        "DOMAIN_NAME",  # katana sparse target root
    }
)

NODE_COUNT_TOLERANCE_NEAR_FULL = 2

CASES: list[dict[str, Any]] = [
    {
        "tool": "netdiscover",
        "scenario_id": "local_subnet_fast_parsable",
        "structured": EXAM_ROOT / "netdiscover" / "3_output_structured.json",
        "mode": "near_full",
    },
    {
        "tool": "nerva",
        "scenario_id": "tcp_closed_clean_miss",
        "structured": EXAM_ROOT / "nerva" / "6_output_structured.json",
        "mode": "near_full",
    },
    {
        "tool": "katana",
        "scenario_id": "from_httpx_vcof_sparse",
        "structured": EXAM_ROOT / "katana" / "3_output_structured.json",
        "mode": "near_full",
    },
    {
        "tool": "nmap",
        "scenario_id": "host_discovery_permissive_xml",
        "structured": FIXTURES_DIR / "nmap_scan_head.json",
        "mode": "scan_head",
        # Golden still used for narrative re-render + AH invariants.
    },
    {
        "tool": "pius",
        "scenario_id": "corporate_squarepeg_ndjson",
        "structured": EXAM_ROOT / "pius" / "4_output_structured.json",
        "mode": "scan_head",
    },
    {
        "tool": "subfinder",
        "scenario_id": "corporate_vcof_sparse_passive",
        "structured": EXAM_ROOT / "subfinder" / "3_output_structured.json",
        "mode": "scan_head",
    },
    {
        "tool": "httpx",
        "scenario_id": "from_subfinder_vcof_sparse",
        "structured": EXAM_ROOT / "httpx" / "3_output_structured.json",
        "mode": "scan_head",
    },
    {
        "tool": "nuclei",
        "scenario_id": "cipherheart_redis_lab",
        "structured": EXAM_ROOT / "nuclei" / "3_output_structured.json",
        "mode": "scan_head",
    },
]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _golden_graph_path(tool: str, scenario_id: str) -> Path:
    return NUGGET_ROOT / f"{tool}_{scenario_id}_proposed_nuggets_edges.json"


def _golden_md_path(tool: str, scenario_id: str) -> Path:
    return NUGGET_ROOT / f"{tool}_{scenario_id}_proposed_nuggets_edges_description.md"


def _normalize_nugget_ids(graph: dict[str, Any]) -> set[str]:
    return {str(node.get("nugget_id")) for node in graph.get("nodes") or [] if node.get("nugget_id")}


def _assert_no_ip_address(graph: dict[str, Any], *, label: str) -> None:
    bad = [n for n in graph.get("nodes") or [] if n.get("nugget_id") == "IP_ADDRESS"]
    assert not bad, f"{label}: found ambiguous IP_ADDRESS nodes (AH split incomplete)"


def _assert_no_orphans(graph: dict[str, Any], *, label: str) -> None:
    # validate_graph raises on orphans / duplicates / dangling edges
    try:
        validate_graph(graph)
    except ValueError as exc:
        pytest.fail(f"{label}: graph validation failed: {exc}")


def _inject_scan_data(tool: str, doc: dict[str, Any]) -> dict[str, Any]:
    """Mirror adapter scan_data injection without importing cli_corpus adapters."""
    out = dict(doc)
    if out.get("scan_data"):
        return out
    target = out.get("target") or out.get("org") or tool
    command = out.get("command") or tool
    if tool == "nerva":
        out["scan_data"] = f"nerva:{target}:{out.get('started_at') or command}"
    elif tool == "nmap":
        out["scan_data"] = out.get("scan_data") or f"nmap:{out.get('scan_target') or target}:{command}"
    else:
        out["scan_data"] = f"{tool}:{target}:{command}"
    return out


def _add_scan_tool(builder: GraphBuilder, scan_id: str, tool: str) -> None:
    node = builder.add_node(nugget_node("SCAN_TOOL", tool, nugget_type="DESCRIPTOR"))
    builder.add_edge(scan_id, node["id"], "had")


def _build_netdiscover_graph(doc: dict[str, Any]) -> dict[str, Any]:
    """Ported mirror of ``adapters.netdiscover.to_graph`` using ``_core.topology``."""
    scan_data = doc["netdiscover_scan"]
    args_label = scan_data.get("args", "netdiscover scan")
    runstats = scan_data.get("runstats") or {}
    finished = runstats.get("finished_time") or {}
    systems_stats = runstats.get("systems") or {}

    builder = GraphBuilder()
    scan = add_scan_head(builder, args_label, command=args_label)
    scan_id = scan["id"]

    def _desc(nugget_id: str, value: Any, *, description: str | None = None) -> None:
        if value is None or value == "":
            return
        node = builder.add_node(
            nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR", description=description)
        )
        builder.add_edge(scan_id, node["id"], "had")

    _desc("SCAN_TIMESTAMP", scan_data.get("start_time"), description="Scan Start Time")
    _desc("SCAN_END_TIME", finished.get("end_time"), description="Scan End Time")
    _desc("SCAN_SUMMARY", finished.get("summary"))
    _desc(
        "SCAN_EXIT_STATUS",
        scan_data.get("exit_status") or finished.get("exit_status"),
        description="Scan Exit Status",
    )
    _desc("SCAN_TRIES", systems_stats.get("scan_tries"), description="Scan Tries")
    _desc("SCAN_EMPTY_SCANS", systems_stats.get("empty_scans"), description="Empty Scans")
    _desc("SCAN_DISCOVERED", systems_stats.get("discovered"), description="Systems Discovered")

    for system in scan_data.get("systems") or []:
        ipv4 = system.get("ipv4")
        if not ipv4:
            continue
        add_system_l2(
            builder,
            scan_id,
            system=ipv4,
            ip_address=ipv4,
            mac_address=system.get("mac"),
            mac_vendor=(str(system.get("mac_vendor") or "").strip() or "Unknown"),
        )
    return builder.build()


def _build_rule_engine_graph(tool: str, doc: dict[str, Any]) -> dict[str, Any]:
    """RuleEngine scan head + mapped descriptors + SCAN_TOOL (+ sparse katana roots)."""
    doc = _inject_scan_data(tool, doc)
    pack = load_rule_pack(mapping_path(tool), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    _add_scan_tool(builder, scan["id"], tool)

    # Minimal katana hook surface used by the sparse golden (empty records[]).
    if tool == "katana":
        target = str(doc.get("target") or "").lower().rstrip(".")
        if target:
            root = builder.add_node(nugget_node("DOMAIN_NAME", target))
            builder.add_edge(scan["id"], root["id"], "contains")
        upstream = doc.get("httpx_scenario")
        if upstream:
            node = builder.add_node(
                nugget_node("UPSTREAM_SCENARIO_ID", str(upstream), nugget_type="DESCRIPTOR")
            )
            builder.add_edge(scan["id"], node["id"], "had")

    return builder.build()


def build_ported_graph(tool: str, structured: dict[str, Any]) -> dict[str, Any]:
    if tool == "netdiscover":
        return _build_netdiscover_graph(structured)
    return _build_rule_engine_graph(tool, structured)


def build_ported_narrative(tool: str, graph: dict[str, Any], scenario_id: str) -> str:
    return render_narrative(graph, tool=tool, scenario_key=scenario_id)


def _original_rule_engine_graph_via_subprocess(tool: str, structured: dict[str, Any]) -> dict[str, Any]:
    """Compare against original cli_corpus RuleEngine without importing it into modules_v2."""
    script = r"""
import json, sys
from pathlib import Path
corpus = Path(sys.argv[1])
tool = sys.argv[2]
doc = json.loads(sys.argv[3])
sys.path.insert(0, str(corpus))
from core.rule_engine import RuleEngine, load_rule_pack
from core.graph_builder import GraphBuilder, nugget_node
rules = corpus / "rules"
if not doc.get("scan_data"):
    target = doc.get("target") or doc.get("org") or tool
    command = doc.get("command") or tool
    if tool == "nerva":
        doc["scan_data"] = f"nerva:{target}:{doc.get('started_at') or command}"
    else:
        doc["scan_data"] = f"{tool}:{target}:{command}"
pack = load_rule_pack(rules / tool / "mapping.yaml", shared_dir=rules / "_shared")
engine = RuleEngine(pack)
builder = GraphBuilder()
scan = engine._add_scan_head(builder, doc)
engine._add_mapped_descriptors(builder, doc, scan["id"])
tool_node = builder.add_node(nugget_node("SCAN_TOOL", tool, nugget_type="DESCRIPTOR"))
builder.add_edge(scan["id"], tool_node["id"], "had")
print(json.dumps(builder.build()))
"""
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(CORPUS_DIR),
            tool,
            json.dumps(structured),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"original RuleEngine failed: {proc.stderr or proc.stdout}")
    return json.loads(proc.stdout)


@pytest.mark.parametrize("case", CASES, ids=[c["tool"] for c in CASES])
def test_parity_graph_and_narrative(case: dict[str, Any]) -> None:
    tool = case["tool"]
    scenario_id = case["scenario_id"]
    mode: ParityMode = case["mode"]
    structured_path: Path = case["structured"]
    golden_path = _golden_graph_path(tool, scenario_id)
    md_path = _golden_md_path(tool, scenario_id)

    assert structured_path.is_file(), f"missing structured fixture: {structured_path}"
    assert golden_path.is_file(), f"missing golden graph: {golden_path}"
    assert md_path.is_file(), f"missing golden narrative: {md_path}"

    structured = _read_json(structured_path)
    golden = _read_json(golden_path)
    golden_md = md_path.read_text(encoding="utf-8")

    ported = build_ported_graph(tool, structured)
    narrative = build_ported_narrative(tool, ported, scenario_id)

    _assert_no_ip_address(ported, label=f"{tool}/ported")
    _assert_no_ip_address(golden, label=f"{tool}/golden")
    _assert_no_orphans(ported, label=f"{tool}/ported")
    _assert_no_orphans(golden, label=f"{tool}/golden")

    assert narrative.strip(), f"{tool}: ported narrative is empty"
    assert len(narrative.strip()) >= 40, f"{tool}: ported narrative too short"

    ported_ids = _normalize_nugget_ids(ported)
    golden_ids = _normalize_nugget_ids(golden)
    assert "IP_ADDRESS" not in ported_ids
    assert "IP_ADDRESS" not in golden_ids

    if mode == "near_full":
        # Allow SCAN_START value formatting drift (nerva) — compare type sets + counts.
        assert ported_ids == golden_ids, (
            f"{tool}: nugget_id set mismatch\n"
            f"  only_ported={sorted(ported_ids - golden_ids)}\n"
            f"  only_golden={sorted(golden_ids - ported_ids)}"
        )
        ported_n = len(ported.get("nodes") or [])
        golden_n = len(golden.get("nodes") or [])
        assert abs(ported_n - golden_n) <= NODE_COUNT_TOLERANCE_NEAR_FULL, (
            f"{tool}: node count {ported_n} vs golden {golden_n} "
            f"(tol ±{NODE_COUNT_TOLERANCE_NEAR_FULL})"
        )
    else:
        # Scan-head / RuleEngine-only: every ported type must appear in the golden,
        # and the scan-level intersection must match after normalize.
        assert ported_ids <= golden_ids, (
            f"{tool}: ported nugget_ids not subset of golden\n"
            f"  extra={sorted(ported_ids - golden_ids)}"
        )
        ported_scan = ported_ids & SCAN_LEVEL_IDS
        golden_scan = golden_ids & SCAN_LEVEL_IDS
        # Ported scan-level set should equal the intersection of what RuleEngine emits
        # with golden scan-level ids (golden may have more SCAN_* from hooks).
        assert ported_scan <= golden_scan
        assert ported_scan, f"{tool}: expected at least one scan-level nugget_id"

    # Narrative engine parity: re-render the *golden* graph through ported _core.
    rerendered = build_ported_narrative(tool, golden, scenario_id)
    assert rerendered.strip(), f"{tool}: narrative re-render of golden graph is empty"
    assert len(rerendered) >= min(80, len(golden_md) // 4), (
        f"{tool}: re-rendered narrative unexpectedly short vs golden MD"
    )


def _build_rule_engine_only(tool: str, doc: dict[str, Any]) -> dict[str, Any]:
    """RuleEngine + SCAN_TOOL only (no tool-specific hook extras)."""
    doc = _inject_scan_data(tool, doc)
    pack = load_rule_pack(mapping_path(tool), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    _add_scan_tool(builder, scan["id"], tool)
    return builder.build()


@pytest.mark.parametrize(
    "case",
    [c for c in CASES if c["tool"] != "netdiscover"],
    ids=[c["tool"] for c in CASES if c["tool"] != "netdiscover"],
)
def test_rule_engine_matches_original_core(case: dict[str, Any]) -> None:
    """Ported RuleEngine(+SCAN_TOOL) matches original cli_corpus core on the same fixture."""
    if not CORPUS_DIR.is_dir():
        pytest.skip("cli_corpus tree missing")

    tool = case["tool"]
    structured = _read_json(case["structured"])
    ported = _build_rule_engine_only(tool, structured)
    original = _original_rule_engine_graph_via_subprocess(tool, structured)

    assert _normalize_nugget_ids(ported) == _normalize_nugget_ids(original)
    assert len(ported["nodes"]) == len(original["nodes"])
    # Instance ids must match (same ontology seed + catalogues).
    assert {n["id"] for n in ported["nodes"]} == {n["id"] for n in original["nodes"]}, (
        f"{tool}: instance id drift between ported and original RuleEngine"
    )


def test_all_eight_tools_covered() -> None:
    tools = {c["tool"] for c in CASES}
    expected = {
        "nmap",
        "netdiscover",
        "nerva",
        "pius",
        "subfinder",
        "httpx",
        "katana",
        "nuclei",
    }
    assert tools == expected
