"""Semantic identity keys for SPEC-020 context merges.

Normalization is deterministic. These functions do not decide whether two
records merge and do not mutate graphs. Same-address evidence is workflow
scoped and is not itself an endpoint identity key.
"""

from __future__ import annotations

import ipaddress
import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

IdentityStrategy = Literal[
    "global",
    "parent_scoped",
    "observation",
    "evidence_resolved",
]
DecisionAction = Literal["match", "distinct", "hold", "infer"]

GLOBAL_NUGGET_IDS = frozenset(
    {
        "IPV4_ADDRESS",
        "IPV6_ADDRESS",
        "MAC_ADDRESS",
        "DOMAIN_NAME",
        "COMPANY",
    }
)
PARENT_SCOPED_NUGGET_IDS = frozenset(
    {
        "NETWORKS",
        "APPLICATIONS",
        "ENVIRONMENT",
        "VULNERABILITIES",
        "TRANSPORT",
        "PORT",
        "SERVICE",
    }
)
OBSERVATION_NUGGET_IDS = frozenset(
    {
        "SCAN_RECORD",
        "HOST_STATUS",
        "HOST_STATUS_REASON",
        "SERVICE_VERSION",
        "PORT_STATE",
    }
)
EVIDENCE_RESOLVED_NUGGET_IDS = frozenset({"SYSTEM", "HOST", "DEVICE", "CDN"})

RELATION_ALIASES = {
    "contains": "contains",
    "contains-this": "contains",
    "contains_this": "contains",
    "had": "had",
    "had-this": "had",
    "has_this": "had",
    "has-this": "had",
    "listens-to": "listens-to",
    "listens_to": "listens-to",
    "listens_to_this": "listens-to",
    "listens-to-this": "listens-to",
}

_WHITESPACE = re.compile(r"\s+")
_MAC_SEPARATORS = re.compile(r"[:.\-]")


@dataclass(frozen=True)
class SemanticRecord:
    """One source occurrence interpreted under a semantic identity strategy."""

    strategy: IdentityStrategy
    nugget_id: str
    identity_key: str
    normalized_value: str
    source_occurrence_id: str
    nugget_instance_id: str | None = None
    parent_key: str | None = None
    workflow_execution_id: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class MergeEvent:
    """Normalized pair presented to a later policy stage."""

    left: SemanticRecord
    right: SemanticRecord
    workflow_execution_id: str
    rule_release_id: str | None = None


@dataclass(frozen=True)
class IdentityDecision:
    """Schema for a policy result. This module does not choose the action."""

    action: DecisionAction
    reason: str
    identity_key: str | None = None
    hold_code: str | None = None


def normalize_company_alias(value: str) -> str:
    """Normalize an alias for comparison without making it a company identity key."""
    return normalize_company_name(value)


class IdentityInputError(ValueError):
    """Raised when a value cannot be normalized for its declared nugget type."""


def normalize_ipv4(value: str) -> str:
    try:
        parsed = ipaddress.IPv4Address(value.strip())
    except ipaddress.AddressValueError as exc:
        raise IdentityInputError(f"invalid IPv4 address: {value!r}") from exc
    return str(parsed)


def normalize_ipv6(value: str) -> str:
    text = value.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    try:
        parsed = ipaddress.IPv6Address(text)
    except ipaddress.AddressValueError as exc:
        raise IdentityInputError(f"invalid IPv6 address: {value!r}") from exc
    return parsed.compressed.lower()


def normalize_mac(value: str) -> str:
    compact = _MAC_SEPARATORS.sub("", value.strip().lower())
    if len(compact) != 12 or any(char not in "0123456789abcdef" for char in compact):
        raise IdentityInputError(f"invalid MAC address: {value!r}")
    return ":".join(compact[index : index + 2] for index in range(0, 12, 2))


def normalize_fqdn(value: str) -> str:
    text = value.strip().rstrip(".").lower()
    if not text or any(char.isspace() for char in text):
        raise IdentityInputError(f"invalid domain name: {value!r}")
    labels = text.split(".")
    encoded = ".".join(label.encode("idna").decode("ascii") for label in labels)
    return encoded.lower()


