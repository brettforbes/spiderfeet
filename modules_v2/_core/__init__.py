"""Core helpers for SPEC-004 CLI graph conversion."""

from .graph_builder import (
    DEFAULT_TYPE_COLOURS,
    ONTOLOGY_NAMESPACE,
    GraphBuilder,
    load_nugget_templates,
    nugget_instance_id,
    nugget_node,
    validate_graph,
    validate_graph_connectivity,
)
from .rule_engine import RuleEngine, RulePackError, load_rule_pack, load_shared_rules, resolve_path
from .correlation_engine import (
    CorrelationRecord,
    RecordCorrelationResult,
    correlate_nerva_records,
    correlate_records,
    normalize_nerva_record,
)
from .correlation_lists import (
    CDN_SIGNATURES_PATH,
    EDGE_ASNS_PATH,
    cdn_provider_signatures,
    edge_asn_entries,
    load_cdn_signatures,
    load_edge_asns,
    match_edge_asn,
    match_server_header,
)
from .topology import (
    add_host_networks_port_service,
    add_scan_head,
    add_system_l2,
    add_trace_hop_chain,
)
from .types import CaptureFamily, RulePack

__all__ = [
    "DEFAULT_TYPE_COLOURS",
    "ONTOLOGY_NAMESPACE",
    "correlate_nerva_records",
    "correlate_records",
    "CorrelationRecord",
    "RecordCorrelationResult",
    "normalize_nerva_record",
    "GraphBuilder",
    "RulePack",
    "RuleEngine",
    "RulePackError",
    "add_host_networks_port_service",
    "add_scan_head",
    "add_system_l2",
    "add_trace_hop_chain",
    "cdn_provider_signatures",
    "CDN_SIGNATURES_PATH",
    "EDGE_ASNS_PATH",
    "edge_asn_entries",
    "load_cdn_signatures",
    "load_edge_asns",
    "load_nugget_templates",
    "load_rule_pack",
    "load_shared_rules",
    "match_edge_asn",
    "match_server_header",
    "nugget_instance_id",
    "nugget_node",
    "resolve_path",
    "validate_graph",
    "validate_graph_connectivity",
]
