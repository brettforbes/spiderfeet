#!/usr/bin/env python3
"""Generate conversion_to_types/02-nugget-type-catalog.md from nuggets.json + catalogue."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".seed" / "scripts"))

from nugget_purpose_text import all_purposes, purpose_for  # noqa: E402

NUGGETS_JSON = REPO_ROOT / ".docs" / "analysis" / "nuggets.json"
PURPOSES_JSON = REPO_ROOT / ".docs" / "analysis" / "nugget_purposes.json"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
OUT_MD = REPO_ROOT / ".docs" / "analysis" / "conversion_to_types" / "02-nugget-type-catalog.md"

# Ordered groups: (title, nugget_ids in display order — entity then related types)
CATALOG_GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "Scan control",
        "Internal types; not OSINT findings.",
        ["ROOT"],
    ),
    (
        "Accounts & usernames",
        "External accounts and identity handles.",
        [
            "ACCOUNT_EXTERNAL_OWNED",
            "ACCOUNT_EXTERNAL_OWNED_COMPROMISED",
            "ACCOUNT_EXTERNAL_USER_SHARED_COMPROMISED",
            "SIMILAR_ACCOUNT_EXTERNAL",
            "USERNAME",
            "SOCIAL_MEDIA",
        ],
    ),
    (
        "Domains & registration",
        "Owned and related domain entities.",
        [
            "DOMAIN_NAME",
            "DOMAIN_NAME_PARENT",
            "DOMAIN_REGISTRAR",
            "DOMAIN_WHOIS",
            "SIMILARDOMAIN",
            "SIMILARDOMAIN_WHOIS",
            "DESCRIPTION_CATEGORY",
            "DESCRIPTION_ABSTRACT",
        ],
    ),
    (
        "Affiliate domains & metadata",
        "Third-party / neighbouring domain assets.",
        [
            "AFFILIATE_DOMAIN_NAME",
            "AFFILIATE_DOMAIN_UNREGISTERED",
            "AFFILIATE_DOMAIN_WHOIS",
            "AFFILIATE_COMPANY_NAME",
            "AFFILIATE_DESCRIPTION_CATEGORY",
            "AFFILIATE_DESCRIPTION_ABSTRACT",
        ],
    ),
    (
        "Internet names & hostnames",
        "Resolvable names tied to the footprint.",
        [
            "INTERNET_NAME",
            "INTERNET_NAME_UNRESOLVED",
            "AFFILIATE_INTERNET_NAME",
            "AFFILIATE_INTERNET_NAME_UNRESOLVED",
            "AFFILIATE_INTERNET_NAME_HIJACKABLE",
        ],
    ),
    (
        "Co-hosted sites",
        "Shared hosting relationships.",
        [
            "CO_HOSTED_SITE",
            "CO_HOSTED_SITE_DOMAIN",
            "CO_HOSTED_SITE_DOMAIN_WHOIS",
            "BLACKLISTED_COHOST",
            "DEFACED_COHOST",
            "MALICIOUS_COHOST",
        ],
    ),
    (
        "IP addresses & netblocks",
        "Layer-3 identifiers and allocations.",
        [
            "IP_ADDRESS",
            "IPV6_ADDRESS",
            "INTERNAL_IP_ADDRESS",
            "AFFILIATE_IPADDR",
            "AFFILIATE_IPV6_ADDRESS",
            "NETBLOCK_OWNER",
            "NETBLOCK_MEMBER",
            "NETBLOCKV6_OWNER",
            "NETBLOCKV6_MEMBER",
            "NETBLOCK_WHOIS",
            "GEOINFO",
            "TOR_EXIT_NODE",
            "PROXY_HOST",
            "VPN_HOST",
        ],
    ),
    (
        "BGP & providers",
        "ASN and infrastructure provider attribution.",
        [
            "BGP_AS_OWNER",
            "BGP_AS_MEMBER",
            "MALICIOUS_ASN",
            "PROVIDER_DNS",
            "PROVIDER_MAIL",
            "PROVIDER_HOSTING",
            "PROVIDER_TELCO",
            "PROVIDER_JAVASCRIPT",
        ],
    ),
    (
        "Ports, OS & device fingerprint",
        "Active scan and fingerprint outputs.",
        [
            "TCP_PORT_OPEN",
            "TCP_PORT_OPEN_BANNER",
            "UDP_PORT_OPEN",
            "UDP_PORT_OPEN_INFO",
            "OPERATING_SYSTEM",
            "DEVICE_TYPE",
            "WEBSERVER_BANNER",
            "WEBSERVER_HTTPHEADERS",
            "WEBSERVER_STRANGEHEADER",
            "WEBSERVER_TECHNOLOGY",
            "SOFTWARE_USED",
        ],
    ),
    (
        "DNS records",
        "Structured DNS payloads.",
        [
            "DNS_SPF",
            "DNS_SRV",
            "DNS_TEXT",
            "RAW_DNS_RECORDS",
        ],
    ),
    (
        "Web content & analytics",
        "Pages, cookies, and tracking identifiers.",
        [
            "TARGET_WEB_CONTENT",
            "TARGET_WEB_CONTENT_TYPE",
            "TARGET_WEB_COOKIE",
            "AFFILIATE_WEB_CONTENT",
            "SEARCH_ENGINE_WEB_CONTENT",
            "HTTP_CODE",
            "WEB_ANALYTICS_ID",
        ],
    ),
    (
        "Linked URLs",
        "Internal vs external link graph.",
        [
            "LINKED_URL_INTERNAL",
            "LINKED_URL_EXTERNAL",
            "URL_ADBLOCKED_INTERNAL",
            "URL_ADBLOCKED_EXTERNAL",
        ],
    ),
    (
        "URL surface types (current)",
        "Page behaviour classification from spider/pageinfo.",
        [
            "URL_FORM",
            "URL_JAVASCRIPT",
            "URL_STATIC",
            "URL_FLASH",
            "URL_JAVA_APPLET",
            "URL_WEB_FRAMEWORK",
            "URL_PASSWORD",
            "URL_UPLOAD",
        ],
    ),
    (
        "URL surface types (historic)",
        "Archive-derived URL classifications.",
        [
            "URL_FORM_HISTORIC",
            "URL_JAVASCRIPT_HISTORIC",
            "URL_STATIC_HISTORIC",
            "URL_FLASH_HISTORIC",
            "URL_JAVA_APPLET_HISTORIC",
            "URL_WEB_FRAMEWORK_HISTORIC",
            "URL_PASSWORD_HISTORIC",
            "URL_UPLOAD_HISTORIC",
        ],
    ),
    (
        "SSL / TLS certificates",
        "Certificate entities and lifecycle descriptors.",
        [
            "SSL_CERTIFICATE_ISSUED",
            "SSL_CERTIFICATE_ISSUER",
            "SSL_CERTIFICATE_RAW",
            "SSL_CERTIFICATE_MISMATCH",
            "SSL_CERTIFICATE_EXPIRED",
            "SSL_CERTIFICATE_EXPIRING",
        ],
    ),
    (
        "Email addresses",
        "Mailbox entities and validation/compromise states.",
        [
            "EMAILADDR",
            "EMAILADDR_GENERIC",
            "EMAILADDR_COMPROMISED",
            "EMAILADDR_DELIVERABLE",
            "EMAILADDR_UNDELIVERABLE",
            "EMAILADDR_DISPOSABLE",
            "AFFILIATE_EMAILADDR",
            "MALICIOUS_EMAILADDR",
        ],
    ),
    (
        "Phone numbers",
        "Telephone entities and metadata.",
        [
            "PHONE_NUMBER",
            "PHONE_NUMBER_TYPE",
            "PHONE_NUMBER_COMPROMISED",
            "MALICIOUS_PHONE_NUMBER",
        ],
    ),
    (
        "People, organisations & location",
        "Real-world identity and org entities.",
        [
            "HUMAN_NAME",
            "JOB_TITLE",
            "DATE_HUMAN_DOB",
            "COMPANY_NAME",
            "COUNTRY_NAME",
            "PHYSICAL_ADDRESS",
            "PHYSICAL_COORDINATES",
            "LEI",
        ],
    ),
    (
        "Credentials, cards & banking",
        "Sensitive financial identifiers.",
        [
            "CREDIT_CARD_NUMBER",
            "IBAN_NUMBER",
            "PASSWORD_COMPROMISED",
            "HASH",
            "HASH_COMPROMISED",
            "BASE64_DATA",
        ],
    ),
    (
        "Cryptocurrency",
        "On-chain addresses and balances.",
        [
            "BITCOIN_ADDRESS",
            "BITCOIN_BALANCE",
            "MALICIOUS_BITCOIN_ADDRESS",
            "ETHEREUM_ADDRESS",
            "ETHEREUM_BALANCE",
        ],
    ),
    (
        "Files & interesting content",
        "Discovered files and leak-adjacent blobs.",
        [
            "INTERESTING_FILE",
            "INTERESTING_FILE_HISTORIC",
            "JUNK_FILE",
            "LEAKSITE_URL",
            "LEAKSITE_CONTENT",
            "DARKNET_MENTION_URL",
            "DARKNET_MENTION_CONTENT",
            "PGP_KEY",
        ],
    ),
    (
        "Cloud & app stores",
        "Exposed buckets and mobile store entries.",
        [
            "CLOUD_STORAGE_BUCKET",
            "CLOUD_STORAGE_BUCKET_OPEN",
            "APPSTORE_ENTRY",
            "PUBLIC_CODE_REPO",
        ],
    ),
    (
        "Reputation — internet names",
        "Blacklist / deface / malicious overlays on names.",
        [
            "BLACKLISTED_INTERNET_NAME",
            "BLACKLISTED_AFFILIATE_INTERNET_NAME",
            "DEFACED_INTERNET_NAME",
            "DEFACED_AFFILIATE_INTERNET_NAME",
            "MALICIOUS_INTERNET_NAME",
            "MALICIOUS_AFFILIATE_INTERNET_NAME",
        ],
    ),
    (
        "Reputation — IP & netblocks",
        "Threat overlays on addresses and ranges.",
        [
            "BLACKLISTED_IPADDR",
            "BLACKLISTED_AFFILIATE_IPADDR",
            "BLACKLISTED_SUBNET",
            "BLACKLISTED_NETBLOCK",
            "DEFACED_IPADDR",
            "DEFACED_AFFILIATE_IPADDR",
            "MALICIOUS_IPADDR",
            "MALICIOUS_AFFILIATE_IPADDR",
            "MALICIOUS_SUBNET",
            "MALICIOUS_NETBLOCK",
        ],
    ),
    (
        "Vulnerabilities",
        "CVE tiers and general findings.",
        [
            "VULNERABILITY_GENERAL",
            "VULNERABILITY_DISCLOSURE",
            "VULNERABILITY_CVE_CRITICAL",
            "VULNERABILITY_CVE_HIGH",
            "VULNERABILITY_CVE_MEDIUM",
            "VULNERABILITY_CVE_LOW",
        ],
    ),
    (
        "WiFi & misc network",
        "Wireless and error surfaces.",
        [
            "WIFI_ACCESS_POINT",
            "ERROR_MESSAGE",
            "WIKIPEDIA_PAGE_EDIT",
        ],
    ),
    (
        "Raw API & registry payloads",
        "Opaque evidence retained for audit and re-parse.",
        [
            "RAW_RIR_DATA",
            "RAW_FILE_META_DATA",
        ],
    ),
]

# Typical data encoding hints (subset — high-traffic types)
DATA_ENCODING: dict[str, str] = {
    "IP_ADDRESS": "IPv4 literal, e.g. `8.8.8.8`",
    "IPV6_ADDRESS": "IPv6 literal",
    "TCP_PORT_OPEN": "`ip:port` string",
    "TCP_PORT_OPEN_BANNER": "Banner text; source event often port",
    "UDP_PORT_OPEN": "`ip:port`",
    "OPERATING_SYSTEM": "OS guess text, often with IP in parentheses",
    "GEOINFO": "City, country (comma-separated)",
    "EMAILADDR": "RFC5322-like address",
    "DOMAIN_NAME": "FQDN or registrable domain",
    "INTERNET_NAME": "Hostname",
    "NETBLOCK_OWNER": "CIDR, e.g. `192.0.2.0/24`",
    "RAW_RIR_DATA": "`str(api_dict)` or JSON-like blob",
    "WEB_ANALYTICS_ID": "`Network: id`",
    "VULNERABILITY_CVE_CRITICAL": "CVE description from `sf.cveInfo()`",
    "HASH": "Hex digest",
    "USERNAME": "Handle string",
}


def catalogue_counts() -> tuple[Counter[str], Counter[str]]:
    """Count appearances in osint_services.json consumed_nuggets / produced_nuggets."""
    consumed: Counter[str] = Counter()
    produced: Counter[str] = Counter()
    services = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    for svc in services:
        for c in svc.get("consumed_nuggets") or []:
            consumed[c] += 1
        for p in svc.get("produced_nuggets") or []:
            produced[p] += 1
    return consumed, produced


def load_nuggets() -> dict[str, dict]:
    rows = json.loads(NUGGETS_JSON.read_text(encoding="utf-8"))
    return {r["nugget_id"]: r for r in rows}


def load_purposes(nuggets: dict[str, dict]) -> dict[str, str]:
    """Merge curated JSON overrides with built-in purpose text."""
    merged = all_purposes(nuggets)
    if PURPOSES_JSON.is_file():
        overrides = json.loads(PURPOSES_JSON.read_text(encoding="utf-8"))
        for nid, text in overrides.items():
            if nid in nuggets and text:
                merged[nid] = str(text).strip()
    return merged


def md_cell(text: str) -> str:
    """Escape text for markdown table cells."""
    return str(text or "—").replace("|", "\\|").replace("\n", " ")


def sync_purposes_json(nuggets: dict[str, dict], purposes: dict[str, str]) -> None:
    """Write nugget_purposes.json when missing or when curated keys are absent."""
    baseline = all_purposes(nuggets)
    if not PURPOSES_JSON.is_file():
        PURPOSES_JSON.write_text(
            json.dumps(baseline, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return
    existing = json.loads(PURPOSES_JSON.read_text(encoding="utf-8"))
    changed = False
    for nid in sorted(nuggets.keys()):
        if nid not in existing:
            existing[nid] = baseline[nid]
            changed = True
    if changed:
        PURPOSES_JSON.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def archetype_label(t: str) -> str:
    return {
        "ENTITY": "Entity",
        "DESCRIPTOR": "Descriptor",
        "DATA": "Data",
        "SUBENTITY": "Sub-entity",
        "INTERNAL": "Internal",
    }.get(t, t)


def catalogue_cell(cid: str, consumed: Counter[str], produced: Counter[str]) -> str:
    c, p = consumed[cid], produced[cid]
    if c == 0 and p == 0:
        return "—"
    return f"C:{c} / P:{p}"


def row(
    nid: str,
    meta: dict,
    consumed: Counter[str],
    produced: Counter[str],
    purposes: dict[str, str],
) -> str:
    desc = md_cell(meta.get("nugget_description", ""))
    purpose = md_cell(purposes.get(nid, ""))
    archetype = archetype_label(meta.get("nugget_type", ""))
    icon = meta.get("nugget_icon", "")
    colour = meta.get("nugget_colour", "")
    enc = DATA_ENCODING.get(nid, "")
    cat = catalogue_cell(nid, consumed, produced)
    enc_cell = md_cell(enc) if enc else "—"
    return (
        f"| `{nid}` | {desc} | {purpose} | {archetype} | `{icon}` | `{colour}` | {cat} | {enc_cell} |"
    )


def table_header() -> str:
    return (
        "| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | "
        "Catalogue (consume / produce) | Typical `data` encoding |\n"
        "|-----------|-------------|----------------------|-----------|------|--------|"
        "------------------------------|-------------------------|"
    )


def main() -> int:
    nuggets = load_nuggets()
    sync_purposes_json(nuggets, {})
    purposes = load_purposes(nuggets)
    consumed, produced = catalogue_counts()
    all_ids = set(nuggets.keys())

    grouped_ids: list[str] = []
    for _, _, ids in CATALOG_GROUPS:
        grouped_ids.extend(ids)

    missing = sorted(all_ids - set(grouped_ids))
    if missing:
        CATALOG_GROUPS.append(
            (
                "Ungrouped (add to script)",
                "Nuggets not yet assigned to a semantic group.",
                missing,
            )
        )

    lines = [
        "# Nugget type catalog",
        "",
        "Canonical source: [`.docs/analysis/nuggets.json`](../nuggets.json) — **172** archetype definitions.",
        "",
        "In SpiderFeet code these are **event types** (`eventType` on `SpiderFeetEvent`). "
        "In the map UI they are **nuggets**.",
        "",
        "## How to read this catalog",
        "",
        "| Column | Meaning |",
        "|--------|---------|",
        "| **Purpose & definition** | What this type represents in an investigation, why it exists, and how to interpret it "
        "in the event chain. Curated in [`nugget_purposes.json`](../nugget_purposes.json). |",
        "| **Archetype** | `Entity` = identifiable thing; `Descriptor` = state/classification on an entity; "
        "`Data` = bulk payload; `Sub-entity` = component of a parent (port, URL, software); `Internal` = scan control |",
        "| **Catalogue (consume / produce)** | Count of **OSINT services** in `osint_services.json` "
        "listing this type in `consumed_nuggets` (`C`) or `produced_nuggets` (`P`). "
        "One service = one module route declaration (231 services). |",
        "| **Typical `data` encoding** | Conventional string shape in `SpiderFeetEvent.data` (not schema-enforced). |",
        "",
        "Within each section, **entities and sub-entities are listed first**, then **descriptors**, "
        "**data**, and **states** that annotate the same subject (e.g. `EMAILADDR` then `EMAILADDR_COMPROMISED`).",
        "",
        "Regenerate: `poetry run python .seed/scripts/generate_nugget_type_catalog.py`",
        "",
        "## Summary statistics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Archetype definitions | {len(nuggets)} |",
        f"| Types with ≥1 catalogue produce route | {sum(1 for k in nuggets if produced[k])} |",
        f"| Types with ≥1 catalogue consume route | {sum(1 for k in nuggets if consumed[k])} |",
        f"| Types unused in catalogue routes | {sum(1 for k in nuggets if not consumed[k] and not produced[k])} |",
        "",
        "Producer module counts (from `producedEvents()`): [nugget_type_producers.md](nugget_type_producers.md).",
        "",
        "## Archetype layers",
        "",
        "| `nugget_type` | Count | Graph role (intended) |",
        "|---------------|-------|------------------------|",
    ]

    type_counts: Counter[str] = Counter()
    for m in nuggets.values():
        type_counts[m.get("nugget_type", "?")] += 1
    for t in ["INTERNAL", "ENTITY", "SUBENTITY", "DESCRIPTOR", "DATA"]:
        if t in type_counts:
            role = {
                "INTERNAL": "Scan anchor, not OSINT",
                "ENTITY": "First-class node",
                "SUBENTITY": "Part of parent entity (port, link, software)",
                "DESCRIPTOR": "State or classification on entity",
                "DATA": "Evidence blob / opaque payload",
            }[t]
            lines.append(f"| `{t}` | {type_counts[t]} | {role} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    for title, blurb, ids in CATALOG_GROUPS:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(blurb)
        lines.append("")
        lines.append(table_header())
        for nid in ids:
            if nid not in nuggets:
                lines.append(f"| `{nid}` | _missing from nuggets.json_ | — | — | — | — | — |")
                continue
            lines.append(row(nid, nuggets[nid], consumed, produced, purposes))
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Extending the catalog",
        "",
        "Adding a type requires: row in `nuggets.json`, TypeDB entity in `spiderfeet_map.tql`, "
        "module `producedEvents()` + emission code, catalogue route + test seed. "
        "See [06-recommendations-and-roadmap.md](06-recommendations-and-roadmap.md).",
        "",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD} ({len(nuggets)} types, {len(CATALOG_GROUPS)} groups)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
