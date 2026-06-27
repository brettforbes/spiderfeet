"""Settings API schemas."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class CliAppSetting(BaseModel):
    tool_id: str
    display_name: str = ""
    binary_path: str
    runtime: str = "windows"
    env_file: Optional[str] = None
    enabled: bool = True


class CliAppSettingsUpdate(BaseModel):
    apps: List[CliAppSetting]


class AiAgentSummary(BaseModel):
    id: str
    label: str
    provider: str
    model: str = ""
    enabled: bool = True
    has_api_key: bool = False
    masked_api_key: Optional[str] = None


class AiAgentCreate(BaseModel):
    label: str
    provider: str = "custom"
    model: str = ""
    api_key: str = ""
    enabled: bool = True


class AiAgentUpdate(BaseModel):
    label: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    enabled: Optional[bool] = None
