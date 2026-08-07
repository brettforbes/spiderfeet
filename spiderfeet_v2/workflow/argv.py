"""Build argv arrays and materialize auto input/output files (argv-only, no shell)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager

_WORKFLOW_INPUT = re.compile(r"^\$workflow\.inputs\.([a-zA-Z_][a-zA-Z0-9_]*)$")
_INPUT_VALUE_INDEX = re.compile(r"^\$step\.input\.values\[(\d+)\]$")

_FORMAT_SUFFIX = {
    "line_text": ".txt",
    "jsonl": ".jsonl",
    "json": ".json",
    "xml": ".xml",
}


@dataclass
class StepCommand:
    """Resolved argv + optional temp file paths for one step."""

    argv: List[str]
    input_path: Optional[Path]
    output_path: Optional[Path]
    input_values: List[str]


def _suffix_for(fmt: str | None, *, default: str) -> str:
    if not fmt:
        return default
    return _FORMAT_SUFFIX.get(fmt, default)


def build_step_command(
    step: Mapping[str, Any],
    input_values: List[str],
    temps: TempFileManager,
    *,
    workflow_inputs: Mapping[str, List[str]] | None = None,
) -> StepCommand:
    """Materialize auto files and resolve argv placeholders to concrete strings.

    Placeholders:
    - ``$step.files.input`` / ``$step.files.output``
    - ``$step.input.values[N]``
    - ``$workflow.inputs.<name>`` (joined with comma when used as a single token)
    """
    config = step.get("config") or {}
    files_cfg = config.get("files") or {}
    workflow_inputs = workflow_inputs or {}

    input_path: Optional[Path] = None
    output_path: Optional[Path] = None

    inp_spec = files_cfg.get("input") or {}
    inp_mode = inp_spec.get("mode", "none")
    if inp_mode == "auto":
        input_path = temps.write_line_text(
            input_values,
            suffix=_suffix_for(inp_spec.get("format"), default=".txt"),
        )
    elif inp_mode == "path":
        raw = inp_spec.get("path")
        if not raw:
            raise ValueError(f"step {step.get('id')}: files.input.mode=path requires path")
        input_path = Path(raw)

    out_spec = files_cfg.get("output") or {}
    out_mode = out_spec.get("mode", "none")
    if out_mode == "auto":
        output_path = temps.allocate_output(
            suffix=_suffix_for(out_spec.get("format"), default=".out"),
        )
    elif out_mode == "path":
        raw = out_spec.get("path")
        if not raw:
            raise ValueError(f"step {step.get('id')}: files.output.mode=path requires path")
        output_path = Path(raw)

    placeholders: Dict[str, str] = {
        "$step.files.input": str(input_path) if input_path else "",
        "$step.files.output": str(output_path) if output_path else "",
    }

    argv_out: List[str] = []
    for token in config.get("argv") or []:
        if token in placeholders:
            resolved = placeholders[token]
            if not resolved:
                raise ValueError(
                    f"step {step.get('id')}: argv placeholder {token} has no materialized file"
                )
            argv_out.append(resolved)
            continue

        m_idx = _INPUT_VALUE_INDEX.match(token)
        if m_idx:
            idx = int(m_idx.group(1))
            if idx >= len(input_values):
                raise ValueError(
                    f"step {step.get('id')}: $step.input.values[{idx}] out of range "
                    f"(len={len(input_values)})"
                )
            argv_out.append(input_values[idx])
            continue

        m_wf = _WORKFLOW_INPUT.match(token)
        if m_wf:
            key = m_wf.group(1)
            if key not in workflow_inputs:
                raise ValueError(f"step {step.get('id')}: unknown {token}")
            argv_out.append(",".join(workflow_inputs[key]))
            continue

        argv_out.append(token)

    return StepCommand(
        argv=argv_out,
        input_path=input_path,
        output_path=output_path,
        input_values=list(input_values),
    )
