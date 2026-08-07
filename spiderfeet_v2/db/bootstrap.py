"""Idempotent bootstrap for the spiderfeet-actual TypeDB database (R10-09 / AI3)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

from typedb.api.connection.driver import Driver

from spiderfeet.map.config import TypeDBConfigError, TypeDBConnectionConfig, load_connection_config
from spiderfeet.map.connection import open_driver, ping
from spiderfeet.map.typeql_util import literal_string, run_read_exists, run_schema, run_write
from spiderfeet_v2.db.constants import (
    ACTUAL_DATABASE_NAME,
    CLI_APP_SERVICES,
    SCHEMA_TQL,
    SEED_NUGGET_ENTITY,
    SEED_NUGGET_ID,
    SEED_NUGGET_INSTANCE,
)

logger = logging.getLogger(__name__)


@dataclass
class BootstrapReport:
    database: str
    created_database: bool = False
    reset: bool = False
    applied_schema: bool = False
    seed_nugget_inserted: bool = False
    services_inserted: int = 0
    services_skipped: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def ensure_database(driver: Driver, name: str) -> bool:
    if driver.databases.contains(name):
        return False
    driver.databases.create(name)
    return True


def reset_database(driver: Driver, name: str) -> None:
    if driver.databases.contains(name):
        driver.databases.get(name).delete()
    driver.databases.create(name)
    logger.info("Reset database %s", name)


def apply_schema(driver: Driver, database: str) -> None:
    if not SCHEMA_TQL.is_file():
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_TQL}")
    schema_text = SCHEMA_TQL.read_text(encoding="utf-8").strip()
    if not schema_text.endswith(";"):
        schema_text += ";"
    run_schema(driver, database, schema_text)


def schema_loaded(driver: Driver, database: str) -> bool:
    try:
        return "entity nugget" in driver.databases.get(database).type_schema()
    except Exception:
        return False


def seed_anchor_nugget(driver: Driver, database: str) -> bool:
    """Insert ROOT archetype so osint-service relations have a consumed player."""
    exists = run_read_exists(
        driver,
        database,
        f"match $e isa {SEED_NUGGET_ENTITY}, has nugget_id {literal_string(SEED_NUGGET_ID)};",
    )
    if exists:
        return False
    run_write(
        driver,
        database,
        f"""
        insert
          $e isa {SEED_NUGGET_ENTITY},
            has nugget_id {literal_string(SEED_NUGGET_ID)},
            has nugget_instance_id {literal_string(SEED_NUGGET_INSTANCE)},
            has nugget_type "ENTITY",
            has nugget_description "Seed anchor for CLI service relations";
        """,
    )
    return True


def service_exists(driver: Driver, database: str, module_id: str) -> bool:
    return run_read_exists(
        driver,
        database,
        f"match $s isa osint-service, has module_id {literal_string(module_id)};",
    )


def seed_cli_services(driver: Driver, database: str, report: BootstrapReport) -> None:
    for rel_type, module_id, name in CLI_APP_SERVICES:
        if service_exists(driver, database, module_id):
            report.services_skipped += 1
            continue
        query = (
            "match\n"
            f"  $n isa {SEED_NUGGET_ENTITY}, has nugget_id {literal_string(SEED_NUGGET_ID)};\n"
            "insert\n"
            f"  $s isa {rel_type},\n"
            f"    has module_id {literal_string(module_id)},\n"
            f"    has name {literal_string(name)},\n"
            f'    has summary {literal_string(name + " (v2 CLI module)")},\n'
            '    has service_state "in-test",\n'
            '    has service_origin "cli",\n'
            '    has fixture_category "positive";\n'
            "  $s links (consumed: $n);"
        )
        try:
            run_write(driver, database, query)
            report.services_inserted += 1
        except Exception as exc:  # noqa: BLE001
            report.errors.append(f"{module_id}: {exc}")


def count_cli_services(driver: Driver, database: str) -> int:
    from typedb.api.connection.transaction import TransactionType

    count = 0
    with driver.transaction(database, TransactionType.READ) as tx:
        for _, module_id, _ in CLI_APP_SERVICES:
            answer = tx.query(
                f"match $s isa osint-service, has module_id {literal_string(module_id)};"
            ).resolve()
            if hasattr(answer, "as_concept_rows"):
                for _ in answer.as_concept_rows():
                    count += 1
                    break
    return count


def bootstrap_actual(
    cfg: Optional[TypeDBConnectionConfig] = None,
    *,
    database: Optional[str] = None,
    reset: bool = False,
) -> BootstrapReport:
    """Load v2 schema into spiderfeet-actual (or override) and seed 8 CLI services."""
    cfg = cfg or load_connection_config()
    db_name = database or ACTUAL_DATABASE_NAME
    report = BootstrapReport(database=db_name, reset=reset)
    driver = open_driver(cfg)
    try:
        if reset:
            reset_database(driver, db_name)
            report.created_database = True
        else:
            report.created_database = ensure_database(driver, db_name)

        if reset or not schema_loaded(driver, db_name):
            apply_schema(driver, db_name)
            report.applied_schema = True

        report.seed_nugget_inserted = seed_anchor_nugget(driver, db_name)
        seed_cli_services(driver, db_name, report)
    except Exception as exc:  # noqa: BLE001
        report.errors.append(str(exc))
    finally:
        driver.close()
    return report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap spiderfeet-actual TypeDB database (SPEC-010 AI3 / R10-09)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to typedb.connection.json",
    )
    parser.add_argument(
        "--database",
        type=str,
        default=None,
        help=f"Database name (default: {ACTUAL_DATABASE_NAME})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate the database before bootstrap (DESTRUCTIVE)",
    )
    parser.add_argument(
        "--approve-g1",
        action="store_true",
        help="Required with --reset when database is spiderfeet-actual (operator G1 gate)",
    )
    parser.add_argument(
        "--ping-only",
        action="store_true",
        help="Only test TypeDB connectivity",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Check schema + 8 CLI services without mutating",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        cfg = load_connection_config(Path(args.config) if args.config else None)
    except TypeDBConfigError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.ping_only:
        ok = ping(cfg)
        print("ok" if ok else "unreachable")
        return 0 if ok else 1

    db_name = args.database or ACTUAL_DATABASE_NAME

    if args.verify_only:
        driver = open_driver(cfg)
        try:
            if not driver.databases.contains(db_name):
                print(json.dumps({"database": db_name, "exists": False, "services": 0}))
                return 1
            loaded = schema_loaded(driver, db_name)
            n = count_cli_services(driver, db_name)
            print(
                json.dumps(
                    {
                        "database": db_name,
                        "exists": True,
                        "schema_loaded": loaded,
                        "cli_services": n,
                        "expected": len(CLI_APP_SERVICES),
                    },
                    indent=2,
                )
            )
            return 0 if loaded and n == len(CLI_APP_SERVICES) else 1
        finally:
            driver.close()

    if db_name == ACTUAL_DATABASE_NAME and args.reset and not args.approve_g1:
        print(
            "REFUSING: --reset on spiderfeet-actual requires operator G1 approval "
            "(issue #1074). Use --database <scratch> for autonomous smoke, or "
            "re-run with --approve-g1 after an approval comment on the issue.",
            file=sys.stderr,
        )
        return 3

    report = bootstrap_actual(cfg, database=db_name, reset=args.reset)
    print(json.dumps(asdict(report), indent=2))
    if not report.ok:
        return 1

    # Post-bootstrap verify
    driver = open_driver(cfg)
    try:
        n = count_cli_services(driver, db_name)
    finally:
        driver.close()
    if n != len(CLI_APP_SERVICES):
        print(f"verify failed: expected {len(CLI_APP_SERVICES)} services, got {n}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
