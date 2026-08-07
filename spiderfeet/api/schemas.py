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


class ScanLogEntry(BaseModel):
    """One row from tbl_scan_log (CherryPy /scanlog parity)."""

    generated_ms: int
    component: Optional[str] = None
    type: str = Field(..., description="Log classification (INFO, ERROR, STATUS, …)")
    message: str
    row_id: Optional[int] = None


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


class ModuleExecutionSummary(BaseModel):
    """Per-module outcome inferred from scan events and logs (Stage 4c — R2-04-08)."""

    module_id: str
    status: str = Field(
        ...,
        description="Terminal or in-flight scan status for this run",
    )
    events_emitted: int = Field(
        0,
        description="Result events emitted by the target module (excludes storage/UI)",
    )
    verdict: str = Field(
        ...,
        description=(
            "clean_miss | hit | error_failed | incomplete | absent_violation"
        ),
    )
    absent_violations: List[str] = Field(
        default_factory=list,
        description="expected_absent_types that appeared in scan_results_by_type",
    )


class ScanUiResponse(BaseModel):
    scan_record: ScanRecordUi
    consumed: List[NuggetInstance]
    produced: List[NuggetInstance]
    module_execution: Optional[ModuleExecutionSummary] = Field(
        None,
        description="Inferred module outcome for pass/fail (negative fixture support)",
    )


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
    reachable: bool = Field(
        ...,
        description="TypeDB server accepts a connection (same as server_reachable)",
    )
    server_reachable: bool = Field(
        ...,
        description="TypeDB server accepts a connection",
    )
    database_ready: bool = Field(
        False,
        description=(
            "Map database exists with schema and seeded catalogue "
            "(nuggets and OSINT services)"
        ),
    )
    bootstrapped: bool = Field(
        False,
        description=(
            "True when this status check auto-created, schema-loaded, "
            "or re-seeded the map DB"
        ),
    )
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
    service_origin: Optional[str] = Field(
        None,
        description="external-api | cli | local — how the service runs",
    )
    fixture_category: Optional[str] = Field(
        None,
        description="positive | negative — module fixture semantics",
    )
    requires_api_key: Optional[bool] = Field(
        None,
        description="True when module needs subscription/API credentials before tests can run",
    )
    icon: Optional[str] = Field(
        None,
        description="Nugget icon filename (e.g. icon_domain_name.svg)",
    )
    fav_icon: Optional[str] = Field(
        None,
        description="OSINT service favicon URL from data_source.fav_icon",
    )


class ForceGraphLinkModel(BaseModel):
    source: str
    target: str
    role: str


class MapForceGraphResponse(BaseModel):
    nodes: List[ForceGraphNodeModel]
    links: List[ForceGraphLinkModel]


class TestsSummaryResponse(BaseModel):
    module_count: int
    test_count: int = Field(..., description="Executable tests (one per module × consumed nugget)")
    route_count: int = Field(
        ...,
        description="Full route matrix size (consumed × produced) for map coverage metrics",
    )
    consumption_group_count: int
    typedb_connected: bool = False
    test_states: Dict[str, int] = Field(
        default_factory=dict,
        description="Counts by aggregated test state (not_started, in_test, favourite, …)",
    )
    route_states: Dict[str, int] = Field(
        default_factory=dict,
        description="Deprecated alias of test_states for older clients",
    )
    missing_api_key_count: int = Field(
        0,
        description="Plan rows blocked until Subscriptions API keys are configured",
    )
    seed_validated_count: int = Field(
        0,
        description="Plan rows with smoke-validated positive or negative seed in registry",
    )
    pending_seed_count: int = Field(
        0,
        description="Runnable plan rows lacking validated seed (generic fallback input only)",
    )
    runnable_count: int = Field(
        0,
        description="Plan rows with input value and not blocked by missing API key",
    )


class TestsModuleSummary(BaseModel):
    module_id: str
    name: str
    summary: str
    consumption_group: str
    access_tier: str
    fixture_category: str = Field(
        "positive",
        description="Module-level fixture: positive expects output; negative expects clean_miss",
    )
    subscription_tier: str = Field(
        "none",
        description="none | free_auth | paid_auth — subscription/auth classification",
    )
    requires_api_key: bool = Field(
        False,
        description="True when module needs an API key or token to run",
    )
    has_api_key: bool = Field(
        True,
        description="True when runtime module opts include configured credentials",
    )
    test_count: int
    route_count: int = Field(
        0,
        description="Full route matrix size (consumed × produced)",
    )
    tests_run: int = Field(
        0,
        description="Module tests with a non-not-started state in TypeDB (when connected)",
    )
    routes_tested: int = Field(
        0,
        description="Deprecated alias of tests_run",
    )


