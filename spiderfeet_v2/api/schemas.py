"""Pydantic models + OpenAPI examples for v2 engine routes (R10-24)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Shared graph shapes
# ---------------------------------------------------------------------------


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    nugget_instance_id: Optional[str] = None
    nugget_id: Optional[str] = None
    nugget_data: Optional[str] = None
    temporary_id: Optional[str] = Field(
        default=None,
        description="Widget-only tag; stripped before persistence (R10-25).",
    )


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="allow")

    source: Optional[str] = None
    target: Optional[str] = None
    relation: Optional[str] = None
    # Viewer may send from/to/type while temporary_ids are active
    type: Optional[str] = None


class GraphPayload(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------


class TargetCreate(BaseModel):
    target_id: str = Field(..., examples=["target--example-com"])
    target_value: Optional[str] = Field(None, examples=["example.com"])
    target_description: Optional[str] = None
    target_created: Optional[str] = None
    target_yaml: Optional[str] = None


class TargetUpdate(BaseModel):
    target_value: Optional[str] = None
    target_description: Optional[str] = None
    target_created: Optional[str] = None
    target_yaml: Optional[str] = None


class TargetOut(BaseModel):
    model_config = ConfigDict(extra="allow")

    target_id: str
    target_value: Optional[str] = None
    target_description: Optional[str] = None
    target_created: Optional[str] = None
    target_yaml: Optional[str] = None


TARGET_CREATE_EXAMPLE = {
    "target_id": "target--example-com",
    "target_value": "example.com",
    "target_description": "Permissive lab target",
    "target_yaml": "value: example.com\n",
}

TARGET_CREATE_OPENAPI_EXAMPLES = {
    "lab": {
        "summary": "Lab hostname target",
        "value": TARGET_CREATE_EXAMPLE,
    }
}


# ---------------------------------------------------------------------------
# Workflows
# ---------------------------------------------------------------------------


class WorkflowCreate(BaseModel):
    workflow_id: str = Field(..., examples=["workflow--recon-12a"])
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    workflow_yaml: Optional[str] = None
    target_id: Optional[str] = None
    first_step_id: Optional[str] = None
    prior_step_ids: Optional[List[str]] = None
    next_step_ids: Optional[List[str]] = None


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    workflow_yaml: Optional[str] = None
    target_id: Optional[str] = None
    first_step_id: Optional[str] = None
    prior_step_ids: Optional[List[str]] = None
    next_step_ids: Optional[List[str]] = None


class WorkflowOut(BaseModel):
    model_config = ConfigDict(extra="allow")

    workflow_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    workflow_yaml: Optional[str] = None
    target_id: Optional[str] = None
    first_step_id: Optional[str] = None
    prior_step_ids: Optional[List[str]] = None
    next_step_ids: Optional[List[str]] = None


class WorkflowProjectionOut(BaseModel):
    """AL3 projection shape for a workflow."""

    model_config = ConfigDict(extra="allow")

    workflow_id: str
    target: Optional[str] = None
    first_step: Optional[str] = None
    prior_step: List[str] = Field(default_factory=list)
    next_step: List[str] = Field(default_factory=list)
    workflow_yaml: Optional[str] = None


WORKFLOW_CREATE_EXAMPLE = {
    "workflow_id": "workflow--recon-12a",
    "name": "12A recon",
    "description": "Split-branch recon workflow",
    "author": "spiderfeet",
    "workflow_yaml": "apiVersion: spiderfeet.workflow/v1\nkind: Workflow\n",
    "target_id": "target--example-com",
}

WORKFLOW_CREATE_OPENAPI_EXAMPLES = {
    "with_target": {
        "summary": "Workflow linked to a target",
        "value": WORKFLOW_CREATE_EXAMPLE,
    }
}


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


class ProjectCreate(BaseModel):
    """Create a project.

    When ``workflow_ids`` is empty/omitted, the server creates an info-only
    workflow linked to the project (R13-04). When ``workflow_ids`` is provided,
    those existing workflows are linked instead (no new YAML generated).
    """

    project_id: Optional[str] = Field(
        None,
        examples=["project--demo"],
        description="Optional; server generates ``project--<uuid>`` when omitted.",
    )
    project_name: Optional[str] = Field(None, examples=["Demo Project"])
    project_description: Optional[str] = Field(
        None, examples=["A project to scan the target domain"]
    )
    project_created: Optional[str] = Field(
        None,
        examples=["2026-08-09T10:00:00Z"],
        description="ISO-8601 datetime; server supplies when omitted.",
    )
    stix_incident_id: Optional[str] = None
    workflow_ids: List[str] = Field(
        default_factory=list,
        examples=[["workflow--recon-12a"]],
        description=(
            "Optional. Empty/omitted → create info-only workflow (R13-04). "
            "Non-empty → link existing workflows only."
        ),
    )


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    project_created: Optional[str] = None
    stix_incident_id: Optional[str] = None
    workflow_ids: Optional[List[str]] = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(extra="allow")

    project_id: str
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    project_created: Optional[str] = None
    stix_incident_id: Optional[str] = None
    workflow_ids: List[str] = Field(
        default_factory=list,
        description="Workflow ids that link this project (derived).",
    )
    primary_workflow_id: Optional[str] = Field(
        None,
        description="Set on create-new-project (R13-04) to the info-only workflow id.",
    )
    workflow_yaml: Optional[str] = Field(
        None,
        description="Info-only YAML returned on create-new-project for Composer load.",
    )


class ProjectProjectionOut(BaseModel):
    """AL3 projection: workflows/targets/context ids + CRUD project attrs."""

    model_config = ConfigDict(extra="allow")

    project_id: str
    workflows: List[str] = Field(default_factory=list)
    targets: List[str] = Field(default_factory=list)
    project_context: List[str] = Field(default_factory=list)
    temporary_subgraph: List[str] = Field(default_factory=list)
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    project_created: Optional[str] = None
    stix_incident_id: Optional[str] = None


class ProjectCompleteStepSummary(BaseModel):
    """Parsed step summary for Composer one-call load (R13-06)."""

    model_config = ConfigDict(extra="allow")

    scan_instance_id: str
    step_module_id: Optional[str] = None
    scan_status: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    missing: Optional[bool] = None


class ProjectCompleteWorkflow(BaseModel):
    """Workflow attrs + inline YAML + step/target summary (R13-06)."""

    model_config = ConfigDict(extra="allow")

    workflow_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None
    workflow_yaml: Optional[str] = None
    project_id: Optional[str] = None
    target_id: Optional[str] = None
    first_step_id: Optional[str] = None
    prior_step_ids: List[str] = Field(default_factory=list)
    next_step_ids: List[str] = Field(default_factory=list)
    steps: List[ProjectCompleteStepSummary] = Field(default_factory=list)
    target: Optional[Dict[str, Any]] = None


class ProjectCompleteOut(BaseModel):
    """``GET /projects/{id}/complete`` response (R13-06)."""

    model_config = ConfigDict(extra="allow")

    project: ProjectOut
    workflows: List[ProjectCompleteWorkflow] = Field(default_factory=list)


PROJECT_CREATE_EXAMPLE = {
    "project_id": "project--demo",
    "project_name": "Demo Project",
    "project_description": "A project to scan the target domain",
    "project_created": "2026-08-09T10:00:00Z",
    "stix_incident_id": "incident--demo",
    "workflow_ids": ["workflow--recon-12a"],
}

PROJECT_CREATE_OPENAPI_EXAMPLES = {
    "demo": {
        "summary": "Project with one workflow",
        "value": PROJECT_CREATE_EXAMPLE,
    },
    "standalone": {
        "summary": "Standalone project (no workflows yet)",
        "value": {
            "project_id": "project--new",
            "project_name": "New Project",
            "project_description": "Info-only; workflow added later",
            "project_created": "2026-08-09T10:00:00Z",
        },
    },
}


# ---------------------------------------------------------------------------
# Scan steps (four forms)
# ---------------------------------------------------------------------------


class ScanStepOut(BaseModel):
    """Four UI forms + consumed/produced (AL3 projection + CRUD attrs)."""

    model_config = ConfigDict(extra="allow")

    scan_instance_id: str
    cli_command: Optional[str] = None
    text_form: Optional[str] = None
    structured_form: Optional[str] = None
    graph_form: Optional[str] = None
    markdown_narrative_form: Optional[str] = None
    consumed: List[str] = Field(default_factory=list)
    produced: List[str] = Field(default_factory=list)
    scan_result_graph: List[str] = Field(default_factory=list)
    # CRUD extras when available
    step_module_id: Optional[str] = None
    scan_status: Optional[str] = None
    scan_ui_structured_form_type: Optional[str] = None


# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------


class ContextGraphOut(BaseModel):
    project_id: str
    kind: str
    subgraph_id: Optional[str] = None
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    json_string: Optional[str] = None


class TemporarySubgraphOut(BaseModel):
    """One TypeDB temporary_subgraph row for the Temporary Subgraph Viewer."""

    temporary_subgraph_id: str
    scan_name: Optional[str] = None
    scan_description: Optional[str] = None
    produced_at: Optional[str] = Field(
        default=None,
        description="UTC ISO timestamp when the temp row was produced (chip order).",
    )
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)


class TemporaryContextListOut(BaseModel):
    """SPEC-017 list of all temporary subgraphs for a project."""

    project_id: str
    subgraphs: List[TemporarySubgraphOut] = Field(default_factory=list)


class TemporaryContextUpdate(BaseModel):
    """Deprecated: engine owns temporary writes (SPEC-017 R17-04)."""

    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    temporary_subgraph_id: Optional[str] = Field(
        default=None,
        description="Ignored — PUT temporary context is deprecated.",
    )


TEMPORARY_CONTEXT_UPDATE_EXAMPLE = {
    "temporary_subgraph_id": "temporary-subgraph--demo",
    "nodes": [
        {
            "id": "DOMAIN_NAME--example-com",
            "nugget_instance_id": "DOMAIN_NAME--example-com",
            "nugget_id": "DOMAIN_NAME",
            "nugget_data": "example.com",
            "temporary_id": "temporary--11111111-1111-4111-8111-111111111111",
        },
        {
            "id": "IPV4_ADDRESS--93-184-216-34",
            "nugget_instance_id": "IPV4_ADDRESS--93-184-216-34",
            "nugget_id": "IPV4_ADDRESS",
            "nugget_data": "93.184.216.34",
            "temporary_id": "temporary--22222222-2222-4222-8222-222222222222",
        },
    ],
    "edges": [
        {
            "source": "temporary--11111111-1111-4111-8111-111111111111",
            "target": "temporary--22222222-2222-4222-8222-222222222222",
            "relation": "resolves-to",
        }
    ],
}

TEMPORARY_CONTEXT_UPDATE_OPENAPI_EXAMPLES = {
    "with_temporary_ids": {
        "summary": "Viewer graph with temporary_id tags (stripped on persist)",
        "value": TEMPORARY_CONTEXT_UPDATE_EXAMPLE,
    }
}


# ---------------------------------------------------------------------------
# Execute (AO1 single-step; AO2 full-workflow chaining)
# ---------------------------------------------------------------------------


class ExecuteWorkflowRequest(BaseModel):
    project_id: Optional[str] = None
    dry_run: bool = False


class ExecuteStepRequest(BaseModel):
    project_id: Optional[str] = None
    step_id: Optional[str] = Field(
        default=None,
        description="DSL step id when path param is the scan_instance_id.",
    )
    dry_run: bool = False


class ExecuteAsyncAccepted(BaseModel):
    """202 Accepted body for SPEC-015 async execute (R15-01 / R15-03)."""

    run_id: str
    workflow_id: str
    state: str = Field(..., examples=["queued"])
    kind: str = Field(default="workflow", examples=["workflow", "step"])
    step_id: Optional[str] = None
    message: str = "Workflow execute accepted; poll GET /workflows/{id}/status"


class WorkflowStepStatusOut(BaseModel):
    step_id: str
    scan_instance_id: str
    scan_status: str = Field(
        ...,
        examples=["UNKNOWN", "STARTING", "RUNNING", "FINISHED", "ERROR-FAILED"],
    )
    input_total: Optional[int] = Field(
        default=None,
        description="Resolved input count for batched CLI (n); omit when UNKNOWN.",
    )
    input_done: Optional[int] = Field(
        default=None,
        description="Inputs completed (0 while RUNNING; n when FINISHED/skipped).",
    )


class WorkflowStatusOut(BaseModel):
    """Live per-step scan_status for DAG progress (SPEC-015 R15-02)."""

    workflow_id: str
    run_id: Optional[str] = None
    run_state: Optional[str] = None
    error: Optional[str] = Field(
        default=None,
        description="Registry error message when run_state is error/cancelled.",
    )
    steps: List[WorkflowStepStatusOut] = Field(default_factory=list)


class ExecuteResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str = Field(
        ..., examples=["SUCCESS", "ERROR", "DRY_RUN", "SKIPPED"]
    )
    message: str
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    scan_instance_id: Optional[str] = None
    orchestrator: str = Field(
        default="ao1",
        description="ao1 for single-step; ao2 for full-workflow chaining.",
    )
    module_id: Optional[str] = None
    scan_status: Optional[str] = None
    output_vars: Optional[Dict[str, Any]] = None
    exported_to_temporary: Optional[bool] = None
    temporary_subgraph_id: Optional[str] = None
    scan_result_id: Optional[str] = None
    counts: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    dry_run: Optional[bool] = None
    command: Optional[List[str]] = None
    input_values: Optional[List[str]] = None
    waves: Optional[List[List[str]]] = None
    steps: Optional[List[Dict[str, Any]]] = None
    step_count: Optional[int] = None
    succeeded: Optional[int] = None
    failed: Optional[int] = None
    skipped: Optional[int] = None
    stopped_early: Optional[bool] = None


EXECUTE_WORKFLOW_EXAMPLE = {"project_id": "project--demo", "dry_run": True}
EXECUTE_STEP_EXAMPLE = {
    "project_id": "project--demo",
    "step_id": "sfp_cli_subfinder",
    "dry_run": True,
}

EXECUTE_WORKFLOW_OPENAPI_EXAMPLES = {
    "dry_run": {
        "summary": "Dry-run full-workflow chaining (AO2)",
        "value": EXECUTE_WORKFLOW_EXAMPLE,
    },
    "live": {
        "summary": "Live full-workflow execute (AO2)",
        "value": {"project_id": "project--demo", "dry_run": False},
    },
}

EXECUTE_STEP_OPENAPI_EXAMPLES = {
    "dry_run": {
        "summary": "Dry-run single-step resolve (AO1)",
        "value": EXECUTE_STEP_EXAMPLE,
    },
    "live": {
        "summary": "Live single-step execute (AO1)",
        "value": {
            "project_id": "project--demo",
            "step_id": "sfp_cli_subfinder",
            "dry_run": False,
        },
    },
}
