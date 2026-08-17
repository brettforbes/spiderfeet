"""08-cited graph hooks for Pius structured-native adapter."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from adapters.pius.classify import EntityClassification, classify_record, is_domain_shape, normalize_value
from core.graph_builder import GraphBuilder, nugget_node
from core.pius_lists import load_pius_lists

WILDCARD_BASE_RE = re.compile(
    r"wildcard detected base=(?P<domain>\S+)\s+ips_count=(?P<count>\d+)",
    re.IGNORECASE,
)
WILDCARD_FILTER_RE = re.compile(
    r"wildcard detected, filtering subdomains parent=(?P<domain>\S+)",
    re.IGNORECASE,
)


def _add_descriptor(
    builder: GraphBuilder,
    parent_id: str,
    nugget_id: str,
    value: Any,
    *,
    description: str | None = None,
) -> None:
    if value is None or value == "":
        return
    node = builder.add_node(
        nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR", description=description)
    )
    builder.add_edge(parent_id, node["id"], "had")


class _PiusContext:
    """Per-scan graph accumulator for 08 R3–R11."""

    def __init__(self, builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
        self.builder = builder
        self.scan_id = scan_id
        self.doc = doc
        self.lists = load_pius_lists()
        self.org = str(doc.get("org") or doc.get("target") or "").strip()
        self._entity_nodes: dict[tuple[str, str], dict[str, Any]] = {}
        self._category_nodes: dict[str, dict[str, Any]] = {}
        self._wikidata_index: dict[str, list[dict[str, Any]]] = {}
        self.company_id: str | None = None

    def entity_node(self, nugget_id: str, value: str) -> dict[str, Any]:
        key = (nugget_id, value)
        existing = self._entity_nodes.get(key)
        if existing is not None:
            return existing
        node = self.builder.add_node(nugget_node(nugget_id, value))
        self._entity_nodes[key] = node
        return node

    def ensure_company(self) -> dict[str, Any] | None:
        """SPEC-019 COMPANY head with had COMPANY_NAME (bounded wrap)."""
        if not self.org:
            return None
        apex = str(self.doc.get("target") or "").strip().lower().rstrip(".")
        if not apex:
            return None
        company_data = f"company:{apex}"
        if self.company_id is not None:
            return self._entity_nodes[("COMPANY", company_data)]
        from core.topology import add_company_domain_tree

        tree = add_company_domain_tree(
            self.builder,
            self.scan_id,
            apex,
            company_name=self.org,
        )
        company = tree["company"]
        self._entity_nodes[("COMPANY", company_data)] = company
        self.company_id = company["id"]
        return company

    def category_node(self, nugget_id: str) -> dict[str, Any]:
        cached = self._category_nodes.get(nugget_id)
        if cached is not None:
            return cached
        company = self.ensure_company()
        node = self.builder.add_node(nugget_node(nugget_id, nugget_id, nugget_type="CATEGORY"))
        self._category_nodes[nugget_id] = node
        if company is not None:
            self.builder.add_edge(company["id"], node["id"], "contains")
        return node

    def link_under_category(self, category_id: str, entity: dict[str, Any]) -> None:
        category = self.category_node(category_id)
        self.builder.add_edge(category["id"], entity["id"], "contains")

    def index_wikidata(self, entity: dict[str, Any], wikidata_id: str) -> None:
        if not wikidata_id:
            return
        self._wikidata_index.setdefault(wikidata_id, []).append(entity)

    def org_for_record(self, record: dict[str, Any]) -> str | None:
        data = record.get("Data") or {}
        if isinstance(data, dict):
            org = data.get("org")
            if org:
                return str(org).strip()
        return self.org or None


def _attach_source_descriptors(
    ctx: _PiusContext,
    entity_id: str,
    record: dict[str, Any],
    classification: EntityClassification,
) -> None:
    """08 R6/R7 — source-specific descriptor attachment."""
    data = record.get("Data") or {}
    if not isinstance(data, dict):
        data = {}
    source = str(record.get("Source", "")).lower()

    if classification.raw_value != classification.candidate_value:
        _add_descriptor(ctx.builder, entity_id, "RAW_VALUE", classification.raw_value)

    if source == "wikidata":
        _add_descriptor(ctx.builder, entity_id, "WIKIDATA_ID", data.get("wikidata_id"))
        confidence = data.get("confidence")
        if confidence is not None:
            _add_descriptor(ctx.builder, entity_id, "CONFIDENCE_SCORE", confidence)
        _add_descriptor(ctx.builder, entity_id, "DISCOVERY_METHOD", data.get("method") or "wikidata")
        _add_descriptor(ctx.builder, entity_id, "NEEDS_REVIEW", data.get("needs_review"))
    elif source == "gleif":
        _add_descriptor(ctx.builder, entity_id, "LEI", data.get("lei"))
        _add_descriptor(ctx.builder, entity_id, "JURISDICTION", data.get("jurisdiction"))
        confidence = data.get("confidence")
        if confidence is not None:
            _add_descriptor(ctx.builder, entity_id, "CONFIDENCE_SCORE", confidence)
        _add_descriptor(ctx.builder, entity_id, "NEEDS_REVIEW", data.get("needs_review"))
    elif source == "crt-sh":
        _add_descriptor(ctx.builder, entity_id, "DISCOVERY_METHOD", "certificate-transparency")

    if classification.nugget_id == "CANDIDATE_ENTITY":
        _add_descriptor(ctx.builder, entity_id, "PRESEED_TYPE", data.get("preseed_type"))
        if classification.is_placeholder:
            _add_descriptor(ctx.builder, entity_id, "IS_PLACEHOLDER", "true")
            _add_descriptor(ctx.builder, entity_id, "NEEDS_REVIEW", "true")
        elif data.get("needs_review") is not None:
            _add_descriptor(ctx.builder, entity_id, "NEEDS_REVIEW", data.get("needs_review"))

    if classification.nugget_id == "DOMAIN_NAME" and classification.candidate_value.endswith(".onion"):
        _add_descriptor(ctx.builder, entity_id, "NETWORK_TYPE", "tor")


def _apply_domain_parent(ctx: _PiusContext, domain: dict[str, Any], domain_value: str) -> None:
    """08 R3 — parent domain via leftmost-label strip."""
    labels = domain_value.split(".")
    if len(labels) <= 2:
        return
    parent_value = ".".join(labels[1:])
    if not is_domain_shape(parent_value, ctx.lists):
        return
    parent_link = ctx.builder.add_node(
        nugget_node("DOMAIN_NAME_PARENT", parent_value.lower(), nugget_type="DESCRIPTOR")
    )
    ctx.builder.add_edge(domain["id"], parent_link["id"], "had")


def _apply_r4_containment(
    ctx: _PiusContext,
    record: dict[str, Any],
    classification: EntityClassification,
    entity: dict[str, Any],
) -> None:
    """08 R4a/R4b/R4c — company hierarchy."""
    company = ctx.ensure_company()
    if company is None:
        return
    data = record.get("Data") or {}
    if not isinstance(data, dict):
        data = {}
    source = str(record.get("Source", "")).lower()
    record_type = str(record.get("Type", "")).lower()
    needs_review = data.get("needs_review") is True

    if source == "wikidata" and record_type == "domain" and data.get("subsidiary"):
        affiliate = ctx.entity_node("AFFILIATE_COMPANY_NAME", str(data["subsidiary"]))
        ctx.link_under_category("AFFILIATES", affiliate)
        ctx.builder.add_edge(company["id"], affiliate["id"], "contains")
        relationship = data.get("relationship") or "affiliated"
        _add_descriptor(ctx.builder, affiliate["id"], "RELATIONSHIP_TYPE", relationship)
        ctx.index_wikidata(affiliate, str(data.get("wikidata_id") or ""))
        if classification.nugget_id == "DOMAIN_NAME":
            ctx.link_under_category("DOMAINS", entity)
            ctx.builder.add_edge(affiliate["id"], entity["id"], "contains")
        if needs_review:
            _add_descriptor(ctx.builder, entity["id"], "REVIEW_STATUS", "unconfirmed")
        else:
            _add_descriptor(ctx.builder, entity["id"], "REVIEW_STATUS", "confirmed")
        return

    if source == "gleif":
        if classification.nugget_id == "AFFILIATE_COMPANY_NAME":
            ctx.link_under_category("AFFILIATES", entity)
            ctx.builder.add_edge(company["id"], entity["id"], "contains")
            relationship = data.get("relationshipType") or "affiliated"
            _add_descriptor(ctx.builder, entity["id"], "RELATIONSHIP_TYPE", relationship)
        return

    if classification.nugget_id == "DOMAIN_NAME":
        ctx.link_under_category("DOMAINS", entity)
        ctx.builder.add_edge(company["id"], entity["id"], "contains")
    elif classification.nugget_id == "AFFILIATE_COMPANY_NAME":
        ctx.link_under_category("AFFILIATES", entity)
        ctx.builder.add_edge(company["id"], entity["id"], "contains")
    elif classification.nugget_id == "CANDIDATE_ENTITY":
        ctx.link_under_category("LEADS", entity)
        ctx.builder.add_edge(company["id"], entity["id"], "contains")
    elif classification.nugget_id == "NETBLOCK_OWNER":
        ctx.builder.add_edge(company["id"], entity["id"], "contains")

    review = "unconfirmed" if needs_review else "confirmed"
    _add_descriptor(ctx.builder, entity["id"], "REVIEW_STATUS", review)


def _apply_page_extraction(ctx: _PiusContext, record: dict[str, Any]) -> None:
    """08 R11 — PAGE entity from website URL."""
    data = record.get("Data") or {}
    if not isinstance(data, dict):
        return
    website = data.get("website")
    if not website:
        return
    parsed = urlparse(str(website))
    page_host = (parsed.hostname or "").lower()
    if not page_host:
        return
    page_path = parsed.path or "/"
    host_domain = ctx.entity_node("DOMAIN_NAME", page_host)
    ctx.link_under_category("DOMAINS", host_domain)
    _apply_domain_parent(ctx, host_domain, page_host)
    page = ctx.entity_node("PAGE", str(website))
    pages_category = ctx.category_node("PAGES")
    ctx.builder.add_edge(host_domain["id"], pages_category["id"], "contains")
    ctx.builder.add_edge(pages_category["id"], page["id"], "contains")
    _add_descriptor(ctx.builder, page["id"], "PAGE_URL", str(website))
    _add_descriptor(ctx.builder, page["id"], "PAGE_PATH", page_path)
    if data.get("subsidiary"):
        _add_descriptor(ctx.builder, page["id"], "BRAND_NAME", data.get("subsidiary"))


def _apply_stderr_wildcards(ctx: _PiusContext) -> None:
    """08 R10 — wildcard DNS flags from document stderr_banner."""
    banner = str(ctx.doc.get("stderr_banner") or "")
    if not banner.strip():
        return
    for line in banner.splitlines():
        match = WILDCARD_BASE_RE.search(line)
        if match:
            domain = match.group("domain").lower()
            count = match.group("count")
            target = ctx._entity_nodes.get(("DOMAIN_NAME", domain))
            if target is None:
                target = ctx.entity_node("DOMAIN_NAME", domain)
                ctx.link_under_category("DOMAINS", target)
            _add_descriptor(ctx.builder, target["id"], "IS_WILDCARD_DNS", "true")
            _add_descriptor(ctx.builder, target["id"], "WILDCARD_IP_COUNT", count)
        filter_match = WILDCARD_FILTER_RE.search(line)
        if filter_match:
            domain = filter_match.group("domain").lower()
            target = ctx._entity_nodes.get(("DOMAIN_NAME", domain))
            if target is None:
                target = ctx.entity_node("DOMAIN_NAME", domain)
                ctx.link_under_category("DOMAINS", target)
            _add_descriptor(ctx.builder, target["id"], "SUBDOMAIN_ENUMERATION_SUPPRESSED", "true")


def apply_pius_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply 08 R0–R11 (R8 resolves-to deferred until SPEC relation update)."""
    ctx = _PiusContext(builder, scan_id, doc)
    ctx.ensure_company()

    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        classification = classify_record(record)
        if classification is None:
            continue

        if classification.is_registrar:
            registrar = ctx.entity_node("DOMAIN_REGISTRAR", classification.candidate_value)
            _attach_source_descriptors(ctx, registrar["id"], record, classification)
            company = ctx.ensure_company()
            if company is not None:
                ctx.builder.add_edge(company["id"], registrar["id"], "contains")
            continue

        entity = ctx.entity_node(classification.nugget_id, classification.candidate_value)
        _attach_source_descriptors(ctx, entity["id"], record, classification)

        data = record.get("Data") or {}
        if isinstance(data, dict) and data.get("wikidata_id"):
            ctx.index_wikidata(entity, str(data["wikidata_id"]))

        if classification.nugget_id == "DOMAIN_NAME":
            _apply_domain_parent(ctx, entity, classification.candidate_value)

        _apply_r4_containment(ctx, record, classification, entity)
        _apply_page_extraction(ctx, record)

    _apply_stderr_wildcards(ctx)
