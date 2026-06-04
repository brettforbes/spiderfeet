"""Request/response models for the public API."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class UseCase(str, Enum):
    all = "all"
    footprint = "footprint"
    investigate = "investigate"
    passive = "passive"


class ModuleInfo(BaseModel):
    name: str
    description: str


class EventTypeInfo(BaseModel):
    name: str
    description: str


class ScanCreateRequest(BaseModel):
    target: str = Field(..., min_length=1, description="Scan target (domain, IP, etc.)")
    scan_name: Optional[str] = Field(
        None, description="Display name; defaults to target"
    )
    modules: Optional[List[str]] = Field(
        None, description="Module names (sfp_*), same as sf.py -m"
    )
    event_types: Optional[List[str]] = Field(
        None, description="Event types; expands module list like sf.py -t"
    )
    use_case: Optional[UseCase] = Field(
        None, description="Module group: all, footprint, investigate, passive"
    )
    debug: bool = False

    @model_validator(mode="after")
    def require_module_selection(self) -> "ScanCreateRequest":
        if not self.modules and not self.event_types and not self.use_case:
            raise ValueError(
                "At least one of modules, event_types, or use_case is required"
            )
        return self


class ScanCreateResponse(BaseModel):
    scan_id: str
    status: str = "STARTING"


class ScanSummary(BaseModel):
    scan_id: str
    name: str
    target: str
    created: Optional[int] = None
    started: Optional[int] = None
    ended: Optional[int] = None
    status: str
    result_count: int = 0


class ScanDetail(BaseModel):
    scan_id: str
    name: str
    target: str
    created: Optional[int] = None
    started: Optional[int] = None
    ended: Optional[int] = None
    status: str


class ScanResultItem(BaseModel):
    generated: int
    data: str
    source_data: Optional[str] = None
    module: str
    type: str
    confidence: int
    visibility: int
    risk: int
    event_description: Optional[str] = None
    false_positive: bool = False
