"""Host-correlation engine for Nerva records (Rulesets A, C, B from seed 07)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .correlation_lists import (
    CdnProviderSignature,
    EdgeAsnEntry,
    cdn_provider_signatures,
    edge_asn_entries,
    match_edge_asn,
    match_server_header,
)

Confidence = str  # high | medium | low | inconclusive
HostClassification = str  # standard_host | origin_behind_proxy | fronted_unknown | unknown


@dataclass
class CorrelationRecord:
    record_id: str
    hostname: str
    ip_address: str
    port: int
    protocol: str
    ssh_host_key_fingerprint: str | None = None
    ssh_host_key_type: str | None = None
    tls_cert_serial: str | None = None
    service_banner: str | None = None
    response_headers: dict[str, list[str]] = field(default_factory=dict)
    technologies: list[str] = field(default_factory=list)
    asn: int | None = None
    version: str | None = None


@dataclass
class RecordCorrelationResult:
    record_id: str
    hostname: str
    ip_address: str
    same_system_group_id: str | None
    same_system_confidence: Confidence
    same_system_evidence: str
    host_classification: HostClassification
    classification_confidence: Confidence
    classification_rule_fired: str
    cdn_vendor: str | None = None
    origin_host_count: int | None = None


def normalize_nerva_record(record: dict[str, Any], index: int) -> CorrelationRecord:
    """Map one nerva_fingerprint_v1 record into correlation inputs."""
    metadata = record.get("metadata") or {}
    headers = metadata.get("response_headers") or {}
    normalized_headers: dict[str, list[str]] = {}
    for key, value in headers.items():
        if isinstance(value, list):
            normalized_headers[str(key)] = [str(item) for item in value]
        elif value is not None:
            normalized_headers[str(key)] = [str(value)]

    return CorrelationRecord(
        record_id=f"{record.get('host', 'unknown')}:{record.get('ip', '?')}:{record.get('port', 0)}:{index}",
        hostname=str(record.get("host") or "unknown"),
        ip_address=str(record.get("ip") or ""),
        port=int(record.get("port") or 0),
        protocol=str(record.get("protocol") or ""),
        ssh_host_key_fingerprint=metadata.get("host_key_fingerprint"),
        ssh_host_key_type=metadata.get("host_key_type"),
        tls_cert_serial=metadata.get("tls_cert_serial") or metadata.get("cert_serial"),
        service_banner=metadata.get("banner"),
        response_headers=normalized_headers,
        technologies=[str(item) for item in metadata.get("technologies") or []],
        asn=int(record["asn"]) if record.get("asn") is not None else None,
        version=record.get("version"),
    )


def _header_value(headers: dict[str, list[str]], name: str) -> str:
    for key, values in headers.items():
        if key.lower() == name.lower() and values:
            return values[0]
    return ""


def _header_items(headers: dict[str, list[str]]) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for key, values in headers.items():
        for value in values:
            items.append((key.lower(), value))
    return items


def _ruleset_a_pair(left: CorrelationRecord, right: CorrelationRecord) -> tuple[bool, Confidence, str]:
    """Ruleset A — compare two records for same-system evidence."""
    if left.ssh_host_key_fingerprint and right.ssh_host_key_fingerprint:
        if left.ssh_host_key_fingerprint != right.ssh_host_key_fingerprint:
            return False, "high", "A6: divergent SSH host key fingerprints"
        return True, "high", "A1: matching SSH host key fingerprint"

    if left.tls_cert_serial and right.tls_cert_serial:
        if left.tls_cert_serial != right.tls_cert_serial:
            return False, "high", "A6: divergent TLS certificate serial"
        return True, "high", "A2: matching TLS certificate serial"

    if left.service_banner and right.service_banner and left.service_banner == right.service_banner:
        return True, "medium", "A3: matching service banner"

    left_headers = _header_items(left.response_headers)
    right_headers = _header_items(right.response_headers)
    if left_headers and right_headers:
        shared = set(left_headers) & set(right_headers)
        if len(shared) >= 2:
            return True, "medium", "A4: matching response headers"

    return False, "inconclusive", ""


def _union_groups(records: list[CorrelationRecord]) -> list[list[CorrelationRecord]]:
    parent = list(range(len(records)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(a: int, b: int) -> None:
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[root_b] = root_a

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            same, _, _ = _ruleset_a_pair(records[i], records[j])
            if same:
                union(i, j)

    grouped: dict[int, list[CorrelationRecord]] = {}
    for index, record in enumerate(records):
        grouped.setdefault(find(index), []).append(record)
    return list(grouped.values())


def _match_c1(record: CorrelationRecord, signatures: list[CdnProviderSignature]) -> str | None:
    server = _header_value(record.response_headers, "Server") or (record.version or "")
    vendor = match_server_header(server, signatures)
    if vendor:
        return vendor

    for key, value in _header_items(record.response_headers):
        for signature in signatures:
            for prefix in signature.header_prefixes:
                if key.startswith(prefix.lower()):
                    return signature.vendor
            for header_name in signature.header_names:
                if key == header_name.lower():
                    return signature.vendor
            for pattern in signature.powered_by_patterns:
                if pattern.lower() in value.lower():
                    return signature.vendor

    for technology in record.technologies:
        for signature in signatures:
            for marker in signature.technology_markers:
                if marker.lower() == technology.lower():
                    return signature.vendor
    return None


def _pop_code_from_cf_ray(value: str) -> str | None:
    if "-" not in value:
        return None
    suffix = value.rsplit("-", 1)[-1].strip()
    return suffix or None


def _ruleset_c(
    records: Iterable[CorrelationRecord],
    *,
    signatures: list[CdnProviderSignature],
    edge_asns: list[EdgeAsnEntry],
) -> tuple[bool, Confidence, str, str | None]:
    """Ruleset C — fronting / edge detection (runs before Ruleset B)."""
    records = list(records)
    fired: list[str] = []
    vendor: str | None = None

    for record in records:
        c1_vendor = _match_c1(record, signatures)
        if c1_vendor:
            vendor = vendor or c1_vendor
            fired.append(f"C1: Server/header signature ({c1_vendor})")

        if record.asn is not None:
            c2_vendor = match_edge_asn(record.asn, edge_asns)
            if c2_vendor:
                vendor = vendor or c2_vendor
                fired.append(f"C2: ASN {record.asn} ({c2_vendor})")

    pop_codes = {
        pop
        for record in records
        for pop in [
            _pop_code_from_cf_ray(_header_value(record.response_headers, "Cf-Ray")),
        ]
        if pop
    }
    if len(records) >= 2 and pop_codes:
        fired.append("C3: edge PoP metadata across hostname records")
        if not vendor:
            vendor = _match_c1(records[0], signatures)

    web_only = all(record.port in {80, 443} for record in records)
    if web_only and len(records) >= 2:
        fired.append("C5: web-only port profile")

    if any(rule.startswith("C1:") or rule.startswith("C2:") for rule in fired):
        rule = fired[0]
        return True, "high", rule, vendor
    if any(rule.startswith("C3:") for rule in fired) and vendor:
        return True, "medium", "C3: edge PoP metadata", vendor
    if len([rule for rule in fired if rule.startswith("C5:")]) >= 1 and vendor:
        return True, "medium", "C5: web-only port profile with CDN signature", vendor
    return False, "low", "", None


def _has_durable_identity(record: CorrelationRecord) -> bool:
    return bool(record.ssh_host_key_fingerprint or record.tls_cert_serial or record.service_banner)


def _ruleset_b(records: Iterable[CorrelationRecord], fronted: bool) -> tuple[HostClassification, Confidence, str]:
    """Ruleset B — standard host classification when not fronted."""
    records = list(records)
    durable = [record for record in records if _has_durable_identity(record)]
    if not durable:
        return "unknown", "low", "B: no durable machine identifier"

    non_web = any(record.port not in {80, 443} for record in records)
    if fronted:
        return "origin_behind_proxy", "medium", "B1+C: durable identity behind fronted edge"

    if non_web:
        return "standard_host", "high", "B1+B2: durable identity with non-web port profile"
    return "standard_host", "high", "B1: durable machine identifier present"


def correlate_records(
    records: list[CorrelationRecord],
    *,
    signatures: list[CdnProviderSignature] | None = None,
    edge_asns: list[EdgeAsnEntry] | None = None,
) -> list[RecordCorrelationResult]:
    """Correlate one hostname's records using seed 07 A -> C -> B chaining."""
    signatures = signatures or cdn_provider_signatures()
    edge_asns = edge_asns or edge_asn_entries()
    if not records:
        return []

    groups = _union_groups(records)
    results: list[RecordCorrelationResult] = []

    for group_index, group in enumerate(groups, start=1):
        hostname = group[0].hostname
        group_id = f"{hostname}:group:{group_index}"

        pair_evidence = ""
        pair_confidence: Confidence = "inconclusive"
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    same, confidence, evidence = _ruleset_a_pair(group[i], group[j])
                    if same and evidence:
                        pair_evidence = evidence
                        pair_confidence = confidence
                        break
                if pair_evidence:
                    break

        fronted, c_confidence, c_rule, vendor = _ruleset_c(group, signatures=signatures, edge_asns=edge_asns)
        if fronted:
            host_class: HostClassification = "fronted_unknown"
            class_confidence = c_confidence
            class_rule = c_rule
            origin_host_count = None
            if vendor and any(record.ssh_host_key_fingerprint or record.tls_cert_serial for record in group):
                host_class, class_confidence, class_rule = _ruleset_b(group, fronted=True)
        else:
            host_class, class_confidence, class_rule = _ruleset_b(group, fronted=False)
            origin_host_count = 1 if host_class == "standard_host" else None

        for record in group:
            results.append(
                RecordCorrelationResult(
                    record_id=record.record_id,
                    hostname=record.hostname,
                    ip_address=record.ip_address,
                    same_system_group_id=group_id if len(group) > 1 or pair_evidence else None,
                    same_system_confidence=pair_confidence if pair_evidence else "inconclusive",
                    same_system_evidence=pair_evidence,
                    host_classification=host_class,
                    classification_confidence=class_confidence,
                    classification_rule_fired=class_rule,
                    cdn_vendor=vendor,
                    origin_host_count=origin_host_count,
                )
            )

    return results


def correlate_nerva_records(
    records: list[dict[str, Any]],
    *,
    signatures: list[CdnProviderSignature] | None = None,
    edge_asns: list[EdgeAsnEntry] | None = None,
) -> list[RecordCorrelationResult]:
    """Group nerva records by hostname and run Rulesets A -> C -> B."""
    normalized = [normalize_nerva_record(record, index) for index, record in enumerate(records)]
    by_hostname: dict[str, list[CorrelationRecord]] = {}
    for record in normalized:
        by_hostname.setdefault(record.hostname, []).append(record)

    results: list[RecordCorrelationResult] = []
    for hostname in sorted(by_hostname):
        results.extend(
            correlate_records(
                by_hostname[hostname],
                signatures=signatures,
                edge_asns=edge_asns,
            )
        )
    return results
