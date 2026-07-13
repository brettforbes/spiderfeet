"""CLI entrypoints for workflow validate / GSE eval / dry helpers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python -m cli_workflow.cli` from repo via PYTHONPATH=.seed/scripts
from cli_workflow.core.gse_eval import eval_binding, eval_select
from cli_workflow.core.loader import load_workflow, topological_waves


def cmd_validate(args: argparse.Namespace) -> int:
    doc = load_workflow(args.workflow, validate=True)
    waves = topological_waves(doc["steps"])
    print(f"OK: {args.workflow}")
    print(f"steps={len(doc['steps'])} waves={waves}")
    return 0


def cmd_gse_file(args: argparse.Namespace) -> int:
    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    select = json.loads(Path(args.select).read_text(encoding="utf-8"))
    values = eval_select(select, graph)
    for v in values:
        print(v)
    print(f"# count={len(values)}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cli_workflow")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="Validate a workflow YAML document")
    p_val.add_argument("workflow")
    p_val.set_defaults(func=cmd_validate)

    p_gse = sub.add_parser("gse-eval", help="Evaluate a select JSON against a graph JSON")
    p_gse.add_argument("--graph", required=True)
    p_gse.add_argument("--select", required=True)
    p_gse.set_defaults(func=cmd_gse_file)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
