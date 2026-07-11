"""08 R0–R2 value normalization and entity classification for Pius records."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from core.pius_lists import is_known_registrar, is_placeholder_value, load_pius_lists

MARKDOWN_LINK_PATTERN = re.compile(
    r"^\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)$",
)
DOMAIN_LABEL_PATTERN = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NormalizedValue:
    """Result of 08 R0 normalization."""

    raw_value: str
    candidate_value: str
    label_mismatch: bool = False


@dataclass(frozen=True)
class EntityClassification:
    """Entity type chosen by 08 R1/R2."""

    nugget_id: str
    candidate_value: str
    raw_value: str
    is_placeholder: bool = False
    is_registrar: bool = False


def _legal_suffix_hit(value: str, denylist: list[str]) -> bool:
    upper = value.upper()
    tokens = re.split(r"[\s.,]+", upper)
    deny = {entry.upper() for entry in denylist}
    return any(token in deny for token in tokens)


def normalize_value(raw: str) -> NormalizedValue:
    """08 R0 — unwrap markdown links before shape classification."""
    raw = raw.strip()
    match = MARKDOWN_LINK_PATTERN.match(raw)
    if not match:
        return NormalizedValue(raw_value=raw, candidate_value=raw)
    label = match.group("label").strip()
    url = match.group("url").strip()
    parsed = urlparse(url if "://" in url else f"https://{url}")
    hostname = (parsed.hostname or label).strip().lower()
    label_host = label.lower().lstrip("www.")
    host_norm = hostname.lstrip("www.")
    mismatch = bool(label_host and host_norm and label_host != host_norm)
    return NormalizedValue(
        raw_value=raw,
        candidate_value=hostname or label,
        label_mismatch=mismatch,
    )


def is_domain_shape(candidate_value: str, lists: dict[str, Any] | None = None) -> bool:
    """08 R1 — candidate_value matches DOMAIN_REGEX and legal-suffix denylist."""
    lists = lists or load_pius_lists()
    value = candidate_value.strip().lower()
    if not value or " " in value:
        return False
    if not DOMAIN_LABEL_PATTERN.match(value):
        return False
    if _legal_suffix_hit(value, lists["legal_suffix_denylist"]):
        return False
    return True


def classify_record(record: dict[str, Any], lists: dict[str, Any] | None = None) -> EntityClassification | None:
    """08 R1/R2 — shape gates entity type; declared Type is advisory only."""
    lists = lists or load_pius_lists()
    raw_value = str(record.get("Value", "")).strip()
    if not raw_value:
        return None

    record_type = str(record.get("Type", "")).lower()
    source = str(record.get("Source", "")).lower()
    normalized = normalize_value(raw_value)
    candidate = normalized.candidate_value

    if record_type == "cidr" and "/" in candidate:
        return EntityClassification("NETBLOCK_OWNER", candidate, raw_value)

    if record_type == "preseed":
        if source == "whois" and is_known_registrar(candidate, lists):
            return EntityClassification(
                "DOMAIN_REGISTRAR",
                candidate,
                raw_value,
                is_registrar=True,
            )
        placeholder = is_placeholder_value(candidate, lists)
        return EntityClassification(
            "CANDIDATE_ENTITY",
            candidate,
            raw_value,
            is_placeholder=placeholder,
        )

    if record_type == "domain" and is_domain_shape(candidate, lists):
        return EntityClassification("DOMAIN_NAME", candidate.lower(), raw_value)

    if record_type == "domain":
        return EntityClassification("AFFILIATE_COMPANY_NAME", candidate, raw_value)

    return EntityClassification("AFFILIATE_COMPANY_NAME", candidate, raw_value)
