"""Load versioned shared correlation lists for Ruleset C (SPEC-004 C1)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SHARED_RULES_DIR = Path(__file__).resolve().parents[1] / "rules" / "_shared"
CDN_SIGNATURES_PATH = SHARED_RULES_DIR / "cdn_signatures.yaml"
EDGE_ASNS_PATH = SHARED_RULES_DIR / "edge_asns.yaml"


class CorrelationListError(ValueError):
    """Raised when a shared correlation list fails validation."""


@dataclass(frozen=True)
class CdnProviderSignature:
    vendor: str
    confidence: str
    server_header_values: tuple[str, ...]
    header_prefixes: tuple[str, ...]
    header_names: tuple[str, ...]
    technology_markers: tuple[str, ...]
    powered_by_patterns: tuple[str, ...]


@dataclass(frozen=True)
class EdgeAsnEntry:
    asn: int
    vendor: str
    org_names: tuple[str, ...]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CorrelationListError(f"{path} must contain a YAML mapping")
    return data


def load_cdn_signatures(path: Path | None = None) -> dict[str, Any]:
    """Load and validate `cdn_signatures.yaml`."""
    path = path or CDN_SIGNATURES_PATH
    data = _load_yaml(path)
    if data.get("schema") != "cdn_signatures_v1":
        raise CorrelationListError(f"{path} requires schema cdn_signatures_v1")
    providers = data.get("providers")
    if not isinstance(providers, list) or not providers:
        raise CorrelationListError(f"{path} requires a non-empty providers list")
    for provider in providers:
        if not isinstance(provider, dict) or not provider.get("vendor"):
            raise CorrelationListError(f"{path} provider entries require vendor")
    return data


def load_edge_asns(path: Path | None = None) -> dict[str, Any]:
    """Load and validate `edge_asns.yaml`."""
    path = path or EDGE_ASNS_PATH
    data = _load_yaml(path)
    if data.get("schema") != "edge_asns_v1":
        raise CorrelationListError(f"{path} requires schema edge_asns_v1")
    asns = data.get("asns")
    if not isinstance(asns, list) or not asns:
        raise CorrelationListError(f"{path} requires a non-empty asns list")
    for entry in asns:
        if not isinstance(entry, dict) or "asn" not in entry or not entry.get("vendor"):
            raise CorrelationListError(f"{path} asn entries require asn and vendor")
    return data


def cdn_provider_signatures(path: Path | None = None) -> list[CdnProviderSignature]:
    """Return normalized provider signature rows for correlation_engine (C2)."""
    data = load_cdn_signatures(path)
    rows: list[CdnProviderSignature] = []
    for provider in data["providers"]:
        rows.append(
            CdnProviderSignature(
                vendor=str(provider["vendor"]),
                confidence=str(provider.get("confidence") or "medium"),
                server_header_values=tuple(provider.get("server_header_values") or ()),
                header_prefixes=tuple(provider.get("header_prefixes") or ()),
                header_names=tuple(provider.get("header_names") or ()),
                technology_markers=tuple(provider.get("technology_markers") or ()),
                powered_by_patterns=tuple(provider.get("powered_by_patterns") or ()),
            )
        )
    return rows


def edge_asn_entries(path: Path | None = None) -> list[EdgeAsnEntry]:
    """Return normalized ASN rows for correlation_engine (C2)."""
    data = load_edge_asns(path)
    return [
        EdgeAsnEntry(
            asn=int(entry["asn"]),
            vendor=str(entry["vendor"]),
            org_names=tuple(entry.get("org_names") or ()),
        )
        for entry in data["asns"]
    ]


def match_server_header(server_value: str, signatures: list[CdnProviderSignature] | None = None) -> str | None:
    """Ruleset C1 helper: return vendor when Server header matches a signature."""
    signatures = signatures or cdn_provider_signatures()
    normalized = (server_value or "").strip().lower()
    if not normalized:
        return None
    for signature in signatures:
        for candidate in signature.server_header_values:
            if normalized == candidate.lower() or candidate.lower() in normalized:
                return signature.vendor
    return None


def match_edge_asn(asn: int, entries: list[EdgeAsnEntry] | None = None) -> str | None:
    """Ruleset C2 helper: return vendor when ASN is in the edge provider list."""
    entries = entries or edge_asn_entries()
    for entry in entries:
        if entry.asn == asn:
            return entry.vendor
    return None
