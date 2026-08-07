"""AI1 / R10-07: scan_step.relates produced round-trips with nugget plays scan_step:produced."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCHEMA = REPO / ".seed" / "spiderfeet_v2_semantic.tql"
SMOKE_DB = "spiderfeet-ai1-smoke"


def test_schema_file_declares_scan_step_produced() -> None:
    src = SCHEMA.read_text(encoding="utf-8")
    scan_block = src.split("relation scan_step", 1)[1].split("relation workflow", 1)[0]
    assert "relates produced" in scan_block
    assert "plays scan_step:produced" in src


def test_produced_role_round_trip() -> None:
    pytest.importorskip("typedb.driver")
    from spiderfeet.map.config import TypeDBConfigError, load_connection_config
    from spiderfeet.map.connection import open_driver, ping
    from spiderfeet.map.typeql_util import run_read_exists, run_schema, run_write

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    driver = open_driver(cfg)
    try:
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
        driver.databases.create(SMOKE_DB)
        schema = SCHEMA.read_text(encoding="utf-8").strip()
        if not schema.endswith(";"):
            schema += ";"
        run_schema(driver, SMOKE_DB, schema)

        # TypeDB rejects multi-statement inserts; attach produced in the same insert
        # as scan_step so the relation is not orphan-GC'd at commit.
        run_write(
            driver,
            SMOKE_DB,
            """
            insert
              $n isa ipv4-address,
                has nugget_id "IPV4_ADDRESS",
                has nugget_instance_id "IPV4_ADDRESS--ai1-smoke",
                has nugget_data "203.0.113.10";
            """,
        )
        run_write(
            driver,
            SMOKE_DB,
            """
            match
              $n isa ipv4-address, has nugget_instance_id "IPV4_ADDRESS--ai1-smoke";
            insert
              $s isa scan_step, has scan_instance_id "scan_step--ai1-smoke";
              $s links (produced: $n);
            """,
        )
        assert run_read_exists(
            driver,
            SMOKE_DB,
            """
            match
              $s isa scan_step, has scan_instance_id "scan_step--ai1-smoke";
              $n isa ipv4-address, has nugget_instance_id "IPV4_ADDRESS--ai1-smoke";
              $s links (produced: $n);
            """,
        )
    finally:
        try:
            if driver.databases.contains(SMOKE_DB):
                driver.databases.get(SMOKE_DB).delete()
        finally:
            driver.close()
