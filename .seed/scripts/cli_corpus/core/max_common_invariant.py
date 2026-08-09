"""SPEC-014 max-common / min-specific invariant (R14-07)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import yaml

_CORPUS = Path(__file__).resolve().parents[1]
ADAPTERS = _CORPUS / "adapters"
RULES = _CORPUS / "rules"

# Keys read by ``render_narrative`` / ``build_factual_intro``.
ENGINE_CONSUMED_KEYS = frozenset(
    {
        "tool_name",
        "intro_facts",
        "phrasing",
        "meta_concepts",
        "include_trace",
        "include_appendix",
        "footer_brand",
        "host_nugget_id",
    }
)

# Documented metadata / legacy keys that may remain without driving prose.
METADATA_OR_LEGACY_KEYS = frozenset(
    {
        "tool",
        "profile",
        "version",
        "seed_docs",
        "sections",
        "primary_sections",
        "categories",
        "appendix_format",
    }
)

ALLOWED_NARRATIVE_YAML_KEYS = ENGINE_CONSUMED_KEYS | METADATA_OR_LEGACY_KEYS

_FORBIDDEN_ADAPTER_NAMES = frozenset(
    {
        "NarrativeReportBuilder",
        "NetdiscoverNarrativeReportBuilder",
        "build_narrative_report",
        "build_nmap_narrative_report",
        "build_netdiscover_narrative_report",
        "_load_narrative_profile",
        "render_concept_section",
        "append_appendix",
    }
)


def iter_tool_adapters() -> list[Path]:
    return sorted(
        p
        for p in ADAPTERS.glob("*/__init__.py")
        if p.parent.name not in {"_template", "__pycache__"}
    )


def check_adapter_to_narrative_shim(path: Path) -> list[str]:
    """Adapters may only expose a thin ``to_narrative`` that calls ``render_narrative``."""
    problems: list[str] = []
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    tool = path.parent.name

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in _FORBIDDEN_ADAPTER_NAMES:
            problems.append(f"{tool}: forbidden narrative helper `{node.name}`")
        if isinstance(node, ast.ClassDef) and node.name in _FORBIDDEN_ADAPTER_NAMES:
            problems.append(f"{tool}: forbidden narrative class `{node.name}`")

    to_nar = next(
        (
            n
            for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "to_narrative"
        ),
        None,
    )
    if to_nar is None:
        problems.append(f"{tool}: missing to_narrative shim")
        return problems

    # Body must reference render_narrative and must not define nested narrative builders.
    body_dump = ast.dump(to_nar)
    if "render_narrative" not in body_dump:
        problems.append(f"{tool}: to_narrative must call render_narrative")
    for child in ast.walk(to_nar):
        if isinstance(child, ast.FunctionDef) and child is not to_nar:
            problems.append(f"{tool}: to_narrative must not nest function `{child.name}`")
    # Heuristic: shim should stay small (import + return).
    if len(to_nar.body) > 6:
        problems.append(f"{tool}: to_narrative body too large ({len(to_nar.body)} stmts); keep shim thin")
    return problems


def check_narrative_yaml_keys(path: Path) -> list[str]:
    problems: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return [f"{path.parent.name}: narrative.yaml must be a mapping"]
    for key in data:
        if key not in ALLOWED_NARRATIVE_YAML_KEYS:
            problems.append(
                f"{path.parent.name}: narrative.yaml key `{key}` is neither engine-consumed "
                f"nor allowed metadata (R14-07)"
            )
    return problems


def check_max_common_invariant() -> list[str]:
    problems: list[str] = []
    for adapter in iter_tool_adapters():
        problems.extend(check_adapter_to_narrative_shim(adapter))
        yaml_path = RULES / adapter.parent.name / "narrative.yaml"
        if yaml_path.is_file():
            problems.extend(check_narrative_yaml_keys(yaml_path))
        else:
            problems.append(f"{adapter.parent.name}: missing rules/{adapter.parent.name}/narrative.yaml")
    return problems


def assert_max_common_invariant() -> None:
    problems = check_max_common_invariant()
    if problems:
        raise AssertionError("max-common invariant failed:\n- " + "\n- ".join(problems))
