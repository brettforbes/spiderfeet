#!/usr/bin/env python3
"""SPEC-006 CLI — regenerate tool Structure docs and composed ontology."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_CORPUS_DIR = Path(__file__).resolve().parent
if str(_CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(_CORPUS_DIR))

from core.structure_doc_engine import (  # noqa: E402
    ADAPTER_TOOLS,
    render_ontology_doc,
    render_tool_structure_doc,
    structure_doc_path,
    write_ontology_doc,
    write_tool_structure_doc,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render SPEC-006 structure docs from rules/<tool>/structure.yaml",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tool", help="Adapter tool id (e.g. nmap)")
    group.add_argument("--all", action="store_true", help="Render all ADAPTER_TOOLS structure docs")
    group.add_argument("--ontology", action="store_true", help="Compose _Current_Ontology.md")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths only; do not write files",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print rendered Markdown to stdout instead of writing",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if args.ontology:
        if args.stdout:
            print(render_ontology_doc(), end="")
            return 0
        path = write_ontology_doc(dry_run=args.dry_run)
        if args.dry_run:
            print(f"dry-run: would write {path}")
        else:
            print(f"wrote {path}")
        return 0

    tools = list(ADAPTER_TOOLS) if args.all else [args.tool]
    for tool in tools:
        if tool not in ADAPTER_TOOLS:
            print(f"error: unknown tool {tool!r}; expected one of {', '.join(ADAPTER_TOOLS)}", file=sys.stderr)
            return 1
        if args.stdout:
            print(render_tool_structure_doc(tool), end="")
            continue
        path = write_tool_structure_doc(tool, dry_run=args.dry_run)
        if args.dry_run:
            print(f"dry-run: would write {path}")
        else:
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
