"""Idempotent bootstrap for the spiderfeet-map TypeDB database (R2-03-01)."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from typedb.api.connection.driver import Driver

from spiderfeet.map.config import TypeDBConnectionConfig
from spiderfeet.map.connection import driver_session
from spiderfeet.map.constants import (
    ARCHETYPE_INSTANCE_PREFIX,
    MAP_DATABASE_NAME,
    NUGGETS_JSON,
    OSINT_SERVICES_JSON,
    SCHEMA_TQL,
)
from spiderfeet.map.fixture_categories import fixture_category_for_service
from spiderfeet.map.service_states import service_state_for_service
from spiderfeet.map.naming import entity_type_for_nugget_id, relation_type_for_module_id
from spiderfeet.map.typeql_util import (
    literal_string,
    run_read_exists,
    run_schema,
    run_write,
    run_writes,
)

logger = logging.getLogger(__name__)


@dataclass
class BootstrapReport:
    """Structured result for CLI / future init API."""

    database: str
    created_database: bool = False
    applied_schema: bool = False
    nuggets_inserted: int = 0
    nuggets_skipped: int = 0
    services_inserted: int = 0
    services_skipped: int = 0
    services_failed: int = 0
    links_added: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_json(path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_already_loaded(driver: Driver, database: str) -> bool:
    """Heuristic: map schema defines abstract entity nugget."""
    try:
        db = driver.databases.get(database)
        type_schema = db.type_schema()
        return "entity nugget" in type_schema
    except Exception:
        return False


def ensure_database(driver: Driver, name: str) -> bool:
    """Create database if missing; return True when created."""
    if driver.databases.contains(name):
        return False
    driver.databases.create(name)
    return True


def reset_database(driver: Driver, name: str) -> None:
    """Drop and recreate database (development bootstrap only)."""
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


def _archetype_instance_id(nugget_id: str) -> str:
    return f"{ARCHETYPE_INSTANCE_PREFIX}{nugget_id}"


def build_nugget_insert_query(row: Dict[str, Any]) -> str:
    nugget_id = row["nugget_id"]
    entity = entity_type_for_nugget_id(nugget_id)
    instance_id = _archetype_instance_id(nugget_id)
    attrs = [
        f"has nugget_id {literal_string(nugget_id)}",
        f"has nugget_instance_id {literal_string(instance_id)}",
        f"has nugget_description {literal_string(row.get('nugget_description', ''))}",
        f"has nugget_type {literal_string(row.get('nugget_type', ''))}",
        f"has nugget_icon {literal_string(row.get('nugget_icon', ''))}",
        f"has nugget_colour {literal_string(row.get('nugget_colour', ''))}",
    ]
    attr_block = ",\n    ".join(attrs)
    return (
        "match\n"
        f"  not {{ $e isa {entity}, has nugget_id {literal_string(nugget_id)}; }};\n"
        "insert\n"
        f"  $e isa {entity},\n    {attr_block};"
    )


def seed_nuggets(driver: Driver, database: str, report: BootstrapReport) -> None:
    rows = _load_json(NUGGETS_JSON)
    for row in rows:
        nugget_id = row.get("nugget_id", "")
        if nugget_exists(driver, database, nugget_id):
            report.nuggets_skipped += 1
            continue
        query = build_nugget_insert_query(row)
        try:
            run_write(driver, database, query)
            report.nuggets_inserted += 1
        except Exception as exc:
            report.errors.append(f"nugget {nugget_id}: {exc}")


def _json_list_has(attr: str, values: List[str]) -> Optional[str]:
    """Store list fields as JSON in a single string (TypeDB list attrs not available)."""
    filtered = [v for v in values if v]
    if not filtered:
        return None
    return f"has {attr} {literal_string(json.dumps(filtered, ensure_ascii=False))}"


def _service_attr_lines(svc: Dict[str, Any], module_id: str) -> List[str]:
    attrs: List[str] = [
        f"has module_id {literal_string(module_id)}",
        f"has name {literal_string(svc.get('name', ''))}",
        f"has summary {literal_string(svc.get('summary', ''))}",
        f'has service_state "{service_state_for_service(svc)}"',
    ]
    category = fixture_category_for_service(svc)
    attrs.append(f'has fixture_category {literal_string(category)}')
    for key in ("access_tier", "consumption_group", "route_seed_nugget"):
        val = svc.get(key)
        if val:
            attrs.append(f"has {key} {literal_string(str(val))}")
    for key in ("flags", "use_cases", "categories", "consumed_nuggets", "produced_nuggets"):
        line = _json_list_has(key, svc.get(key) or [])
        if line:
            attrs.append(line)
    return attrs


def _service_link_specs(svc: Dict[str, Any]) -> List[tuple[str, str]]:
    """(nugget_id, role) pairs; consumed first, then produced."""
    specs: List[tuple[str, str]] = []
    seen: set[str] = set()
    for nugget_id in svc.get("consumed_nuggets") or []:
        if nugget_id and nugget_id not in seen:
            specs.append((nugget_id, "consumed"))
            seen.add(nugget_id)
    for nugget_id in svc.get("produced_nuggets") or []:
        if nugget_id and nugget_id not in seen:
            specs.append((nugget_id, "produced"))
            seen.add(nugget_id)
    return specs


def build_service_insert_queries(svc: Dict[str, Any]) -> List[str]:
    """
    One TypeQL write query per insert (TypeDB rejects multi-statement insert blocks).

    The first query must attach at least one consumed/produced role player in the
    same insert as the service relation. Orphan relations (no role players) are
    removed automatically when the write transaction commits.
    """
    module_id = svc.get("module_id")
    if not module_id:
        return []
    rel_type = relation_type_for_module_id(module_id)
    attr_block = ",\n    ".join(_service_attr_lines(svc, module_id))
    link_specs = _service_link_specs(svc)
    if not link_specs:
        link_specs = [("ROOT", "consumed")]

    match_lines = [
        f"  not {{ $mod isa {rel_type}, has module_id {literal_string(module_id)}; }};",
    ]
    for idx, (nugget_id, _role) in enumerate(link_specs):
        entity = entity_type_for_nugget_id(nugget_id)
        match_lines.append(
            f"  $nug{idx} isa {entity}, has nugget_id {literal_string(nugget_id)};"
        )

    insert_lines = [f"  $mod isa {rel_type},\n    {attr_block};"]
    for idx, (_nugget_id, role) in enumerate(link_specs):
        insert_lines.append(f"  $mod links ({role}: $nug{idx});")

    queries = [
        "match\n"
        + "\n".join(match_lines)
        + "\ninsert\n"
        + "\n".join(insert_lines)
    ]

    ds = svc.get("data_source") or {}
    source_attrs: List[str] = []
    for key in ("website", "model", "description", "fav_icon", "logo"):
        val = ds.get(key)
        if val:
            source_attrs.append(f"has {key} {literal_string(str(val))}")
    for key in ("references", "api_key_instructions"):
        line = _json_list_has(key, ds.get(key) or [])
        if line:
            source_attrs.append(line)
    if source_attrs:
        src_attrs = ",\n      ".join(source_attrs)
        queries.append(
            "match\n"
            f"  $mod isa {rel_type}, has module_id {literal_string(module_id)};\n"
            "insert\n"
            f"  $src isa osint-source,\n      {src_attrs};\n"
            "  (service: $mod, source: $src) isa data-source;"
        )

    for idx, opt in enumerate(svc.get("module_opts") or []):
        opt_name = opt.get("name") or opt.get("opt_name")
        if not opt_name:
            continue
        opt_attrs = [f"has opt_name {literal_string(opt_name)}"]
        desc = opt.get("description")
        if desc:
            opt_attrs.append(f"has description {literal_string(str(desc))}")
        vt = opt.get("value_type", "string")
        val = opt.get("value")
        if vt == "integer" and val not in (None, ""):
            opt_attrs.append(f"has in_value {int(val)}")
        elif vt == "double" and val not in (None, ""):
            opt_attrs.append(f"has db_value {float(val)}")
        elif vt == "boolean" and val not in (None, ""):
            opt_attrs.append(f"has bo_value {'true' if val else 'false'}")
        elif val not in (None, ""):
            opt_attrs.append(f"has st_value {literal_string(str(val))}")
        oa = ",\n      ".join(opt_attrs)
        var = f"$opt{idx}"
        queries.append(
            "match\n"
            f"  $mod isa {rel_type}, has module_id {literal_string(module_id)};\n"
            "insert\n"
            f"  {var} isa module-opt,\n      {oa};\n"
            f"  (service: $mod, opt: {var}) isa opts;"
        )
    return queries


def nugget_exists(driver: Driver, database: str, nugget_id: str) -> bool:
    entity = entity_type_for_nugget_id(nugget_id)
    return run_read_exists(
        driver,
        database,
        f"match $e isa {entity}, has nugget_id {literal_string(nugget_id)};",
    )


def service_exists(driver: Driver, database: str, module_id: str) -> bool:
    rel_type = relation_type_for_module_id(module_id)
    return run_read_exists(
        driver,
        database,
        f"match $s isa {rel_type}, has module_id {literal_string(module_id)};",
    )


def role_link_exists(
    driver: Driver,
    database: str,
    module_id: str,
    nugget_id: str,
    role: str,
) -> bool:
    rel_type = relation_type_for_module_id(module_id)
    entity = entity_type_for_nugget_id(nugget_id)
    return run_read_exists(
        driver,
        database,
        "match\n"
        f"  $mod isa {rel_type}, has module_id {literal_string(module_id)};\n"
        f"  $nug isa {entity}, has nugget_id {literal_string(nugget_id)};\n"
        f"  $mod links ({role}: $nug);",
    )


def build_role_link_query(
    module_id: str,
    nugget_id: str,
    role: str,
) -> str:
    rel_type = relation_type_for_module_id(module_id)
    entity = entity_type_for_nugget_id(nugget_id)
    return (
        "match\n"
        f"  $mod isa {rel_type}, has module_id {literal_string(module_id)};\n"
        f"  $nug isa {entity}, has nugget_id {literal_string(nugget_id)};\n"
        f"  not {{ $mod links ({role}: $nug); }};\n"
        "insert\n"
        f"  $mod links ({role}: $nug);"
    )


def seed_services(driver: Driver, database: str, report: BootstrapReport) -> None:
    services = _load_json(OSINT_SERVICES_JSON)
    for svc in services:
        module_id = svc.get("module_id", "")
        if not module_id:
            report.services_failed += 1
            continue
        if not service_exists(driver, database, module_id):
            queries = build_service_insert_queries(svc)
            if not queries:
                report.services_failed += 1
                continue
            try:
                run_writes(driver, database, queries)
                report.services_inserted += 1
                report.links_added += len(_service_link_specs(svc))
            except Exception as exc:
                report.services_failed += 1
                report.errors.append(f"service {module_id}: {exc}")
                continue
        else:
            report.services_skipped += 1

        for nugget_id in svc.get("consumed_nuggets") or []:
            _link_role(driver, database, report, module_id, nugget_id, "consumed")
        for nugget_id in svc.get("produced_nuggets") or []:
            _link_role(driver, database, report, module_id, nugget_id, "produced")


def _link_role(
    driver: Driver,
    database: str,
    report: BootstrapReport,
    module_id: str,
    nugget_id: str,
    role: str,
) -> None:
    query = build_role_link_query(module_id, nugget_id, role)
    if role_link_exists(driver, database, module_id, nugget_id, role):
        return
    try:
        run_write(driver, database, query)
        report.links_added += 1
    except Exception as exc:
        report.errors.append(f"link {module_id} {role} {nugget_id}: {exc}")


def bootstrap_map(
    cfg: Optional[TypeDBConnectionConfig] = None,
    *,
    database: Optional[str] = None,
    reset: bool = False,
) -> BootstrapReport:
    """
    Idempotent bootstrap: database, schema, archetype nuggets, OSINT services.

    Uses typedb-driver directly (type-bridge deferred until Python 3.13+).
    """
    if cfg is None:
        from spiderfeet.map.config import load_connection_config

        cfg = load_connection_config()

    db_name = database or cfg.database or MAP_DATABASE_NAME
    report = BootstrapReport(database=db_name)

    with driver_session(cfg) as driver:
        if reset:
            reset_database(driver, db_name)
            report.created_database = True
        else:
            report.created_database = ensure_database(driver, db_name)
        if not schema_already_loaded(driver, db_name):
            apply_schema(driver, db_name)
            report.applied_schema = True
        seed_nuggets(driver, db_name, report)
        seed_services(driver, db_name, report)

    return report


def bootstrap_map_from_config_path(path) -> BootstrapReport:
    from spiderfeet.map.config import load_connection_config

    return bootstrap_map(load_connection_config(path))
