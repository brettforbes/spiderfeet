"""Catalogue coverage tests for SPEC-004 CLI graph nuggets."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOGUE_PATHS = (
    REPO_ROOT / ".docs" / "analysis" / "nuggets.json",
    REPO_ROOT / ".docs" / "analysis" / "nuggets_extension.json",
)
EXTENSION_PATH = REPO_ROOT / ".docs" / "analysis" / "nuggets_extension.json"

SPEC004_REQUIRED_IDS = {
    "SYSTEM",
    "CDN",
    "SCAN_ARGS",
    "SCAN_TIMESTAMP",
    "SCAN_END_TIME",
    "SCAN_EXIT_STATUS",
    "SCAN_TRIES",
    "SCAN_EMPTY_SCANS",
    "SCAN_DISCOVERED",
    "MAC_VENDOR",
    "RECORD_ID",
    "IP_VERSION",
    "SAME_SYSTEM_GROUP_ID",
    "SAME_SYSTEM_CONFIDENCE",
    "SAME_SYSTEM_EVIDENCE",
    "HOST_CLASSIFICATION",
    "CLASSIFICATION_CONFIDENCE",
    "CLASSIFICATION_RULE_FIRED",
    "CDN_VENDOR",
    "CDN_VENDOR_CONFIDENCE",
    "CDN_DETECTION_SIGNAL",
    "CDN_ASN",
    "CDN_ASN_ORG",
    "CDN_PRODUCT_HINT",
    "CDN_POP_CODE",
    "EDGE_NODE_ID",
    "ANYCAST_SUSPECTED",
    "CACHE_STATUS",
    "EDGE_DURATION_MS",
    "ORIGIN_DURATION_MS",
    "PROTOCOLS_OFFERED",
    "HSTS_ENABLED",
    "HSTS_MAX_AGE",
    "HSTS_PRELOAD",
    "HSTS_INCLUDE_SUBDOMAINS",
    "CSP_PRESENT",
    "CSP_THIRD_PARTY_DOMAIN",
    "NEL_ACTIVE",
    "NEL_REPORT_ENDPOINT",
    "WAF_BOT_MANAGEMENT_DETECTED",
    "WAF_VENDOR_HINT",
    "RESPONSE_HEADERS_RAW",
    "REDIRECT_LOCATION",
    "SERVER_HEADER",
    "ORIGIN_HOST_COUNT",
    "ORIGIN_IP",
    "ORIGIN_TECHNOLOGY",
    "ORIGIN_FINGERPRINT_SUPPRESSED",
    "ORIGIN_FINGERPRINT_RAW",
}


def _load_records(path: Path) -> list[dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_spec004_netdiscover_and_nerva_catalogue_ids_exist():
    catalogue_ids = {
        record["nugget_id"]
        for path in CATALOGUE_PATHS
        for record in _load_records(path)
    }

    assert SPEC004_REQUIRED_IDS <= catalogue_ids


def test_nuggets_extension_ids_are_unique():
    ids = [record["nugget_id"] for record in _load_records(EXTENSION_PATH)]
    duplicates = [nugget_id for nugget_id, count in Counter(ids).items() if count > 1]

    assert duplicates == []
