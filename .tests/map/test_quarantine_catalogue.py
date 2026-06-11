"""Stage 5 quarantine catalogue extraction (SPEC-003 R3-05-01)."""

import sys
from pathlib import Path

_ANALYSIS = Path(__file__).resolve().parents[2] / ".docs" / "analysis"
sys.path.insert(0, str(_ANALYSIS))

from analyse_modules import (
    analyse_quarantine_modules,
    parse_quarantine_module,
    service_icon_path,
)

MODULES = Path(__file__).resolve().parents[2] / "modules"


def test_quarantine_module_count():
    services = analyse_quarantine_modules()
    assert len(services) == 54


def test_dnsresolve_quarantine_record():
    svc = parse_quarantine_module(MODULES / "sfp_dnsresolve.py")
    assert svc is not None
    assert svc["service_origin"] == "local"
    assert svc["service_state"] == "quarantine"
    assert svc["access_tier"] == "free_no_auth"
    assert "INTERNET_NAME" in svc["consumed_nuggets"]
    assert "IP_ADDRESS" in svc["produced_nuggets"]
    assert svc["data_source"]["model"] == "LOCAL_NOAUTH"
    assert svc["data_source"]["website"].startswith("spiderfeet://local/")


def test_dnsbrute_override_consumed():
    svc = parse_quarantine_module(MODULES / "sfp_dnsbrute.py")
    assert svc is not None
    assert set(svc["consumed_nuggets"]) == {"DOMAIN_NAME", "INTERNET_NAME"}
    assert svc["route_seed_nugget"] == "DOMAIN_NAME"


def test_countryname_route_seed_override():
    svc = parse_quarantine_module(MODULES / "sfp_countryname.py")
    assert svc is not None
    assert svc["route_seed_nugget"] == "TARGET_WEB_CONTENT"


def test_service_icon_path():
    assert service_icon_path("sfp_dnsresolve") == "icons/icon_service_dnsresolve.svg"


def test_tool_module_origin_is_cli():
    svc = parse_quarantine_module(MODULES / "sfp_tool_nmap.py")
    assert svc is not None
    assert svc["service_origin"] == "cli"
    assert svc["service_state"] == "quarantine"
