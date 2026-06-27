"""Settings API routes — CLI app paths and AI agent keys."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from spiderfeet.api.bootstrap import Runtime, get_runtime
from spiderfeet.api.schemas_settings import (
    AiAgentCreate,
    AiAgentSummary,
    AiAgentUpdate,
    CliAppSetting,
    CliAppSettingsUpdate,
)
from spiderfeet.settings import ai_agents, cli_apps

router = APIRouter(prefix="/settings", tags=["settings"])


def runtime_dep() -> Runtime:
    return get_runtime()


@router.get("/cli-apps", response_model=List[CliAppSetting])
def get_cli_apps(runtime: Runtime = Depends(runtime_dep)) -> List[CliAppSetting]:
    rows = cli_apps.list_cli_apps(runtime.config)
    return [CliAppSetting(**row) for row in rows]


@router.put("/cli-apps", response_model=List[CliAppSetting])
def put_cli_apps(
    body: CliAppSettingsUpdate,
    runtime: Runtime = Depends(runtime_dep),
) -> List[CliAppSetting]:
    try:
        rows = cli_apps.update_cli_apps([app.model_dump() for app in body.apps])
        return [CliAppSetting(**row) for row in rows]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/ai-agents", response_model=List[AiAgentSummary])
def get_ai_agents() -> List[AiAgentSummary]:
    return [AiAgentSummary(**row) for row in ai_agents.list_ai_agents()]


@router.post("/ai-agents", response_model=AiAgentSummary)
def post_ai_agent(body: AiAgentCreate) -> AiAgentSummary:
    try:
        row = ai_agents.create_ai_agent(body.model_dump())
        return AiAgentSummary(**row)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.put("/ai-agents/{agent_id}", response_model=AiAgentSummary)
def put_ai_agent(agent_id: str, body: AiAgentUpdate) -> AiAgentSummary:
    try:
        payload = {k: v for k, v in body.model_dump().items() if v is not None}
        row = ai_agents.update_ai_agent(agent_id, payload)
        return AiAgentSummary(**row)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/ai-agents/{agent_id}", status_code=204)
def delete_ai_agent(agent_id: str) -> None:
    try:
        ai_agents.delete_ai_agent(agent_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
