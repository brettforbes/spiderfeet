#!/usr/bin/env python3
"""Static analysis of module output → nugget (event type) conversion patterns."""

from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "modules"
OUT_DIR = REPO_ROOT / ".docs" / "analysis" / "conversion_to_types"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
NUGGETS_JSON = REPO_ROOT / ".docs" / "analysis" / "nuggets.json"

SF_METHOD_SIGNALS = (
    "validIP",
    "validIP6",
    "validIpNetwork",
    "validHost",
    "isDomain",
    "urlFQDN",
    "hostDomain",
    "resolveHost",
    "resolveIP",
    "fetchUrl",
    "parseCert",
    "cveInfo",
    "optValueToData",
)

HELPER_SIGNALS = (
    "extractLinksFromHtml",
    "extractEmailsFromText",
    "extractPhoneNumbers",
    "extractHashesFromText",
    "extractIbansFromText",
)


@dataclass
class ModuleAnalysis:
    module_id: str
    produced: list[str] = field(default_factory=list)
    consumed: list[str] = field(default_factory=list)
    emitted_types: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    has_subprocess: bool = False
    has_json_loads: bool = False
    has_fetch_url: bool = False
    has_regex: bool = False
    has_beautifulsoup: bool = False
    service_origin: str = ""
    conversion_pattern: str = ""


def _str_list(node: ast.AST | None) -> list[str]:
    if node is None:
        return []
    if isinstance(node, ast.List):
        out: list[str] = []
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                out.append(elt.value)
        return out
    return []


def _event_type_from_call(node: ast.Call) -> str | None:
    if not node.args:
        return None
    first = node.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def analyse_module(path: Path) -> ModuleAnalysis:
    module_id = path.stem
    text = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(text)
    rec = ModuleAnalysis(module_id=module_id)

    for sig in SF_METHOD_SIGNALS:
        if f"self.sf.{sig}" in text or f"sf.{sig}" in text:
            rec.signals.append(f"sf.{sig}")
    for sig in HELPER_SIGNALS:
        if sig in text:
            rec.signals.append(f"helpers.{sig}")

    rec.has_subprocess = "Popen(" in text or "subprocess." in text
    rec.has_json_loads = "json.loads" in text
    rec.has_fetch_url = "fetchUrl" in text
    rec.has_regex = bool(re.search(r"\bre\.(findall|search|match|compile)", text))
    rec.has_beautifulsoup = "BeautifulSoup" in text

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "producedEvents":
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    rec.produced = _str_list(child.value)
        if isinstance(node, ast.FunctionDef) and node.name == "watchedEvents":
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    rec.consumed = _str_list(child.value)
        if isinstance(node, ast.Call):
            func = node.func
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name == "SpiderFeetEvent":
                et = _event_type_from_call(node)
                if et:
                    rec.emitted_types.append(et)

    rec.emitted_types = sorted(set(rec.emitted_types))
    rec.signals = sorted(set(rec.signals))
    rec.conversion_pattern = classify_pattern(rec)
    return rec


def classify_pattern(rec: ModuleAnalysis) -> str:
    if rec.module_id.startswith("sfp_tool_"):
        return "cli_subprocess_parse"
    if rec.has_subprocess and not rec.module_id.startswith("sfp_tool_"):
        return "subprocess_other"
    if rec.has_fetch_url and rec.has_json_loads:
        return "api_json_map"
    if rec.has_fetch_url:
        return "api_text_or_html"
    if "helpers.extract" in " ".join(rec.signals) or "BeautifulSoup" in str(rec.has_beautifulsoup):
        return "content_extract"
    if any(s.startswith("sf.resolve") for s in rec.signals) or "sf.validIP" in rec.signals:
        return "dns_network_local"
    if rec.has_regex and not rec.has_fetch_url:
        return "regex_local"
    return "custom_logic"


def load_catalogue() -> dict[str, dict]:
    services = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    return {s["module_id"]: s for s in services}


def load_nuggets() -> dict[str, dict]:
    rows = json.loads(NUGGETS_JSON.read_text(encoding="utf-8"))
    return {r["nugget_id"]: r for r in rows}


def pattern_description(pattern: str) -> str:
    return {
        "cli_subprocess_parse": "Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events.",
        "subprocess_other": "Uses subprocess outside sfp_tool_* naming (rare).",
        "api_json_map": "HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.",
        "api_text_or_html": "HTTP fetch → text/HTML parsing without structured JSON schema.",
        "content_extract": "Parses page/content events with helpers/regex; emits derived identifiers.",
        "dns_network_local": "DNS, sockets, or validation helpers; no third-party OSINT API.",
        "regex_local": "Primarily regex over event.data or fetched reference files.",
        "custom_logic": "Mixed or module-specific logic not captured by heuristics.",
    }.get(pattern, pattern)