class ModuleTestItem(BaseModel):
    test_id: str
    consumed_nugget_id: str
    input_value: Optional[str] = Field(
        None,
        description="Scan target sent as consumed nugget_data (exploratory test input)",
    )
    test_state: str = "not-started"
    fixture_kind: str = Field(
        "positive",
        description="positive: expect produced objects; negative: expect FINISHED with zero output",
    )
    seed_validated: bool = Field(
        False,
        description="True when registry has smoke-validated positive or negative fixture",
    )
    expected_absent_types: List[str] = Field(
        default_factory=list,
        description="For negative fixtures: types that must not appear in scan_results_by_type",
    )


class RouteCatalogItem(BaseModel):
    route_name: str
    consumed_nugget_id: str
    produced_nugget_id: str
    route_state: str = "not-started"
    sample_target: Optional[str] = Field(
        None,
        description="Pilot test value for consumed nugget (Stage 4c; full corpus in 4b)",
    )


class TestsNuggetSamplesResponse(BaseModel):
    samples: Dict[str, str] = Field(
        default_factory=dict,
        description="nugget_id → valid SpiderFeet scan target string",
    )


class TestsModuleDetail(BaseModel):
    module_id: str
    name: str
    summary: str
    consumption_group: str
    access_tier: str
    route_seed_nugget: Optional[str] = None
    test_count: int
    route_count: int = Field(
        0,
        description="Full route matrix size (consumed × produced)",
    )
    tests: List[ModuleTestItem]


class TestsPlanItem(BaseModel):
    """One runnable catalog test for batch execution (pre-expanded queue row)."""

    test_id: str
    module_id: str
    consumed_nugget_id: str
    input_value: Optional[str] = Field(
        None,
        description="Scan target for scan_ui consumed.nugget_data",
    )
    subscription_tier: str = Field(
        "none",
        description="none | free_auth | paid_auth",
    )
    requires_api_key: bool = Field(
        False,
        description="True when module metadata indicates auth/API key requirement",
    )
    has_api_key: bool = Field(
        True,
        description="True when runtime module opts include a configured API key/token",
    )
    skip_reason: Optional[str] = Field(
        None,
        description="Why this test should be skipped in Run All (e.g. missing-api-key)",
    )
    fixture_kind: str = Field(
        "positive",
        description="positive: expect produced objects; negative: expect FINISHED with zero output",
    )
    seed_validated: bool = Field(
        False,
        description="True when registry has smoke-validated positive or negative fixture",
    )
    expected_absent_types: List[str] = Field(
        default_factory=list,
        description="For negative fixtures: types that must not appear in scan_results_by_type",
    )


class TestsPlanResponse(BaseModel):
    items: List[TestsPlanItem] = Field(default_factory=list)
    module_count: int = 0
    test_count: int = 0


class SecretOptMasked(BaseModel):
    name: str
    masked_value: Optional[str] = Field(
        None,
        description="Masked secret (never full value on GET)",
    )
    configured: bool = Field(
        False,
        description="True when a non-empty value is stored",
    )


class SubscriptionModuleSummary(BaseModel):
    module_id: str
    name: str
    subscription_tier: str
    requires_api_key: bool
    has_api_key: bool
    fixture_category: str = Field(
        "positive",
        description="Module-level fixture: positive expects output; negative expects clean_miss",
    )
    signup_url: Optional[str] = Field(
        None,
        description="Primary signup or API key registration URL from catalogue",
    )
    signup_bucket: Optional[str] = Field(
        None,
        description="self-serve | review | manual | paid-risk",
    )
    signup_note: Optional[str] = Field(
        None,
        description="Heuristic guidance for operator signup (confirm free tier on site)",
    )
    secret_opts: List[SecretOptMasked] = Field(default_factory=list)
    provider_kind: str = Field(
        "spiderfeet",
        description="spiderfeet | cli_only | shared",
    )
    service_labels: List[str] = Field(
        default_factory=list,
        description="Human-readable consumer labels (SpiderFeet module, CLI apps)",
    )
    cli_apps: List[str] = Field(
        default_factory=list,
        description="Registered CLI applications that consume this credential",
    )
    group: str = Field(
        "spiderfeet",
        description="Accordion grouping: spiderfeet | cli | shared",
    )


class SubscriptionModuleDetail(BaseModel):
    module_id: str
    name: str
    summary: str
    access_tier: str
    subscription_tier: str
    requires_api_key: bool
    has_api_key: bool
    website: Optional[str] = None
    signup_url: Optional[str] = None
    signup_bucket: Optional[str] = None
    signup_note: Optional[str] = None
    api_key_instructions: List[str] = Field(default_factory=list)
    consumed_nuggets: List[str] = Field(default_factory=list)
    produced_nuggets: List[str] = Field(default_factory=list)
    secret_opts: List[SecretOptMasked] = Field(default_factory=list)
    provider_kind: str = Field("spiderfeet", description="spiderfeet | cli_only | shared")
    service_labels: List[str] = Field(default_factory=list)
    cli_apps: List[str] = Field(default_factory=list)
    group: str = Field("spiderfeet", description="spiderfeet | cli | shared")


class SubscriptionModuleUpdate(BaseModel):
    secrets: Dict[str, Optional[str]] = Field(
        ...,
        description="Secret opt name → value; empty string or null clears the stored secret",
    )
