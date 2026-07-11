"""11B-cited graph hooks for Nuclei structured-native adapter (SPEC-004 D5)."""

from __future__ import annotations

import json
from typing import Any

from core.graph_builder import GraphBuilder, nugget_node
from nuclei_structured import CVE_RE

SEVERITY_CATEGORY: dict[str, str] = {
    "info": "NUCLEI_SEVERITY_INFO",
    "low": "NUCLEI_SEVERITY_LOW",
    "medium": "NUCLEI_SEVERITY_MEDIUM",
    "high": "NUCLEI_SEVERITY_HIGH",
    "critical": "NUCLEI_SEVERITY_CRITICAL",
}

CVE_TIER: dict[str, str] = {
    "critical": "VULNERABILITY_CVE_CRITICAL",
    "high": "VULNERABILITY_CVE_HIGH",
    "medium": "VULNERABILITY_CVE_MEDIUM",
    "low": "VULNERABILITY_CVE_LOW",
    "info": "VULNERABILITY_CVE_LOW",
}


def _add_descriptor(builder: GraphBuilder, parent_id: str, nugget_id: str, value: Any) -> None:
    if value is None or value == "":
        return
    if isinstance(value, list):
        if not value:
            return
        value = ", ".join(str(item) for item in value)
    node = builder.add_node(nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR"))
    builder.add_edge(parent_id, node["id"], "had")


def _host_identity(record: dict[str, Any]) -> str:
    """11B H1/H2 — resolve host from hostname with ip fallback."""
    host = str(record.get("host") or "").strip()
    if host:
        return host
    ip = str(record.get("ip") or "").strip()
    return ip or "unknown"


def _finding_identity(record: dict[str, Any]) -> str:
    """11B F2 — unique finding identity per record."""
    template_id = str(record.get("template-id") or "unknown")
    matched = str(record.get("matched-at") or "")
    timestamp = str(record.get("timestamp") or "")
    return f"{template_id}:{matched}:{timestamp}"


def _extract_cves(record: dict[str, Any]) -> list[str]:
    info = record.get("info") or {}
    classification = info.get("classification") or {}
    cves: set[str] = set()
    cve_id = classification.get("cve-id")
    if cve_id:
        cves.add(str(cve_id))
    cves.update(CVE_RE.findall(json.dumps(record)))
    return sorted(cves)


def _severity_key(record: dict[str, Any]) -> str:
    """11B SEV1/SEV2/SEV3 — normalize severity bucket."""
    info = record.get("info") or {}
    severity = str(info.get("severity") or "info").strip().lower()
    return severity if severity in SEVERITY_CATEGORY else "info"


def _ensure_host_security(builder: GraphBuilder, host_id: str, host_key: str) -> dict[str, Any]:
    """11B SEC1/SEC2 — reuse or create SECURITY beneath HOST."""
    security = builder.add_node(nugget_node("SECURITY", f"{host_key}::SECURITY", nugget_type="CATEGORY"))
    builder.add_edge(host_id, security["id"], "contains")
    return security


def _ensure_templates_used(builder: GraphBuilder, security_id: str, host_key: str) -> dict[str, Any]:
    """11B TMP1/TMP2 — reuse or create TEMPLATES_USED beneath SECURITY."""
    templates_used = builder.add_node(
        nugget_node("TEMPLATES_USED", f"{host_key}::TEMPLATES_USED", nugget_type="CATEGORY")
    )
    builder.add_edge(security_id, templates_used["id"], "contains")
    return templates_used


def _ensure_findings(builder: GraphBuilder, security_id: str, host_key: str) -> dict[str, Any]:
    """11B FIND1/FIND2 — reuse or create FINDINGS beneath SECURITY."""
    findings = builder.add_node(nugget_node("FINDINGS", f"{host_key}::FINDINGS", nugget_type="CATEGORY"))
    builder.add_edge(security_id, findings["id"], "contains")
    return findings


def _ensure_severity_category(
    builder: GraphBuilder,
    findings_id: str,
    host_key: str,
    severity: str,
) -> dict[str, Any]:
    """11B SEV4/SEV5 — reuse or create severity category beneath FINDINGS."""
    category_id = SEVERITY_CATEGORY[severity]
    category = builder.add_node(
        nugget_node(category_id, f"{host_key}::{category_id}", nugget_type="CATEGORY")
    )
    builder.add_edge(findings_id, category["id"], "contains")
    return category


def _add_template(builder: GraphBuilder, templates_used_id: str, record: dict[str, Any]) -> dict[str, Any]:
    """11B T1-T5 — deduplicated template entity with descriptors."""
    template_id = str(record.get("template-id") or "unknown")
    template = builder.add_node(nugget_node("NUCLEI_TEMPLATE", template_id))
    builder.add_edge(templates_used_id, template["id"], "contains")

    info = record.get("info") or {}
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_ID", template_id)
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_NAME", info.get("name"))
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_PATH", record.get("template-path"))
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_AUTHOR", info.get("author"))
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_TAGS", info.get("tags"))
    _add_descriptor(builder, template["id"], "NUCLEI_TEMPLATE_PROTOCOL", record.get("type"))
    return template


def _add_vulnerability(builder: GraphBuilder, finding_id: str, record: dict[str, Any]) -> dict[str, Any]:
    """11B V1-V4 — per-record vulnerability observation beneath finding."""
    identity = _finding_identity(record)
    info = record.get("info") or {}
    vuln_name = str(info.get("name") or record.get("template-id") or identity)
    vulnerability = builder.add_node(nugget_node("NUCLEI_VULNERABILITY", identity))
    builder.add_edge(finding_id, vulnerability["id"], "contains")

    classification = info.get("classification") or {}
    metadata = info.get("metadata") or {}
    _add_descriptor(builder, vulnerability["id"], "VULNERABILITY_GENERAL", vuln_name)
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_DESCRIPTION", info.get("description"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_IMPACT", info.get("impact"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_REMEDIATION", info.get("remediation"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_SEVERITY", info.get("severity"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_VENDOR", metadata.get("vendor"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_PRODUCT", metadata.get("product"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_TAGS", info.get("tags"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_CWE", classification.get("cwe-id"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_CPE", classification.get("cpe"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_CVSS_METRICS", classification.get("cvss-metrics"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_CVSS_SCORE", classification.get("cvss-score"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_EPSS_SCORE", classification.get("epss-score"))
    _add_descriptor(builder, vulnerability["id"], "NUCLEI_VULN_EPSS_PERCENTILE", classification.get("epss-percentile"))

    severity = _severity_key(record)
    tier = CVE_TIER[severity]
    for cve in _extract_cves(record):
        _add_descriptor(builder, vulnerability["id"], tier, cve)
    return vulnerability


def _add_finding(
    builder: GraphBuilder,
    severity_category_id: str,
    template: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    """11B F1-F3/E5/E6 — create finding with observation descriptors."""
    finding = builder.add_node(nugget_node("NUCLEI_FINDING", _finding_identity(record)))
    builder.add_edge(severity_category_id, finding["id"], "contains")

    _add_descriptor(builder, finding["id"], "NUCLEI_TEMPLATE_ID", record.get("template-id"))
    _add_descriptor(builder, finding["id"], "NUCLEI_MATCHED_AT", record.get("matched-at"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_TIMESTAMP", record.get("timestamp"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_HOST", record.get("host"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_IP", record.get("ip"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_PORT", record.get("port"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_URL", record.get("url"))
    _add_descriptor(builder, finding["id"], "NUCLEI_FINDING_PROTOCOL", record.get("type"))
    _add_descriptor(builder, finding["id"], "NUCLEI_MATCHER_NAME", record.get("matcher-name"))
    _add_descriptor(builder, finding["id"], "NUCLEI_MATCHER_STATUS", record.get("matcher-status"))
    _add_descriptor(builder, finding["id"], "NUCLEI_EXTRACTED_RESULTS", record.get("extracted-results"))

    vulnerability = _add_vulnerability(builder, finding["id"], record)
    builder.add_edge(finding["id"], template["id"], "had")
    return vulnerability


def apply_nuclei_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply 11B host/security/finding hierarchy using approved SPEC-004 relations only."""
    target = str(doc.get("target") or "").strip()
    if target:
        target_host = builder.add_node(nugget_node("HOST", target))
        builder.add_edge(scan_id, target_host["id"], "contains")

    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        if not record.get("template-id") or not record.get("info") or not record.get("host"):
            continue

        host_key = _host_identity(record)
        host = builder.add_node(nugget_node("HOST", host_key))
        builder.add_edge(scan_id, host["id"], "contains")

        security = _ensure_host_security(builder, host["id"], host_key)
        templates_used = _ensure_templates_used(builder, security["id"], host_key)
        findings = _ensure_findings(builder, security["id"], host_key)

        severity = _severity_key(record)
        severity_category = _ensure_severity_category(builder, findings["id"], host_key, severity)

        template = _add_template(builder, templates_used["id"], record)
        vulnerability = _add_finding(builder, severity_category["id"], template, record)

        port = record.get("port")
        if port:
            service_key = f"{host_key}:{port}"
            service = builder.add_node(nugget_node("SERVICE", service_key))
            builder.add_edge(host["id"], service["id"], "contains")
            _add_descriptor(builder, service["id"], "NUCLEI_FINDING_PORT", port)
            builder.add_edge(service["id"], vulnerability["id"], "had")

        builder.add_edge(host["id"], vulnerability["id"], "had")
