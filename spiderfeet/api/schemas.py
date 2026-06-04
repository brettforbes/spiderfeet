"""Request/response models for the public API."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

# Default Swagger / Try-it-out payload: one concrete OSINT module, not use_case.
SCAN_CREATE_SWAGGER_EXAMPLE = {
    "target": "sbs.com.au",
    "modules": ["sfp_dnsresolve"],
}


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
    """Start a new OSINT scan."""

    target: str = Field(
        ...,
        min_length=1,
        description="Scan target (domain, IP, email, etc.)",
    )
    scan_name: Optional[str] = Field(
        None, description="Display name; defaults to target"
    )
    modules: Optional[List[str]] = Field(
        None,
        description=(
            "OSINT module names (sfp_*). Prefer this over use_case for a focused scan. "
            "Example: sfp_dnsresolve (DNS Resolver) for a domain."
        ),
    )
    event_types: Optional[List[str]] = Field(
        None, description="Event types; expands module list like sf.py -t"
    )
    use_case: Optional[UseCase] = Field(
        None,
        description=(
            "Run all modules in a group (slow). Prefer modules for a single service."
        ),
    )
    debug: bool = False

    model_config = ConfigDict(json_schema_extra={"example": SCAN_CREATE_SWAGGER_EXAMPLE})

    @model_validator(mode="after")
    def require_module_selection(self) -> "ScanCreateRequest":
        if not self.modules and not self.event_types and not self.use_case:
            raise ValueError(
                "At least one of modules, event_types, or use_case is required"
            )
        return self


SCAN_CREATE_OPENAPI_EXAMPLES = {
    "dns_resolver": {
        "summary": "DNS Resolver on sbs.com.au",
        "description": (
            "Runs the sfp_dnsresolve module (DNS Resolver) against the domain. "
            "Produces IP_ADDRESS and related DNS events within seconds."
        ),
        "value": SCAN_CREATE_SWAGGER_EXAMPLE,
    },
}


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
