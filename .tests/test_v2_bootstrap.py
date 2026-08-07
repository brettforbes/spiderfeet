"""AI3 / R10-09: spiderfeet_v2.db.bootstrap loads schema + 8 CLI services (scratch DB)."""

from __future__ import annotations

import pytest

from spiderfeet_v2.db.constants import CLI_APP_SERVICES

SMOKE_DB = "spiderfeet-ai3-smoke"


def test_cli_service_catalogue_has_eight() -> None:
    assert len(CLI_APP_SERVICES) == 8
    module_ids = {m for _, m, _ in CLI_APP_SERVICES}
    assert "sfp_cli_nmap" in module_ids
    assert "sfp_cli_nuclei" in module_ids


def test_bootstrap_scratch_db_round_trip() -> None:
    pytest.importorskip("typedb.driver")
    from spiderfeet.map.config import TypeDBConfigError, load_connection_config
    from spiderfeet.map.connection import open_driver, ping
    from spiderfeet_v2.db.bootstrap import bootstrap_actual, count_cli_services, schema_loaded

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    report = bootstrap_actual(cfg, database=SMOKE_DB, reset=True)
    assert report.ok, report.errors
    assert report.applied_schema
    assert report.services_inserted == 8

    # Idempotent second pass skips existing services
    report2 = bootstrap_actual(cfg, database=SMOKE_DB, reset=False)
    assert report2.ok, report2.errors
    assert report2.services_skipped == 8

    driver = open_driver(cfg)
    try:
        assert schema_loaded(driver, SMOKE_DB)
        assert count_cli_services(driver, SMOKE_DB) == 8
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
    finally:
        driver.close()


def test_refuse_reset_actual_without_override(capsys) -> None:
    from spiderfeet_v2.db.bootstrap import main

    rc = main(["--reset"])
    assert rc == 3
    err = capsys.readouterr().err
    assert "G1" in err or "spiderfeet-actual" in err
