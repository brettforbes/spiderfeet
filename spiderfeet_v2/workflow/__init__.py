"""Workflow DSL + GSE runtime for SpiderFeet v2 (SPEC-010 AM1/AM2).

Ported and extended from ``.seed/scripts/cli_workflow/`` (SPEC-007).
Canonical authoring shape: ``.seed/12A_Workflow_YAML_Example.yaml``.
AM2: YAML-DSL ↔ TypeDB conversion via ``typedb_convert``.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "WorkflowLoadError",
    "VariableError",
    "GseError",
    "StepCommand",
    "load_workflow",
    "validate_workflow_dict",
    "validate_gse_binding",
    "topological_waves",
    "schedule_waves",
    "workflow_input_values",
    "resolve_step_input",
    "resolve_step_inputs",
    "build_env",
    "build_step_command",
    "eval_binding",
    "eval_select",
    "evaluate_output_vars",
    "normalize_list",
    "hostname_from_url",
    "TempFileManager",
    "WorkflowConvertError",
    "TypedbWorkflowForms",
    "yaml_to_typedb_forms",
    "typedb_forms_to_yaml",
    "typedb_to_api_json",
    "persist_workflow_yaml",
    "load_workflow_yaml",
    "load_workflow_api_json",
    "workflows_equal",
    "dump_canonical_yaml",
]


def __getattr__(name: str) -> Any:
    if name in (
        "WorkflowLoadError",
        "load_workflow",
        "validate_workflow_dict",
        "validate_gse_binding",
        "topological_waves",
        "schedule_waves",
        "workflow_input_values",
    ):
        from spiderfeet_v2.workflow import loader as _loader

        return getattr(_loader, name)
    if name in ("VariableError", "resolve_step_input", "build_env"):
        from spiderfeet_v2.workflow import variables as _variables

        return getattr(_variables, name)
    if name == "resolve_step_inputs":
        from spiderfeet_v2.workflow.inputs import resolve_step_inputs

        return resolve_step_inputs
    if name in ("StepCommand", "build_step_command"):
        from spiderfeet_v2.workflow import argv as _argv

        return getattr(_argv, name)
    if name in ("GseError", "eval_binding", "eval_select", "evaluate_output_vars"):
        from spiderfeet_v2.workflow import gse_eval as _gse

        return getattr(_gse, name)
    if name in ("normalize_list", "hostname_from_url"):
        from spiderfeet_v2.workflow import normalize as _normalize

        return getattr(_normalize, name)
    if name == "TempFileManager":
        from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager

        return TempFileManager
    if name in (
        "WorkflowConvertError",
        "TypedbWorkflowForms",
        "yaml_to_typedb_forms",
        "typedb_forms_to_yaml",
        "typedb_to_api_json",
        "persist_workflow_yaml",
        "load_workflow_yaml",
        "load_workflow_api_json",
        "workflows_equal",
        "dump_canonical_yaml",
    ):
        from spiderfeet_v2.workflow import typedb_convert as _convert

        return getattr(_convert, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name}")
