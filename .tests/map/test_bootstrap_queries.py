"""Unit tests for TypeQL bootstrap query builders (no server)."""

from unittest.mock import MagicMock, patch

from spiderfeet.map.bootstrap import (
    build_nugget_insert_query,
    build_role_link_query,
    build_schema_extension_ddl,
    build_service_insert_queries,
    ensure_map_ready,
    needs_map_bootstrap,
)


def test_needs_map_bootstrap_when_database_missing():
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    driver = MagicMock()
    driver.databases.contains.return_value = False
    session = MagicMock()
    session.__enter__.return_value = driver
    session.__exit__.return_value = False

    with patch("spiderfeet.map.bootstrap.driver_session", return_value=session):
        assert needs_map_bootstrap(cfg) is True


def test_needs_map_bootstrap_when_schema_missing():
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    driver = MagicMock()
    driver.databases.contains.return_value = True
    session = MagicMock()
    session.__enter__.return_value = driver
    session.__exit__.return_value = False

    with patch("spiderfeet.map.bootstrap.driver_session", return_value=session), patch(
        "spiderfeet.map.bootstrap.schema_already_loaded", return_value=False
    ):
        assert needs_map_bootstrap(cfg) is True


def test_needs_map_bootstrap_when_catalogue_empty():
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    driver = MagicMock()
    driver.databases.contains.return_value = True
    session = MagicMock()
    session.__enter__.return_value = driver
    session.__exit__.return_value = False

    with patch("spiderfeet.map.bootstrap.driver_session", return_value=session), patch(
        "spiderfeet.map.bootstrap.schema_already_loaded", return_value=True
    ), patch(
        "spiderfeet.map.bootstrap.catalogue_seeded", return_value=False
    ):
        assert needs_map_bootstrap(cfg) is True


def test_ensure_map_ready_skips_when_ready():
    cfg = MagicMock()
    with patch(
        "spiderfeet.map.bootstrap.needs_map_bootstrap", return_value=False
    ), patch("spiderfeet.map.bootstrap.bootstrap_map") as bootstrap:
        assert ensure_map_ready(cfg) is False
        bootstrap.assert_not_called()


def test_ensure_map_ready_runs_bootstrap_when_needed():
    cfg = MagicMock()
    with patch(
        "spiderfeet.map.bootstrap.needs_map_bootstrap", return_value=True
    ), patch("spiderfeet.map.bootstrap.bootstrap_map") as bootstrap:
        assert ensure_map_ready(cfg) is True
        bootstrap.assert_called_once_with(cfg, database=None)



def test_build_nugget_insert_query():
    q = build_nugget_insert_query(
        {
            "nugget_id": "INTERNET_NAME",
            "nugget_description": "Internet Name",
            "nugget_type": "ENTITY",
            "nugget_icon": "icon_internet_name.svg",
            "nugget_colour": "#3B82F6",
        }
    )
    assert "isa internet-name" in q
    assert 'has nugget_id "INTERNET_NAME"' in q
    assert 'has nugget_instance_id "archetype:INTERNET_NAME"' in q


def test_build_service_insert_queries():
    queries = build_service_insert_queries(
        {
            "module_id": "sfp_dnsresolve",
            "name": "DNS Resolve",
            "summary": "Resolve hosts.",
            "flags": [],
            "use_cases": ["Footprint"],
            "categories": ["DNS"],
            "access_tier": "free_no_auth",
            "consumed_nuggets": ["INTERNET_NAME"],
            "produced_nuggets": ["IP_ADDRESS"],
            "service_origin": "local",
            "service_state": "quarantine",
            "data_source": {"website": "spiderfeet://local/sfp_dnsresolve", "model": "LOCAL_NOAUTH"},
        }
    )
    assert len(queries) >= 2
    assert "isa sfp-dnsresolve" in queries[0]
    assert 'has module_id "sfp_dnsresolve"' in queries[0]
    assert 'has service_state "quarantine"' in queries[0]
    assert 'has service_origin "local"' in queries[0]
    assert 'has fixture_category "positive"' in queries[0]
    assert "links (consumed: $nug0)" in queries[0]
    assert "links (produced: $nug1)" in queries[0]
    assert "has use_cases " in queries[0] and "Footprint" in queries[0]
    assert any("isa osint-source" in q for q in queries)
    assert any("isa data-source" in q for q in queries)


def test_build_role_link_query():
    q = build_role_link_query("sfp_dnsresolve", "INTERNET_NAME", "consumed")
    assert "sfp-dnsresolve" in q
    assert "internet-name" in q
    assert "links (consumed: $nug)" in q


def test_build_schema_extension_ddl():
    ddl = build_schema_extension_ddl(
        add_service_origin=True,
        relation_types=["sfp-accounts", "sfp-dnsbrute"],
    )
    assert ddl is not None
    assert "attribute service_origin" in ddl
    assert "osint-service owns service_origin" in ddl
    assert "relation sfp-accounts, sub osint-service" in ddl
    assert build_schema_extension_ddl(add_service_origin=False, relation_types=[]) is None