def write_module_doc(rec: ModuleAnalysis, cat: dict | None, nuggets: dict[str, dict]) -> None:
    lines = [
        f"# {rec.module_id}",
        "",
        f"**Conversion pattern:** `{rec.conversion_pattern}` — {pattern_description(rec.conversion_pattern)}",
        "",
    ]
    if cat:
        lines.extend([
            "## Catalogue",
            "",
            f"- **Name:** {cat.get('name', '')}",
            f"- **service_origin:** `{cat.get('service_origin', '')}`",
            f"- **Summary:** {cat.get('summary', '')}",
            "",
        ])
        routes = cat.get("routes") or []
        if routes:
            r0 = routes[0]
            lines.extend([
                "## Declared routes (catalogue)",
                "",
                f"- **Consumes:** {', '.join(r0.get('consumed') or [])}",
                f"- **Produces:** {', '.join(r0.get('produced') or [])}",
                "",
            ])

    lines.extend([
        "## Produced nugget types",
        "",
        "| Nugget ID | Archetype | Emitted in code (static) |",
        "|-----------|-----------|--------------------------|",
    ])
    for p in rec.produced or ["_(none declared)_"]:
        meta = nuggets.get(p, {})
        archetype = meta.get("nugget_type", "—")
        in_code = "yes" if p in rec.emitted_types else "declared only"
        lines.append(f"| `{p}` | {archetype} | {in_code} |")

    if rec.emitted_types:
        extra = [t for t in rec.emitted_types if t not in rec.produced]
        if extra:
            lines.extend(["", f"_Additional types seen in code but not in producedEvents():_ {', '.join(f'`{t}`' for t in extra)}"])

    lines.extend([
        "",
        "## Consumed nugget types",
        "",
        ", ".join(f"`{c}`" for c in rec.consumed) or "_(none)_",
        "",
        "## Parsing signals (static)",
        "",
    ])
    flags = []
    if rec.has_subprocess:
        flags.append("subprocess/Popen")
    if rec.has_json_loads:
        flags.append("json.loads")
    if rec.has_fetch_url:
        flags.append("fetchUrl")
    if rec.has_regex:
        flags.append("regex")
    if rec.has_beautifulsoup:
        flags.append("BeautifulSoup")
    lines.append(", ".join(flags) or "_(none detected)_")
    if rec.signals:
        lines.extend(["", "**SpiderFeet/sf helpers used:**", ""])
        for s in rec.signals:
            lines.append(f"- `{s}`")

    lines.extend([
        "",
        "## Conversion notes",
        "",
        "SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. "
        "The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields "
        "(port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.",
        "",
        f"Module source: `modules/{rec.module_id}.py`",
        "",
    ])

    (OUT_DIR / "modules" / f"{rec.module_id}.md").write_text("\n".join(lines), encoding="utf-8")


def write_index(analyses: list[ModuleAnalysis], nuggets: dict[str, dict]) -> None:
    by_pattern: dict[str, list[str]] = defaultdict(list)
    type_producers: dict[str, list[str]] = defaultdict(list)
    for rec in analyses:
        by_pattern[rec.conversion_pattern].append(rec.module_id)
        for p in rec.produced:
            type_producers[p].append(rec.module_id)

    summary = {
        "module_count": len(analyses),
        "pattern_counts": {k: len(v) for k, v in sorted(by_pattern.items())},
        "nugget_types_produced": len(type_producers),
        "patterns": {k: sorted(v) for k, v in sorted(by_pattern.items())},
        "type_producers": {k: sorted(v) for k, v in sorted(type_producers.items())},
    }
    (OUT_DIR / "module_conversion_index.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Nugget type producers (index)",
        "",
        "Auto-generated from `analyse_module_conversions.py`. One row per nugget type; modules that declare it in `producedEvents()`.",
        "",
        "| Nugget ID | Archetype | Producer count | Modules |",
        "|-----------|-----------|----------------|---------|",
    ]
    for nugget_id in sorted(type_producers.keys()):
        meta = nuggets.get(nugget_id, {})
        archetype = meta.get("nugget_type", "—")
        mods = type_producers[nugget_id]
        mod_preview = ", ".join(f"`{m}`" for m in mods[:5])
        if len(mods) > 5:
            mod_preview += f", … (+{len(mods) - 5})"
        lines.append(f"| `{nugget_id}` | {archetype} | {len(mods)} | {mod_preview} |")

    (OUT_DIR / "nugget_type_producers.md").write_text("\n".join(lines), encoding="utf-8")

    plines = [
        "# Conversion pattern index",
        "",
        "| Pattern | Count | Description |",
        "|---------|-------|-------------|",
    ]
    for pattern, mods in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
        plines.append(
            f"| `{pattern}` | {len(mods)} | {pattern_description(pattern)} |"
        )
    (OUT_DIR / "pattern_index.md").write_text("\n".join(plines), encoding="utf-8")


def main() -> int:
    catalogue = load_catalogue()
    nuggets = load_nuggets()
    (OUT_DIR / "modules").mkdir(parents=True, exist_ok=True)

    analyses: list[ModuleAnalysis] = []
    for path in sorted(MODULES_DIR.glob("sfp_*.py")):
        if path.name.startswith("sfp__"):
            continue
        rec = analyse_module(path)
        cat = catalogue.get(rec.module_id)
        if cat:
            rec.service_origin = str(cat.get("service_origin") or "")
        write_module_doc(rec, cat, nuggets)
        analyses.append(rec)

    write_index(analyses, nuggets)
    print(f"analysed {len(analyses)} modules -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
