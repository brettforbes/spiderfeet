"""Resolve scan_ui consumed nuggets into SpiderFeet scan target value + type."""

from __future__ import annotations

from spiderfeet import SpiderFeetHelpers

# Catalogue nugget types used as explicit scan seeds (not CLI-regex inferrable).
CATALOGUE_SCAN_TARGET_TYPES = frozenset(
    {
        "COMPANY_NAME",
        "PHYSICAL_ADDRESS",
        "WEB_ANALYTICS_ID",
        "LEI",
    }
)

# Consumed nugget payloads passed verbatim as the scan seed event (Stage 5 quarantine).
PAYLOAD_NUGGET_TYPES = frozenset(
    {
        "AFFILIATE_DOMAIN_WHOIS",
        "BASE64_DATA",
        "CO_HOSTED_SITE_DOMAIN_WHOIS",
        "DARKNET_MENTION_CONTENT",
        "DNS_TEXT",
        "DOMAIN_WHOIS",
        "LEAKSITE_CONTENT",
        "LINKED_URL_INTERNAL",
        "LINKED_URL_EXTERNAL",
        "AFFILIATE_INTERNET_NAME",
        "AFFILIATE_INTERNET_NAME_UNRESOLVED",
        "PROVIDER_DNS",
        "NETBLOCK_WHOIS",
        "RAW_DNS_RECORDS",
        "RAW_FILE_META_DATA",
        "RAW_RIR_DATA",
        "SIMILARDOMAIN_WHOIS",
        "SOCIAL_MEDIA",
        "PUBLIC_CODE_REPO",
        "SSL_CERTIFICATE_RAW",
        "TARGET_WEB_CONTENT",
        "TCP_PORT_OPEN_BANNER",
        "WEBSERVER_BANNER",
        "WEBSERVER_HTTPHEADERS",
        "INTERESTING_FILE",
        "URL_PASSWORD",
        "URL_FORM",
        "URL_FLASH",
        "URL_STATIC",
        "URL_JAVA_APPLET",
        "URL_UPLOAD",
        "URL_JAVASCRIPT",
        "URL_WEB_FRAMEWORK",
    }
)


def normalize_scan_target(target: str, target_type: str) -> str:
    if target_type in ("HUMAN_NAME", "USERNAME", "BITCOIN_ADDRESS"):
        return target.replace('"', "")
    if target_type in CATALOGUE_SCAN_TARGET_TYPES:
        return target
    return target.lower()


def resolve_scan_ui_target(nugget_id: str, nugget_data: str) -> tuple[str, str]:
    """Map consumed nugget input to (target_value, target_type) for scan start."""
    anchor, anchor_type, _payload = resolve_scan_ui_seed(nugget_id, nugget_data)
    return anchor, anchor_type


def resolve_scan_ui_seed(
    nugget_id: str, nugget_data: str
) -> tuple[str, str, tuple[str, str] | None]:
    """
    Map consumed nugget to scan anchor target plus optional payload event.

    Content/payload nuggets use an INTERNET_NAME anchor (valid for SpiderFeetTarget)
    and inject the consumed event after ROOT in the scanner.
    """
    data = (nugget_data or "").strip()
    if not data:
        raise ValueError("blank nugget_data")

    if nugget_id in PAYLOAD_NUGGET_TYPES:
        anchor = "example.com"
        # External URL payloads keep example.com as scan target so cross-ref modules
        # can match affiliate links back to the intended smoke-test target.
        if nugget_id not in ("LINKED_URL_EXTERNAL",):
            if "://" in data:
                host = data.split("://", 1)[1].split("/")[0].split(":")[0]
                if SpiderFeetHelpers.targetTypeFromString(host) == "INTERNET_NAME":
                    anchor = host.lower()
            else:
                for token in data.replace("/", " ").split():
                    if SpiderFeetHelpers.targetTypeFromString(token) == "INTERNET_NAME":
                        anchor = token.lower()
                        break
        return anchor, "INTERNET_NAME", (nugget_id, data)

    inferred = SpiderFeetHelpers.targetTypeFromString(data)

    if nugget_id == "USERNAME" and inferred is None:
        quoted = data if (data.startswith('"') and data.endswith('"')) else f'"{data}"'
        if SpiderFeetHelpers.targetTypeFromString(quoted) == "USERNAME":
            return (
                normalize_scan_target(quoted, "USERNAME"),
                "USERNAME",
                None,
            )

    if inferred == nugget_id:
        return normalize_scan_target(data, inferred), inferred, None

    if inferred == "INTERNET_NAME" and nugget_id == "DOMAIN_NAME":
        return normalize_scan_target(data, "INTERNET_NAME"), "INTERNET_NAME", None

    if nugget_id in CATALOGUE_SCAN_TARGET_TYPES:
        return normalize_scan_target(data, nugget_id), nugget_id, None

    if inferred is not None:
        return normalize_scan_target(data, inferred), inferred, None

    raise ValueError("nugget_data is not a valid SpiderFeet target")
