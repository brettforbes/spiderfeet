"""CLI entrypoints for workflow validate / GSE eval / dry helpers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from cli_workflow.core.gse_eval import eval_select
from cli_workflow.core.loader import load_workflow, topological_waves
from cli_workflow.runtime.executor import execute_workflow
from cli_workflow.tools.registry import FixtureDriver


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


def cmd_dry_run(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    doc = load_workflow(args.workflow, validate=True)
    fixture_map = yaml.safe_load(Path(args.fixtures).read_text(encoding="utf-8"))

    class _Runner:
        def run_step(self, step, input_values):  # noqa: ANN001
            rel = fixture_map[step["id"]]
            graph = json.loads((repo_root / rel).read_text(encoding="utf-8"))
            return {"scan_graph": graph, "exit_code": 0}

    result = execute_workflow(doc, _Runner())
    export_steps = [
        s["id"]
        for s in doc["steps"]
        if (s.get("context") or {}).get("export") == "scan_graph"
    ]
    print(f"OK dry-run: steps={len(result.steps)} context_nodes={len(result.context['nodes'])}")
    print(f"export_steps={export_steps}")
    for sid, sr in result.steps.items():
        print(f"  {sid}: vars={list(sr.vars.keys())} input_count={len(sr.input_values)}")
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

    p_dry = sub.add_parser("dry-run", help="Execute workflow using fixture scan graphs (no CLI)")
    p_dry.add_argument("--workflow", required=True)
    p_dry.add_argument("--fixtures", required=True)
    p_dry.add_argument("--repo-root", default=".")
    p_dry.set_defaults(func=cmd_dry_run)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
