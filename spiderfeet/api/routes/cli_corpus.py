"""CLI corpus review endpoints for the widget Profiling tab."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from spiderfeet.api.services import cli_corpus as corpus_service

router = APIRouter(prefix="/cli-corpus", tags=["cli-corpus"])


class CliCorpusConfigResponse(BaseModel):
    data_viewer_url: str
    corpus_index_path: str


class CliCorpusToolSummary(BaseModel):
    id: str
    phase: str = "pending"
    priority: int | None = None
    runtime: str | None = None
    exam_count: int = 0
    has_graph_structure: bool = False
    notes: str | None = None


class CliCorpusScenarioSummary(BaseModel):
    scenario_key: str
    scenario_name: str | None = None
    target: str | None = None
    runtime: str | None = None
    structured_kind: str | None = None
    review_status: str = "pending"
    legacy_exam_ids: list[int] = Field(default_factory=list)
    has_text: bool = False
    has_structured: bool = False
    has_graph: bool = False
    has_markdown: bool = False
    complete: bool = False
    exam_id: int | None = None
    scenario_id: str | None = None


class CliCorpusStructuredPayload(BaseModel):
    format: str
    filename: str
    content: str


class CliCorpusArtifacts(BaseModel):
    has_text: bool = False
    has_structured: bool = False
    has_graph: bool = False
    has_markdown: bool = False


class CliCorpusScenarioDetail(BaseModel):
    tool_id: str
    scenario_key: str
    exam_id: int | None = None
    manifest: dict
    review_status: str
    command: str = ""
    output_text: str = ""
    structured: CliCorpusStructuredPayload | None = None
    graph_proposal: dict | None = None
    graph_description_markdown: str | None = None
    markdown: str | None = None
    artifacts: CliCorpusArtifacts
    complete: bool = False


class CliCorpusMarkdownDocument(BaseModel):
    tool_id: str
    filename: str
    markdown: str


class CliCorpusReviewRequest(BaseModel):
    status: str = Field(..., pattern="^(pending|approved|rejected)$")


class CliCorpusReviewResponse(BaseModel):
    status: str
    scenario_key: str
    tool: str
    updated_at: str


@router.get("/config", response_model=CliCorpusConfigResponse)
def cli_corpus_config() -> CliCorpusConfigResponse:
    """Embed URL and corpus paths for the Profiling tab."""
    return CliCorpusConfigResponse(**corpus_service.corpus_config())


@router.get("/tools", response_model=List[CliCorpusToolSummary])
def list_tools() -> List[CliCorpusToolSummary]:
    """All CLI tools tracked in corpus_index.json with scenario counts."""
    return [CliCorpusToolSummary(**row) for row in corpus_service.list_tools()]


@router.get("/tools/{tool_id}/scenarios", response_model=List[CliCorpusScenarioSummary])
def list_scenarios(tool_id: str) -> List[CliCorpusScenarioSummary]:
    """Logical scan scenarios for a tool (one row per command, not per file type)."""
    try:
        rows = corpus_service.list_scenarios(tool_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not rows and not corpus_service.tool_in_index(tool_id):
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_id}")
    return [CliCorpusScenarioSummary(**row) for row in rows]


@router.get("/tools/{tool_id}/graph-structure", response_model=CliCorpusMarkdownDocument)
def get_tool_graph_structure(tool_id: str) -> CliCorpusMarkdownDocument:
    """Tool-level nugget graph structure markdown."""
    try:
        doc = corpus_service.get_tool_graph_structure(tool_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Graph structure not found: {tool_id}")
    return CliCorpusMarkdownDocument(**doc)


@router.get("/tools/{tool_id}/scenarios/{scenario_key}", response_model=CliCorpusScenarioDetail)
def get_scenario(tool_id: str, scenario_key: str) -> CliCorpusScenarioDetail:
    """Full scenario bundle for review panes (text, structured, graph, markdown)."""
    try:
        detail = corpus_service.get_scenario(tool_id, scenario_key)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if detail is None:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario not found: {tool_id}/{scenario_key}",
        )
    return CliCorpusScenarioDetail(**detail)


@router.post(
    "/tools/{tool_id}/scenarios/{scenario_key}/review",
    response_model=CliCorpusReviewResponse,
)
def set_scenario_review(
    tool_id: str, scenario_key: str, body: CliCorpusReviewRequest
) -> CliCorpusReviewResponse:
    """Update review status for a scenario bundle."""
    try:
        result = corpus_service.set_review_status(tool_id, scenario_key, body.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CliCorpusReviewResponse(**result)


# Backward-compatible aliases (exam_id resolves to merged scenario)
@router.get("/tools/{tool_id}/examinations", response_model=List[CliCorpusScenarioSummary])
def list_examinations(tool_id: str) -> List[CliCorpusScenarioSummary]:
    try:
        rows = corpus_service.list_examinations(tool_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not rows and not corpus_service.tool_in_index(tool_id):
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_id}")
    return [CliCorpusScenarioSummary(**row) for row in rows]


@router.get("/tools/{tool_id}/examinations/{exam_id}", response_model=CliCorpusScenarioDetail)
def get_examination(tool_id: str, exam_id: int) -> CliCorpusScenarioDetail:
    try:
        detail = corpus_service.get_examination(tool_id, exam_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if detail is None:
        raise HTTPException(
            status_code=404,
            detail=f"Examination not found: {tool_id}/{exam_id}",
        )
    return CliCorpusScenarioDetail(**detail)


@router.post(
    "/tools/{tool_id}/examinations/{exam_id}/review",
    response_model=CliCorpusReviewResponse,
)
def set_exam_review(tool_id: str, exam_id: int, body: CliCorpusReviewRequest) -> CliCorpusReviewResponse:
    try:
        result = corpus_service.set_review_status_by_exam(tool_id, exam_id, body.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CliCorpusReviewResponse(**result)
