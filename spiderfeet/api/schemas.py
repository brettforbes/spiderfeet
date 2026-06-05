"""Request/response models for the public API."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

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
    poll: str = Field(
        ...,
        description="Poll this URL until status is FINISHED",
    )
    results: str = Field(
        ...,
        description="Fetch scan events here after FINISHED",
    )


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


# --- scan_ui (widget / TypeDB map model) ---

SCAN_UI_SWAGGER_EXAMPLE = {
    "module_id": "sfp_dnsresolve",
    "consumed": {
        "nugget_id": "INTERNET_NAME",
        "nugget_data": "sbs.com.au",
    },
    "wait": True,
    "timeout_seconds": 120,
}


class ConsumedNuggetInput(BaseModel):
    """Seed nugget the UI sends into a module."""

    nugget_id: str = Field(
        ...,
        description="Catalogue nugget_id / event type, e.g. INTERNET_NAME",
    )
    nugget_data: str = Field(
        ...,
        min_length=1,
        description="Target value (domain, IP, etc.)",
    )


class ScanUiRequest(BaseModel):
    """Run one module against a consumed nugget; return map-shaped scan record."""

    module_id: str = Field(..., description="OSINT module name, e.g. sfp_dnsresolve")
    consumed: ConsumedNuggetInput
    scan_name: Optional[str] = Field(
        None, description="Optional scan display name; defaults to nugget_data"
    )
    scan_notes: Optional[str] = Field("", description="Free-text notes for scan-record")
    wait: bool = Field(
        True,
        description="If true, block until scan finishes or timeout (default for UI)",
    )
    timeout_seconds: int = Field(120, ge=5, le=600)
    debug: bool = False

    model_config = ConfigDict(json_schema_extra={"example": SCAN_UI_SWAGGER_EXAMPLE})


SCAN_UI_OPENAPI_EXAMPLES = {
    "dns_from_domain": {
        "summary": "DNS Resolver on sbs.com.au",
        "description": (
            "Consumes an INTERNET_NAME nugget and runs sfp_dnsresolve. "
            "Returns scan-record fields plus produced nuggets (IP_ADDRESS, etc.)."
        ),
        "value": SCAN_UI_SWAGGER_EXAMPLE,
    },
}


class OsintServiceRef(BaseModel):
    module_id: str
    name: str


class RouteRef(BaseModel):
    route_name: Optional[str] = None
    route_state: Optional[str] = None


class ScanRecordUi(BaseModel):
    """Mirrors TypeDB scan-record relation (`.seed/spiderfeet_map.tql`)."""

    scan_instance_id: str
    scan_status: str = Field(
        ...,
        description="Scan lifecycle status (also duplicated in scan_results.status)",
        alias="status",
    )
    scan_event_count: int = Field(
        0,
        description="Total events in this scan instance",
    )
    scan_results_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Event type → count (e.g. IP_ADDRESS: 2)",
    )
    scan_results: Dict[str, Any] = Field(
        ...,
        description="Bundled summary: status, event_count, by_type",
    )
    scan_duration: Optional[float] = Field(
        None, description="Seconds between started and ended"
    )
    scan_timestamp: Optional[str] = Field(
        None, description="ISO-8601 UTC from scan start"
    )
    scan_notes: str = ""
    service: OsintServiceRef = Field(
        ...,
        description="Linked osint-service (scan-record:service role)",
    )
    route: Optional[RouteRef] = Field(
        None,
        description="Linked route under test (scan-record:route role)",
    )

    model_config = ConfigDict(populate_by_name=True)


class NuggetInstance(BaseModel):
    """Nugget entity instance aligned with TypeDB map attributes."""

    nugget_id: str
    nugget_instance_id: str
    entity_type: str
    nugget_description: Optional[str] = None
    nugget_type: Optional[str] = None
    nugget_event_type: str
    nugget_icon: Optional[str] = None
    nugget_colour: Optional[str] = None
    nugget_data: str
    nugget_source_data: Optional[str] = None
    nugget_module: str
    nugget_generated: int
    nugget_confidence: int
    nugget_visibility: int
    nugget_risk: int
    nugget_false_positive: bool = False


class ScanUiResponse(BaseModel):
    scan_record: ScanRecordUi
    consumed: List[NuggetInstance]
    produced: List[NuggetInstance]


class MapConnectionInfo(BaseModel):
    database: str
    addresses: List[str]
    username: str
    tls_enabled: bool = False
    configured: bool = True


class MapConnectionPingResponse(BaseModel):
    reachable: bool
    database: str


class MapInventoryCounts(BaseModel):
    nugget_count: int
    service_count: int
    link_count: int


class MapStatusResponse(BaseModel):
    database: str
    reachable: bool
    inventory: Optional[MapInventoryCounts] = None


class MapBootstrapResponse(BaseModel):
    database: str
    created_database: bool
    applied_schema: bool
    nuggets_inserted: int
    nuggets_skipped: int
    services_inserted: int
    services_skipped: int
    services_failed: int
    links_added: int
    ok: bool
    errors: List[str]

    @classmethod
    def from_report(cls, report) -> "MapBootstrapResponse":
        return cls(
            database=report.database,
            created_database=report.created_database,
            applied_schema=report.applied_schema,
            nuggets_inserted=report.nuggets_inserted,
            nuggets_skipped=report.nuggets_skipped,
            services_inserted=report.services_inserted,
            services_skipped=report.services_skipped,
            services_failed=report.services_failed,
            links_added=report.links_added,
            ok=report.ok,
            errors=list(report.errors),
        )


class ForceGraphNodeModel(BaseModel):
    id: str
    kind: str
    label: str
    colour: Optional[str] = None
    service_state: Optional[str] = None


class ForceGraphLinkModel(BaseModel):
    source: str
    target: str
    role: str


class MapForceGraphResponse(BaseModel):
    nodes: List[ForceGraphNodeModel]
    links: List[ForceGraphLinkModel]


class TestsSummaryResponse(BaseModel):
    module_count: int
    route_count: int
    consumption_group_count: int
    typedb_connected: bool = False
    route_states: Dict[str, int] = Field(
        default_factory=dict,
        description="Counts by route_state (not_started, in_test, favourite, …)",
    )


class TestsModuleSummary(BaseModel):
    module_id: str
    name: str
    summary: str
    consumption_group: str
    access_tier: str
    route_count: int
    routes_tested: int = Field(
        0,
        description="Routes with a non-not-started state in TypeDB (when connected)",
    )


class RouteCatalogItem(BaseModel):
    route_name: str
    consumed_nugget_id: str
    produced_nugget_id: str
    route_state: str = "not-started"


class TestsModuleDetail(BaseModel):
    module_id: str
    name: str
    summary: str
    consumption_group: str
    access_tier: str
    route_seed_nugget: Optional[str] = None
    route_count: int
    routes: List[RouteCatalogItem]
