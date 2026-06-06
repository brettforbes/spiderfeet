"""Default test target values per consumed nugget_id (Stage 4c pilot).

Full corpus lives in ``test_nugget_data.csv`` (Stage 4b). Until that ships,
these samples enable route smoke tests from the Tests tab.
"""

from __future__ import annotations

from typing import Dict, Optional

from spiderfeet import SpiderFeetHelpers

# Keys are catalogue nugget_id values from osint_services consumed_nuggets.
_NUGGET_SAMPLES: Dict[str, str] = {
    "AFFILIATE_DOMAIN_NAME": "affiliate.sbs.com.au",
    "AFFILIATE_INTERNET_NAME": "affiliate.sbs.com.au",
    "AFFILIATE_INTERNET_NAME_UNRESOLVED": "missing-affiliate.example",
    "AFFILIATE_IPADDR": "8.8.8.8",
    "AFFILIATE_IPV6_ADDRESS": "2001:4860:4860::8888",
    "BGP_AS_MEMBER": "15169",
    "BGP_AS_OWNER": "15169",
    "BITCOIN_ADDRESS": "1HesYJSP1QqcyPEjnQ9vzBL1wujruNGe7R",
    "COMPANY_NAME": "sbs.com.au",
    "CO_HOSTED_SITE": "sbs.com.au",
    "DOMAIN_NAME": "sbs.com.au",
    "DOMAIN_NAME_PARENT": "com.au",
    "EMAILADDR": "noreply@spiderfeet.net",
    "ETHEREUM_ADDRESS": "0x0000000000000000000000000000000000000000",
    "HUMAN_NAME": '"Jane Citizen"',
    "INTERESTING_FILE": "sbs.com.au",
    "INTERNET_NAME": "sbs.com.au",
    "INTERNET_NAME_UNRESOLVED": "does-not-resolve.example",
    "IPV6_ADDRESS": "2001:4860:4860::8888",
    "IP_ADDRESS": "8.8.8.8",
    "LEI": "sbs.com.au",
    "LINKED_URL_EXTERNAL": "sbs.com.au",
    "LINKED_URL_INTERNAL": "sbs.com.au",
    "NETBLOCKV6_MEMBER": "2001:4860::/32",
    "NETBLOCKV6_OWNER": "2001:4860::/32",
    "NETBLOCK_MEMBER": "8.8.8.0/24",
    "NETBLOCK_OWNER": "8.8.8.0/24",
    "PHONE_NUMBER": "+61412345678",
    "PHYSICAL_ADDRESS": "sbs.com.au",
    "PHYSICAL_COORDINATES": "sbs.com.au",
    "PROVIDER_DNS": "8.8.8.8",
    "PROVIDER_JAVASCRIPT": "sbs.com.au",
    "SOCIAL_MEDIA": "sbs.com.au",
    "URL_FLASH": "sbs.com.au",
    "URL_FORM": "sbs.com.au",
    "URL_JAVASCRIPT": "sbs.com.au",
    "URL_JAVA_APPLET": "sbs.com.au",
    "URL_PASSWORD": "sbs.com.au",
    "URL_STATIC": "sbs.com.au",
    "URL_UPLOAD": "sbs.com.au",
    "URL_WEB_FRAMEWORK": "sbs.com.au",
    "USERNAME": '"spiderfeet"',
    "WEB_ANALYTICS_ID": "sbs.com.au",
}

# Module-specific seed overrides to improve yield for modules with strict inputs.
# Key format: (module_id, consumed_nugget_id)
_MODULE_SEED_OVERRIDES: Dict[tuple[str, str], str] = {
    ("sfp_emailrep", "EMAILADDR"): "security@spiderfoot.net",
    ("sfp_haveibeenpwned", "EMAILADDR"): "security@spiderfoot.net",
    ("sfp_dnsdb", "DOMAIN_NAME"): "sbs.com.au",
}


def sample_target_for_nugget(nugget_id: str) -> Optional[str]:
    """Return a SpiderFeet-valid scan target for ``nugget_id``, if known."""
    raw = _NUGGET_SAMPLES.get(nugget_id)
    if not raw:
        return None
    if SpiderFeetHelpers.targetTypeFromString(raw) is None:
        return None
    return raw


def sample_target_for_module(
    module_id: str,
    consumed_nugget_id: str,
    route_seed_nugget: Optional[str] = None,
) -> Optional[str]:
    """Return the best seed target for a module test.

    Preference order:
    1) module+consumed override
    2) module route_seed_nugget sample (if compatible)
    3) generic nugget sample
    """
    override = _MODULE_SEED_OVERRIDES.get((module_id, consumed_nugget_id))
    if override and SpiderFeetHelpers.targetTypeFromString(override) is not None:
        return override

    if route_seed_nugget and route_seed_nugget == consumed_nugget_id:
        route_seed = sample_target_for_nugget(route_seed_nugget)
        if route_seed:
            return route_seed

    return sample_target_for_nugget(consumed_nugget_id)


def all_nugget_samples() -> Dict[str, str]:
    """Return validated samples keyed by nugget_id (omits invalid entries)."""
    out: Dict[str, str] = {}
    for nugget_id, value in sorted(_NUGGET_SAMPLES.items()):
        if SpiderFeetHelpers.targetTypeFromString(value) is not None:
            out[nugget_id] = value
    return out
