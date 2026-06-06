"""Default test target values per consumed nugget_id (Stage 4c pilot).

Module-specific seeds live in ``.docs/analysis/module_test_seeds.json`` (Stage 4b).
Generic nugget fallbacks remain here until the full corpus ships (SF-04B-06).
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Dict, Optional

from spiderfeet import SpiderFeetHelpers
from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON

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
    "EMAILADDR": "noreply@spiderfoot.net",
    "ETHEREUM_ADDRESS": "0x0000000000000000000000000000000000000000",
    "HUMAN_NAME": '"Jane Citizen"',
    "INTERESTING_FILE": "sbs.com.au",
    "INTERNET_NAME": "sbs.com.au",
    "INTERNET_NAME_UNRESOLVED": "does-not-resolve.example",
    "IPV6_ADDRESS": "2001:4860:4860::8888",
    "IP_ADDRESS": "8.8.8.8",
    "LEI": "sbs.com.au",
    "LINKED_URL_EXTERNAL": "sbs.com.au",
    "LINKED_URL_INTERNAL": "https://example.com/",
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


@lru_cache(maxsize=1)
def load_module_test_seeds() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Return module_id → consumed_nugget_id → seed metadata from JSON registry."""
    if not MODULE_TEST_SEEDS_JSON.is_file():
        return {}
    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.get("seeds") or {}
    if not isinstance(seeds, dict):
        return {}
    return seeds


def registry_input_value(module_id: str, consumed_nugget_id: str) -> Optional[str]:
    """Lookup module-specific seed input, if registered."""
    module_seeds = load_module_test_seeds().get(module_id) or {}
    entry = module_seeds.get(consumed_nugget_id) or {}
    raw = entry.get("input_value")
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    if SpiderFeetHelpers.targetTypeFromString(text) is None:
        return None
    return text


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
    1) module_test_seeds.json registry entry
    2) module route_seed_nugget sample (if compatible)
    3) generic nugget sample
    """
    registry_value = registry_input_value(module_id, consumed_nugget_id)
    if registry_value:
        return registry_value

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


def pilot_module_ids() -> list[str]:
    """Module IDs with entries in the seed registry (Stage 4b pilot)."""
    return sorted(load_module_test_seeds().keys())