def normalize_company_name(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    text = _WHITESPACE.sub(" ", text).strip()
    if not text:
        raise IdentityInputError("company name is empty")
    return text


def normalize_relation(value: str) -> str:
    key = value.strip().lower().replace(" ", "")
    try:
        return RELATION_ALIASES[key]
    except KeyError as exc:
        raise IdentityInputError(f"unsupported relation: {value!r}") from exc


def normalize_source(value: str) -> str:
    text = value.strip().lower()
    if not text:
        raise IdentityInputError("source identifier is empty")
    return text


def source_occurrence_id(subgraph_id: str, node_id: str) -> str:
    """Identify one emitted node without reusing its typed nugget instance ID."""
    if not subgraph_id.strip() or not node_id.strip():
        raise IdentityInputError("source occurrence requires subgraph and node IDs")
    return f"occ|{subgraph_id.strip()}|{node_id.strip()}"


def port_identity_key(host_key: str, transport: str, port: int | str) -> str:
    host = host_key.strip()
    protocol = transport.strip().lower()
    try:
        number = int(port)
    except (TypeError, ValueError) as exc:
        raise IdentityInputError(f"invalid port: {port!r}") from exc
    if not host or protocol not in {"tcp", "udp", "sctp"} or not 0 <= number <= 65535:
        raise IdentityInputError("port identity requires host, transport, and valid port")
    return f"port|{host}|{protocol}|{number}"


def literal_record(
    value: str,
    *,
    source_occurrence_id: str,
    nugget_instance_id: str | None = None,
) -> SemanticRecord:
    """Interpret a bare observed literal without inventing a system."""
    text = value.strip()
    try:
        normalized = normalize_ipv4(text)
        nugget_id = "IPV4_ADDRESS"
    except IdentityInputError:
        try:
            normalized = normalize_ipv6(text)
            nugget_id = "IPV6_ADDRESS"
        except IdentityInputError:
            normalized = normalize_fqdn(text)
            nugget_id = "DOMAIN_NAME"
    return SemanticRecord(
        strategy="global",
        nugget_id=nugget_id,
        identity_key=f"{nugget_id}|{normalized}",
        normalized_value=normalized,
        source_occurrence_id=source_occurrence_id,
        nugget_instance_id=nugget_instance_id,
    )


def semantic_record(
    *,
    nugget_id: str,
    nugget_data: str = "",
    source_occurrence_id: str,
    nugget_instance_id: str | None = None,
    parent_key: str | None = None,
    transport: str | None = None,
    workflow_execution_id: str | None = None,
    same_system_group_id: str | None = None,
    evidence: tuple[str, ...] = (),
) -> SemanticRecord:
    """Build the semantic identity for one source occurrence."""
    kind = nugget_id.strip().upper()
    if kind in GLOBAL_NUGGET_IDS:
        normalized = _normalize_global(kind, nugget_data)
        return SemanticRecord(
            "global",
            kind,
            f"{kind}|{normalized}",
            normalized,
            source_occurrence_id,
            nugget_instance_id,
            evidence=evidence,
        )
    if kind in PARENT_SCOPED_NUGGET_IDS:
        if not parent_key:
            raise IdentityInputError(f"{kind} requires a parent identity key")
        normalized = _normalize_parent_value(kind, nugget_data, transport)
        key = (
            port_identity_key(parent_key, transport or "", normalized)
            if kind == "PORT"
            else f"{kind}|{parent_key}|{normalized}"
        )
        return SemanticRecord(
            "parent_scoped",
            kind,
            key,
            normalized,
            source_occurrence_id,
            nugget_instance_id,
            parent_key,
            evidence=evidence,
        )
    if kind in OBSERVATION_NUGGET_IDS:
        normalized = _WHITESPACE.sub(" ", nugget_data.strip())
        return SemanticRecord(
            "observation",
            kind,
            f"observation|{source_occurrence_id}",
            normalized,
            source_occurrence_id,
            nugget_instance_id,
            workflow_execution_id=workflow_execution_id,
            evidence=evidence,
        )
    if kind in EVIDENCE_RESOLVED_NUGGET_IDS:
        if not workflow_execution_id:
            raise IdentityInputError(f"{kind} requires a workflow execution boundary")
        group = (same_system_group_id or "").strip()
        key = (
            f"endpoint|{workflow_execution_id}|group|{group}"
            if group
            else f"endpoint|{workflow_execution_id}|occurrence|{source_occurrence_id}"
        )
        return SemanticRecord(
            "evidence_resolved",
            kind,
            key,
            nugget_data.strip(),
            source_occurrence_id,
            nugget_instance_id,
            workflow_execution_id=workflow_execution_id,
            evidence=evidence,
        )
    raise IdentityInputError(f"no identity strategy for nugget type: {nugget_id!r}")


def _normalize_global(nugget_id: str, value: str) -> str:
    if nugget_id == "IPV4_ADDRESS":
        return normalize_ipv4(value)
    if nugget_id == "IPV6_ADDRESS":
        return normalize_ipv6(value)
    if nugget_id == "MAC_ADDRESS":
        return normalize_mac(value)
    if nugget_id == "DOMAIN_NAME":
        return normalize_fqdn(value)
    return normalize_company_name(value)


def _normalize_parent_value(nugget_id: str, value: str, transport: str | None) -> str:
    if nugget_id in {"NETWORKS", "APPLICATIONS", "ENVIRONMENT", "VULNERABILITIES"}:
        return nugget_id
    if nugget_id == "TRANSPORT":
        protocol = (value or transport or "").strip().lower()
        if protocol not in {"tcp", "udp", "sctp"}:
            raise IdentityInputError(f"invalid transport: {value!r}")
        return protocol
    if nugget_id == "PORT":
        return str(int(value))
    normalized = _WHITESPACE.sub(" ", value.strip().casefold())
    if not normalized:
        raise IdentityInputError("service identity requires a service name")
    return normalized
