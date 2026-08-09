#!/usr/bin/env python3
"""SPEC-014 BD1/BD2 match-or-beat gate for nmap + netdiscover narratives (R14-06)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_CORPUS = Path(__file__).resolve().parent
if str(_CORPUS) not in sys.path:
    sys.path.insert(0, str(_CORPUS))

from core.narrative_engine import render_narrative, validate_narrative_coverage  # noqa: E402

REPO_ROOT = _CORPUS.parents[2]
STRUCTURE = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
DEFAULT_REF = _CORPUS / "fixtures" / "spec014_bd1_narrative_reference"

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
_MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
_IP = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
_SHAPE = re.compile(r"^\s+\w+", re.M)


def extract_h2_headings(md: str) -> list[str]:
    return [m.group(1).strip() for m in _H2.finditer(md)]


def _family_ok(tool: str, graph: dict[str, Any], md: str) -> list[str]:
    """Return list of missing section-family problems."""
    problems: list[str] = []
    headings = "\n".join(extract_h2_headings(md)).lower()
    nodes = graph.get("nodes") or []
    ids = {str(n.get("nugget_id") or "") for n in nodes}

    def has(*needles: str) -> bool:
        return any(n in headings for n in needles)

    if not has("introduction"):
        problems.append("missing Introduction")
    if not has("scan"):
        problems.append("missing Scan")
    if not has("conclusion"):
        problems.append("missing Conclusion")
    if not has("appendix"):
        problems.append("missing Appendix")

    if tool == "nmap":
        if "HOST" in ids and not has("host"):
            problems.append("missing Host section family")
        if "TRACE" in ids and not has("trace"):
            problems.append("missing Trace section family")
    elif tool == "netdiscover":
        if "SYSTEM" in ids and not has("system"):
            problems.append("missing System section family")
    return problems


def _progressive_ok(graph: dict[str, Any], md: str) -> list[str]:
    problems: list[str] = []
    ids = {str(n.get("nugget_id") or "") for n in graph.get("nodes") or []}
    roots_present = bool(ids & {"SCAN_RECORD", "HOST", "SYSTEM", "CDN", "COMPANY_NAME", "DOMAIN_NAME"})
    if roots_present and "```mermaid" not in md:
        problems.append("missing Mermaid diagrams for present meta-concepts")
    if md.count("### Edges") > 1:
        problems.append(f"appendix edges duplicated ({md.count('### Edges')} sections)")
    # Prefer structure overview when Scan present
    if "SCAN_RECORD" in ids and "## Scan" in md and "### Structure overview" not in md:
        # Allow legacy topology heading during transition
        if "### Scan topology" not in md and "```mermaid" not in md.split("## Scan", 1)[-1][:2000]:
            problems.append("Scan section lacks overview Mermaid")
    return problems


def _diagram_hygiene(md: str, *, max_shapes: int = 12) -> list[str]:
    problems: list[str] = []
    pre = md.split("## Appendix")[0] if "## Appendix" in md else md
    for block in _MERMAID.findall(pre):
        shapes = len(_SHAPE.findall(block))
        if shapes > max_shapes + 2:  # slight slack for flowchart header lines
            problems.append(f"mermaid shape count {shapes} exceeds cap ~{max_shapes}")
        if '["' not in block and _IP.search(block):
            problems.append("type-only overview Mermaid embeds IP literal")
    return problems


def evaluate_scenario(
    *,
    tool: str,
    scenario_key: str,
    reference_md: str,
    live: bool = True,
) -> list[str]:
    del reference_md  # reserved for future prose diffs; G5 via coverage on live graph
    problems: list[str] = []
    gpath = STRUCTURE / f"{tool}_{scenario_key}_proposed_nuggets_edges.json"
    if not gpath.is_file():
        return [f"missing live graph {gpath.name}"]
    graph = json.loads(gpath.read_text(encoding="utf-8"))
    new_md = render_narrative(graph, tool=tool, scenario_key=scenario_key)
    ok, missing = validate_narrative_coverage(graph, new_md)
    if not ok:
        problems.append(f"coverage missing: {missing[:8]}")
    problems.extend(_family_ok(tool, graph, new_md))
    if live:
        # When still on bespoke builders, progressive disclosure may fail — report as soft until BD2.
        problems.extend(_progressive_ok(graph, new_md))
        problems.extend(_diagram_hygiene(new_md))
    return problems


def load_manifest(reference: Path) -> dict[str, Any]:
    path = reference / "MANIFEST.json"
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REF)
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Only verify reference fixtures + MANIFEST exist (BD1). Skip render gate.",
    )
    parser.add_argument(
        "--allow-bespoke",
        action="store_true",
        help="Skip progressive-disclosure / hygiene checks (current nmap/netdiscover bespoke path).",
    )
    args = parser.parse_args()
    ref: Path = args.reference
    manifest = load_manifest(ref)
    failures = 0

    if args.baseline_only:
        missing_files = [e["file"] for e in manifest["files"] if not (ref / e["file"]).is_file()]
        criteria = ref / "MATCH_OR_BEAT.md"
        if missing_files:
            print("MISSING_FIXTURES", missing_files[:10])
            return 1
        if not criteria.is_file():
            print("MISSING_CRITERIA")
            return 1
        print(f"BD1_OK fixtures={manifest['count']} criteria={criteria.name}")
        return 0

    for entry in manifest["files"]:
        tool = entry["tool"]
        key = entry["scenario_key"]
        ref_md = (ref / entry["file"]).read_text(encoding="utf-8")
        problems = evaluate_scenario(
            tool=tool,
            scenario_key=key,
            reference_md=ref_md,
            live=not args.allow_bespoke,
        )
        if problems:
            failures += 1
            print(f"FAIL {tool}/{key}: {problems}")
        else:
            print(f"PASS {tool}/{key}")

    print(f"done failures={failures} total={manifest['count']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
