"""SPEC-004 R4-01-07 anti-sprawl governance checks."""

from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
ADAPTERS = CLI_CORPUS / "adapters"
RULES = CLI_CORPUS / "rules"

REQUIRED_ADAPTER_TOOLS = (
    "netdiscover",
    "nmap",
    "nerva",
    "pius",
    "subfinder",
    "httpx",
    "katana",
    "nuclei",
)

REQUIRED_ADAPTER_API = ("to_structured", "to_text", "to_graph", "to_narrative", "build_outputs")

SEED_RULE_CITATION = re.compile(
    r"(06B|07B|08 R|09 S|10 H|11B|doc 14|legacy katana|N[0-9]|P[0-9]|G[0-9]|SEC|TMP|FIND|SEV|T[0-9]|V[0-9]|F[0-9]|H[0-9]|S[0-9])"
)


def test_all_spec004_adapters_expose_four_output_api():
    for tool in REQUIRED_ADAPTER_TOOLS:
        init_path = ADAPTERS / tool / "__init__.py"
        assert init_path.is_file(), f"missing adapter package: {tool}"
        source = init_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        defined = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        for fn in REQUIRED_ADAPTER_API:
            assert fn in defined, f"{tool} adapter missing {fn}()"


def test_all_spec004_adapters_have_mapping_yaml():
    for tool in REQUIRED_ADAPTER_TOOLS:
        mapping = RULES / tool / "mapping.yaml"
        assert mapping.is_file(), f"missing rules/{tool}/mapping.yaml"
        text = mapping.read_text(encoding="utf-8")
        assert "capture_family:" in text, f"{tool} mapping.yaml missing capture_family"
        assert "structured_native" in text or "text_native" in text, tool


def test_hooks_cite_seed_rule_ids_when_present():
    for hooks_path in ADAPTERS.glob("*/hooks.py"):
        source = hooks_path.read_text(encoding="utf-8")
        if "def apply_" not in source:
            continue
        assert SEED_RULE_CITATION.search(source), f"{hooks_path} missing seed rule citation in docstrings"


def test_cli_tool_to_graph_has_no_divergent_uid_helper():
    source = (CLI_CORPUS / "cli_tool_to_graph.py").read_text(encoding="utf-8")
    assert "def _uid" not in source
    assert "nugget_instance_id" in source


def test_adapters_do_not_define_alternate_uuid_schemes():
    forbidden = re.compile(r"uuid4\(|uuid5\(NAMESPACE_|def _uid|def make_.*_id")
    for path in ADAPTERS.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if path.name == "__init__.py" and "uuid4" in source:
            continue
        match = forbidden.search(source)
        assert match is None, f"{path} may define alternate identity scheme: {match.group(0) if match else ''}"


def test_legacy_converters_delegate_to_adapters():
    delegators = {
        "nuclei_json_to_graph.py": "nuclei_adapter",
        "katana_json_to_graph.py": "katana_adapter",
        "subfinder_json_to_graph.py": "subfinder_adapter",
        "httpx_json_to_graph.py": "httpx_adapter",
    }
    for filename, token in delegators.items():
        path = CLI_CORPUS / filename
        assert path.is_file(), filename
        assert token in path.read_text(encoding="utf-8"), f"{filename} should delegate to adapter"
