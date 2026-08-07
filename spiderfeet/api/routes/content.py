"""Content platform routes (SPEC-008 R8-04)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from spiderfeet.api.services import content as content_service

router = APIRouter(prefix="/content", tags=["content"])


class ContentToolSummary(BaseModel):
    tool_id: str
    display_name: str
    kind: str = "cli"
    category: str | None = None


class ContentToolsResponse(BaseModel):
    tools: list[ContentToolSummary]
    total: int
    limit: int
    offset: int


class MarkdownDocument(BaseModel):
    markdown: str


@router.get("/tools", response_model=ContentToolsResponse)
def list_content_tools(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> ContentToolsResponse:
    payload = content_service.list_tools(limit=limit, offset=offset)
    return ContentToolsResponse(**payload)


@router.get("/tools/{tool_id}")
def get_tool_manifest(tool_id: str) -> dict[str, Any]:
    manifest = content_service.get_manifest(tool_id)
    if manifest is None:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_id}")
    return manifest


@router.get("/tools/{tool_id}/options", response_model=MarkdownDocument)
def get_tool_options(tool_id: str) -> MarkdownDocument:
    markdown = content_service.get_options_markdown(tool_id)
    if markdown is None:
        raise HTTPException(status_code=404, detail=f"Options not found for tool: {tool_id}")
    return MarkdownDocument(markdown=markdown)


@router.get("/tools/{tool_id}/options-schema")
def get_tool_options_schema(tool_id: str) -> dict[str, Any]:
    schema = content_service.get_options_schema(tool_id)
    if schema is None:
        raise HTTPException(status_code=404, detail=f"Options schema not found for tool: {tool_id}")
    return schema


@router.get("/tools/{tool_id}/zero-to-hero", response_model=MarkdownDocument)
def get_tool_zero_to_hero(tool_id: str) -> MarkdownDocument:
    markdown = content_service.get_zero_to_hero_markdown(tool_id)
    if markdown is None:
        raise HTTPException(status_code=404, detail=f"Zero-to-Hero not found for tool: {tool_id}")
    return MarkdownDocument(markdown=markdown)


@router.get("/tools/{tool_id}/graph-structure", response_model=MarkdownDocument)
def get_tool_graph_structure(tool_id: str) -> MarkdownDocument:
    markdown = content_service.get_graph_structure_markdown(tool_id)
    if markdown is None:
        raise HTTPException(status_code=404, detail=f"Graph structure not found for tool: {tool_id}")
    return MarkdownDocument(markdown=markdown)
