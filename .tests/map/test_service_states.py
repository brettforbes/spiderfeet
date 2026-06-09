"""Operator UI visibility for error-state OSINT services."""

from spiderfeet.map.routes_catalog import list_module_summaries, module_catalog
from spiderfeet.map.service_states import (
    UPSTREAM_ERROR_MODULE_IDS,
    include_in_operator_ui,
    service_state_for_service,
)


def test_upstream_error_modules_marked_error():
    modules = {m.module_id for m in list_module_summaries()}
    for module_id in UPSTREAM_ERROR_MODULE_IDS:
        assert module_id not in modules
        assert module_catalog(module_id, operator_ui=True) is None


def test_service_state_from_catalog():
    from spiderfeet.map.routes_catalog import service_by_module_id

    svc = service_by_module_id("sfp_dnsdumpster")
    assert svc is not None
    assert service_state_for_service(svc) == "error"
    assert include_in_operator_ui(svc) is False
