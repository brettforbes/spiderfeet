"""Unit tests for route catalog helpers."""

from spiderfeet.map.routes_catalog import (
    catalog_summary,
    expand_module_tests_for_service,
    expand_routes_for_service,
    list_module_summaries,
    module_catalog,
    module_test_id,
    route_name,
)


def test_route_name_format():
    assert route_name("DOMAIN_NAME", "IP_ADDRESS", "sfp_dnsresolve") == (
        "DOMAIN_NAME-to-IP_ADDRESS-via-sfp_dnsresolve"
    )


def test_expand_routes_cartesian():
    svc = {
        "module_id": "sfp_example",
        "consumed_nuggets": ["A", "B"],
        "produced_nuggets": ["X", "Y"],
    }
    routes = expand_routes_for_service(svc)
    assert len(routes) == 4
    names = {r.route_name for r in routes}
    assert "A-to-X-via-sfp_example" in names
    assert "B-to-Y-via-sfp_example" in names


def test_expand_module_tests_one_per_consumed():
    svc = {
        "module_id": "sfp_example",
        "consumed_nuggets": ["A", "B"],
        "produced_nuggets": ["X", "Y"],
    }
    tests = expand_module_tests_for_service(svc)
    assert len(tests) == 2
    assert tests[0].test_id == module_test_id("sfp_example", "A")
    assert tests[0].expected_produced_nugget_ids == ("X", "Y")
    assert len(tests[0].route_names) == 2


def test_catalog_summary_matches_osint_json():
    summary = catalog_summary()
    assert summary["module_count"] >= 170
    assert summary["test_count"] > summary["module_count"]
    assert summary["route_count"] >= summary["test_count"]


def test_list_module_summaries_search():
    rows = list_module_summaries(search="abstractapi")
    assert len(rows) >= 1
    assert all("abstractapi" in m.module_id.lower() for m in rows)


def test_module_catalog_unknown():
    assert module_catalog("sfp_does_not_exist_xyz") is None


def test_module_catalog_known():
    detail = module_catalog("sfp_abstractapi")
    assert detail is not None
    assert detail.test_count >= 1
    assert detail.test_count < detail.route_count
    assert detail.tests[0].module_id == "sfp_abstractapi"
