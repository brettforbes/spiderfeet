"""CRUD for project / workflow / target / scan_step / subgraph subtypes ↔ JSON (R10-17 / AL1)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map.typeql_util import literal_string, run_read_exists, run_write, run_writes
from spiderfeet_v2.db.config import TypeDBConnectionConfig, load_connection_config
from spiderfeet_v2.db.connection import open_driver
from spiderfeet_v2.db.subgraph_codec import (
    SubgraphCodecError,
    load_dual_form,
    load_graph_from_typedb,
    read_json_string,
    store_dual_form,
)

# --- Attribute inventories (schema keys ↔ JSON fields) ---

TARGET_ATTRS = (
    "target_value",
    "target_description",
    "target_created",
    "target_yaml",
)

WORKFLOW_ATTRS = (
    "name",
    "description",
    "author",
    "created",
    "workflow_yaml",
)

PROJECT_ATTRS = (
    "stix_incident_id",
    "project_name",
    "project_description",
    "project_created",
)

SCAN_STEP_ATTRS = (
    "step_module_id",
    "scan_status",
    "scan_nugget_count",
    "scan_results_by_type",
    "scan_results",
    "scan_duration",
    "scan_timestamp",
    "scan_notes",
    "scan_ui_cli_command",
    "scan_ui_text_form",
    "scan_ui_structured_form",
    "scan_ui_structured_form_type",
    "scan_ui_graph_form",
    "scan_ui_markdown_narrative_form",
    "scan_yaml",
)

DATETIME_ATTRS = frozenset(
    {"created", "project_created", "target_created", "scan_timestamp"}
)
INT_ATTRS = frozenset({"scan_nugget_count"})
DOUBLE_ATTRS = frozenset({"scan_duration"})

SUBGRAPH_KINDS = (
    "scan_result_graph",
    "project_context",
    "temporary_subgraph",
)

_SUBGRAPH_META = {
    "scan_result_graph": {
        "id_attr": "scan_result_id",
        "owner_type": "scan_step",
        "owner_id_attr": "scan_instance_id",
        "owner_role": "scan_step",
        "json_owner_key": "scan_instance_id",
    },
    "project_context": {
        "id_attr": "project_context_id",
        "owner_type": "project",
        "owner_id_attr": "project_id",
        "owner_role": "project",
        "json_owner_key": "project_id",
    },
    "temporary_subgraph": {
        "id_attr": "temporary_subgraph_id",
        "owner_type": "project",
        "owner_id_attr": "project_id",
        "owner_role": "project",
        "json_owner_key": "project_id",
    },
}


class CrudError(Exception):
    """CRUD validation or persistence failure."""


def _iso_datetime(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
    text = str(value).strip()
    return text or None


def _typedb_datetime_literal(value: Any) -> str:
    """Format a datetime for TypeQL (no surrounding quotes)."""
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    # TypeDB 3 accepts datetime literals like 2024-06-01T12:00:00
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def _attr_literal(attr: str, value: Any) -> str:
    if value is None:
        raise CrudError(f"attribute {attr} cannot be null in a has clause")
    if attr in DATETIME_ATTRS:
        return _typedb_datetime_literal(value)
    if attr in INT_ATTRS:
        return str(int(value))
    if attr in DOUBLE_ATTRS:
        return str(float(value))
    if isinstance(value, (dict, list)):
        return literal_string(json.dumps(value, separators=(",", ":")))
    return literal_string(str(value))


def _normalize_value(attr: str, raw: Any) -> Any:
    if raw is None:
        return None
    if attr in DATETIME_ATTRS:
        return _iso_datetime(raw)
    if attr in INT_ATTRS:
        return int(raw)
    if attr in DOUBLE_ATTRS:
        return float(raw)
    if isinstance(raw, bool):
        return raw
    return str(raw)


def _collect_strings(driver: Driver, database: str, query: str, column: str = "v") -> List[str]:
    out: List[str] = []
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_rows"):
            return out
        for row in answer.as_concept_rows():
            concept = row.get(column)
            if concept is None:
                continue
            value = concept.try_get_value()
            if value is not None:
                out.append(str(value))
    return out


def _read_attrs(
    driver: Driver,
    database: str,
    type_label: str,
    id_attr: str,
    id_value: str,
    attrs: Sequence[str],
) -> Dict[str, Any]:
    """Read optional attributes one-by-one (avoids missing-attr row collapse)."""
    result: Dict[str, Any] = {id_attr: id_value}
    for attr in attrs:
        query = (
            f"match $x isa {type_label}, has {id_attr} {literal_string(id_value)}, "
            f"has {attr} $v;"
        )
        values = _collect_strings(driver, database, query)
        if not values:
            result[attr] = None
            continue
        raw = values[0]
        # Re-fetch typed value for int/double/datetime
        with driver.transaction(database, TransactionType.READ) as tx:
            answer = tx.query(query).resolve()
            typed: Any = raw
            for row in answer.as_concept_rows():
                concept = row.get("v")
                if concept is not None:
                    typed = concept.try_get_value()
                break
        result[attr] = _normalize_value(attr, typed)
    return result


def _has_clauses(data: Dict[str, Any], attrs: Sequence[str]) -> List[str]:
    clauses: List[str] = []
    for attr in attrs:
        if attr not in data or data[attr] is None:
            continue
        clauses.append(f"has {attr} {_attr_literal(attr, data[attr])}")
    return clauses


def _clear_attribute(
    driver: Driver,
    database: str,
    type_label: str,
    id_attr: str,
    id_value: str,
    attr: str,
) -> None:
    has_it = run_read_exists(
        driver,
        database,
        f"match $x isa {type_label}, has {id_attr} {literal_string(id_value)}, "
        f"has {attr} $v;",
    )
    if not has_it:
        return
    run_write(
        driver,
        database,
        f"""
        match
          $x isa {type_label}, has {id_attr} {literal_string(id_value)}, has {attr} $old;
        delete
          has $old of $x;
        """,
    )


def _set_attributes(
    driver: Driver,
    database: str,
    type_label: str,
    id_attr: str,
    id_value: str,
    data: Dict[str, Any],
    attrs: Sequence[str],
) -> None:
    """Replace provided attributes (skip keys absent from data)."""
    for attr in attrs:
        if attr not in data:
            continue
        value = data[attr]
        _clear_attribute(driver, database, type_label, id_attr, id_value, attr)
        if value is None:
            continue
        run_write(
            driver,
            database,
            f"""
            match
              $x isa {type_label}, has {id_attr} {literal_string(id_value)};
            insert
              $x has {attr} {_attr_literal(attr, value)};
            """,
        )


@dataclass
class CrudStore:
    """TypeDB-backed CRUD store for SpiderFeet v2 engine objects."""

    cfg: TypeDBConnectionConfig
    database: str

    @classmethod
    def connect(
        cls,
        cfg: Optional[TypeDBConnectionConfig] = None,
        *,
        database: Optional[str] = None,
    ) -> "CrudStore":
        cfg = cfg or load_connection_config()
        return cls(cfg=cfg, database=database or cfg.database)

    def _driver(self) -> Driver:
        return open_driver(self.cfg)

    # ------------------------------------------------------------------ target

    def create_target(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tid = data.get("target_id")
        if not tid:
            raise CrudError("target_id is required")
        driver = self._driver()
        try:
            if self.get_target(tid, _driver=driver) is not None:
                raise CrudError(f"target already exists: {tid}")
            has_parts = [f"has target_id {literal_string(tid)}"] + _has_clauses(
                data, TARGET_ATTRS
            )
            run_write(
                driver,
                self.database,
                "insert\n  $t isa target,\n    " + ",\n    ".join(has_parts) + ";\n",
            )
            return self.get_target(tid, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def get_target(
        self, target_id: str, *, _driver: Optional[Driver] = None
    ) -> Optional[Dict[str, Any]]:
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $t isa target, has target_id {literal_string(target_id)};",
            )
            if not exists:
                return None
            return _read_attrs(
                driver, self.database, "target", "target_id", target_id, TARGET_ATTRS
            )
        finally:
            if own:
                driver.close()

    def update_target(self, target_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        driver = self._driver()
        try:
            if self.get_target(target_id, _driver=driver) is None:
                raise CrudError(f"target not found: {target_id}")
            _set_attributes(
                driver, self.database, "target", "target_id", target_id, data, TARGET_ATTRS
            )
            return self.get_target(target_id, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def delete_target(self, target_id: str) -> bool:
        driver = self._driver()
        try:
            if self.get_target(target_id, _driver=driver) is None:
                return False
            run_write(
                driver,
                self.database,
                f"""
                match $t isa target, has target_id {literal_string(target_id)};
                delete $t;
                """,
            )
            return True
        finally:
            driver.close()

    def list_targets(self) -> List[Dict[str, Any]]:
        driver = self._driver()
        try:
            ids = _collect_strings(
                driver,
                self.database,
                "match $t isa target, has target_id $v;",
            )
            return [self.get_target(i, _driver=driver) for i in sorted(ids)]  # type: ignore[misc]
        finally:
            driver.close()

    # ---------------------------------------------------------------- workflow

    def create_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        wid = data.get("workflow_id")
        if not wid:
            raise CrudError("workflow_id is required")
        # TypeDB 3 does not persist playerless relation instances.
        # A linked project alone is a valid player (info-only workflow).
        has_players = bool(
            data.get("project_id")
            or data.get("target_id")
            or data.get("first_step_id")
            or data.get("prior_step_ids")
            or data.get("next_step_ids")
        )
        if not has_players:
            raise CrudError(
                "workflow create requires at least one of project_id, target_id, "
                "first_step_id, prior_step_ids, next_step_ids"
            )
        driver = self._driver()
        try:
            if self.get_workflow(wid, _driver=driver) is not None:
                raise CrudError(f"workflow already exists: {wid}")
            has_parts = [f"has workflow_id {literal_string(wid)}"] + _has_clauses(
                data, WORKFLOW_ATTRS
            )
            match_lines: List[str] = []
            insert_links: List[str] = []
            pid = data.get("project_id")
            if pid:
                match_lines.append(
                    f"$p isa project, has project_id {literal_string(pid)};"
                )
                insert_links.append("$w links (project: $p);")
            tid = data.get("target_id")
            if tid:
                match_lines.append(
                    f"$t isa target, has target_id {literal_string(tid)};"
                )
                insert_links.append("$w links (target: $t);")
            first = data.get("first_step_id")
            if first:
                match_lines.append(
                    f"$fs isa scan_step, has scan_instance_id {literal_string(first)};"
                )
                insert_links.append("$w links (first_step: $fs);")
            for i, sid in enumerate(data.get("prior_step_ids") or []):
                var = f"$ps{i}"
                match_lines.append(
                    f"{var} isa scan_step, has scan_instance_id {literal_string(sid)};"
                )
                insert_links.append(f"$w links (prior_step: {var});")
            for i, sid in enumerate(data.get("next_step_ids") or []):
                var = f"$ns{i}"
                match_lines.append(
                    f"{var} isa scan_step, has scan_instance_id {literal_string(sid)};"
                )
                insert_links.append(f"$w links (next_step: {var});")
            query = (
                "match\n  "
                + "\n  ".join(match_lines)
                + "\ninsert\n  $w isa workflow,\n    "
                + ",\n    ".join(has_parts)
                + ";\n  "
                + "\n  ".join(insert_links)
                + "\n"
            )
            run_write(driver, self.database, query)
            return self.get_workflow(wid, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def _link_workflow(self, driver: Driver, wid: str, data: Dict[str, Any]) -> None:
        queries: List[str] = []
        pid = data.get("project_id")
        if pid:
            queries.append(
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $p isa project, has project_id {literal_string(pid)};
                insert
                  $w links (project: $p);
                """
            )
        tid = data.get("target_id")
        if tid:
            queries.append(
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $t isa target, has target_id {literal_string(tid)};
                insert
                  $w links (target: $t);
                """
            )
        first = data.get("first_step_id")
        if first:
            queries.append(
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $s isa scan_step, has scan_instance_id {literal_string(first)};
                insert
                  $w links (first_step: $s);
                """
            )
        for role, key in (("prior_step", "prior_step_ids"), ("next_step", "next_step_ids")):
            for sid in data.get(key) or []:
                queries.append(
                    f"""
                    match
                      $w isa workflow, has workflow_id {literal_string(wid)};
                      $s isa scan_step, has scan_instance_id {literal_string(sid)};
                    insert
                      $w links ({role}: $s);
                    """
                )
        if queries:
            run_writes(driver, self.database, queries)

    def _clear_workflow_links(self, driver: Driver, wid: str) -> None:
        for role in ("project", "target", "first_step", "prior_step", "next_step"):
            exists = run_read_exists(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $w links ({role}: $p);
                """,
            )
            if not exists:
                continue
            run_write(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $w links ({role}: $p);
                delete
                  links ({role}: $p) of $w;
                """,
            )

    def get_workflow(
        self, workflow_id: str, *, _driver: Optional[Driver] = None
    ) -> Optional[Dict[str, Any]]:
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $w isa workflow, has workflow_id {literal_string(workflow_id)};",
            )
            if not exists:
                return None
            row = _read_attrs(
                driver,
                self.database,
                "workflow",
                "workflow_id",
                workflow_id,
                WORKFLOW_ATTRS,
            )
            projects = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(workflow_id)};
                  $w links (project: $p);
                  $p has project_id $v;
                """,
            )
            targets = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(workflow_id)};
                  $w links (target: $t);
                  $t has target_id $v;
                """,
            )
            first = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(workflow_id)};
                  $w links (first_step: $s);
                  $s has scan_instance_id $v;
                """,
            )
            prior = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(workflow_id)};
                  $w links (prior_step: $s);
                  $s has scan_instance_id $v;
                """,
            )
            nxt = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(workflow_id)};
                  $w links (next_step: $s);
                  $s has scan_instance_id $v;
                """,
            )
            row["project_id"] = projects[0] if projects else None
            row["target_id"] = targets[0] if targets else None
            row["first_step_id"] = first[0] if first else None
            row["prior_step_ids"] = sorted(prior)
            row["next_step_ids"] = sorted(nxt)
            return row
        finally:
            if own:
                driver.close()

    def update_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        link_keys = {
            "project_id",
            "target_id",
            "first_step_id",
            "prior_step_ids",
            "next_step_ids",
        }
        current = self.get_workflow(workflow_id)
        if current is None:
            raise CrudError(f"workflow not found: {workflow_id}")
        if link_keys & set(data):
            # Unlinking the last role player drops the relation; recreate instead.
            merged = {**current, **data, "workflow_id": workflow_id}
            self.delete_workflow(workflow_id)
            return self.create_workflow(merged)
        driver = self._driver()
        try:
            _set_attributes(
                driver,
                self.database,
                "workflow",
                "workflow_id",
                workflow_id,
                data,
                WORKFLOW_ATTRS,
            )
            return self.get_workflow(workflow_id, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def delete_workflow(self, workflow_id: str) -> bool:
        driver = self._driver()
        try:
            if self.get_workflow(workflow_id, _driver=driver) is None:
                return False
            run_write(
                driver,
                self.database,
                f"""
                match $w isa workflow, has workflow_id {literal_string(workflow_id)};
                delete $w;
                """,
            )
            return True
        finally:
            driver.close()

    def list_workflows(self) -> List[Dict[str, Any]]:
        driver = self._driver()
        try:
            ids = _collect_strings(
                driver,
                self.database,
                "match $w isa workflow, has workflow_id $v;",
            )
            return [self.get_workflow(i, _driver=driver) for i in sorted(ids)]  # type: ignore[misc]
        finally:
            driver.close()

    # ----------------------------------------------------------------- project

    def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a project **entity** (standalone OK) and optionally link workflows.

        Direction: each workflow relation ``links (project: $p)``. Project entities
        need no role players, so ``workflow_ids`` may be empty.
        """
        pid = data.get("project_id")
        if not pid:
            raise CrudError("project_id is required")
        payload = dict(data)
        # Soft alias: older callers used bare ``created``.
        if "project_created" not in payload and payload.get("created") is not None:
            payload["project_created"] = payload["created"]
        workflow_ids = list(payload.get("workflow_ids") or [])
        driver = self._driver()
        try:
            if self.get_project(pid, _driver=driver) is not None:
                raise CrudError(f"project already exists: {pid}")
            has_parts = [f"has project_id {literal_string(pid)}"] + _has_clauses(
                payload, PROJECT_ATTRS
            )
            query = (
                "insert\n  $p isa project,\n    "
                + ",\n    ".join(has_parts)
                + ";\n"
            )
            run_write(driver, self.database, query)
            if workflow_ids:
                self._set_project_workflows(driver, pid, workflow_ids)
            return self.get_project(pid, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def get_project(
        self, project_id: str, *, _driver: Optional[Driver] = None
    ) -> Optional[Dict[str, Any]]:
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $p isa project, has project_id {literal_string(project_id)};",
            )
            if not exists:
                return None
            row = _read_attrs(
                driver, self.database, "project", "project_id", project_id, PROJECT_ATTRS
            )
            wids = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $p isa project, has project_id {literal_string(project_id)};
                  $w isa workflow, links (project: $p);
                  $w has workflow_id $v;
                """,
            )
            row["workflow_ids"] = sorted(wids)
            return row
        finally:
            if own:
                driver.close()

    def _set_project_workflows(
        self, driver: Driver, project_id: str, workflow_ids: Sequence[str]
    ) -> None:
        """Replace which workflows link this project (workflow → project direction)."""
        current = _collect_strings(
            driver,
            self.database,
            f"""
            match
              $p isa project, has project_id {literal_string(project_id)};
              $w isa workflow, links (project: $p);
              $w has workflow_id $v;
            """,
        )
        desired = set(workflow_ids)
        for wid in current:
            if wid in desired:
                continue
            run_write(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $p isa project, has project_id {literal_string(project_id)};
                  $w links (project: $p);
                delete
                  links (project: $p) of $w;
                """,
            )
        for wid in workflow_ids:
            if wid in current:
                continue
            exists = run_read_exists(
                driver,
                self.database,
                f"match $w isa workflow, has workflow_id {literal_string(wid)};",
            )
            if not exists:
                raise CrudError(f"workflow not found: {wid}")
            run_write(
                driver,
                self.database,
                f"""
                match
                  $w isa workflow, has workflow_id {literal_string(wid)};
                  $p isa project, has project_id {literal_string(project_id)};
                insert
                  $w links (project: $p);
                """,
            )

    def update_project(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_project(project_id)
        if current is None:
            raise CrudError(f"project not found: {project_id}")
        payload = dict(data)
        if "project_created" not in payload and payload.get("created") is not None:
            payload["project_created"] = payload["created"]
        driver = self._driver()
        try:
            attr_patch = {k: v for k, v in payload.items() if k in PROJECT_ATTRS}
            if attr_patch:
                _set_attributes(
                    driver,
                    self.database,
                    "project",
                    "project_id",
                    project_id,
                    attr_patch,
                    PROJECT_ATTRS,
                )
            if "workflow_ids" in payload:
                self._set_project_workflows(
                    driver, project_id, list(payload.get("workflow_ids") or [])
                )
            return self.get_project(project_id, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def delete_project(self, project_id: str) -> bool:
        driver = self._driver()
        try:
            if self.get_project(project_id, _driver=driver) is None:
                return False
            run_write(
                driver,
                self.database,
                f"""
                match $p isa project, has project_id {literal_string(project_id)};
                delete $p;
                """,
            )
            return True
        finally:
            driver.close()

    def list_projects(self) -> List[Dict[str, Any]]:
        driver = self._driver()
        try:
            ids = _collect_strings(
                driver,
                self.database,
                "match $p isa project, has project_id $v;",
            )
            return [self.get_project(i, _driver=driver) for i in sorted(ids)]  # type: ignore[misc]
        finally:
            driver.close()

    # --------------------------------------------------------------- scan_step

    def create_scan_step(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sid = data.get("scan_instance_id")
        if not sid:
            raise CrudError("scan_instance_id is required")
        consumed = list(data.get("consumed_ids") or [])
        produced = list(data.get("produced_ids") or [])
        module_id = data.get("service_module_id")
        if not (consumed or produced or module_id):
            raise CrudError(
                "scan_step create requires service_module_id and/or "
                "consumed_ids/produced_ids (TypeDB 3 cannot persist playerless relations)"
            )
        driver = self._driver()
        try:
            if self.get_scan_step(sid, _driver=driver) is not None:
                raise CrudError(f"scan_step already exists: {sid}")
            has_parts = [f"has scan_instance_id {literal_string(sid)}"] + _has_clauses(
                data, SCAN_STEP_ATTRS
            )
            match_lines: List[str] = []
            insert_links: List[str] = []
            for i, nid in enumerate(consumed):
                var = f"$c{i}"
                match_lines.append(
                    f"{var} isa nugget, has nugget_instance_id {literal_string(nid)};"
                )
                insert_links.append(f"$s links (consumed: {var});")
            for i, nid in enumerate(produced):
                var = f"$p{i}"
                match_lines.append(
                    f"{var} isa nugget, has nugget_instance_id {literal_string(nid)};"
                )
                insert_links.append(f"$s links (produced: {var});")
            if module_id:
                match_lines.append(
                    f"$svc isa osint-service, has module_id {literal_string(module_id)};"
                )
                insert_links.append("$s links (service: $svc);")
            query = (
                "match\n  "
                + "\n  ".join(match_lines)
                + "\ninsert\n  $s isa scan_step,\n    "
                + ",\n    ".join(has_parts)
                + ";\n  "
                + "\n  ".join(insert_links)
                + "\n"
            )
            run_write(driver, self.database, query)
            return self.get_scan_step(sid, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def _link_scan_step(self, driver: Driver, sid: str, data: Dict[str, Any]) -> None:
        queries: List[str] = []
        for role, key in (("consumed", "consumed_ids"), ("produced", "produced_ids")):
            for nid in data.get(key) or []:
                queries.append(
                    f"""
                    match
                      $s isa scan_step, has scan_instance_id {literal_string(sid)};
                      $n isa nugget, has nugget_instance_id {literal_string(nid)};
                    insert
                      $s links ({role}: $n);
                    """
                )
        module_id = data.get("service_module_id")
        if module_id:
            queries.append(
                f"""
                match
                  $s isa scan_step, has scan_instance_id {literal_string(sid)};
                  $svc isa osint-service, has module_id {literal_string(module_id)};
                insert
                  $s links (service: $svc);
                """
            )
        if queries:
            run_writes(driver, self.database, queries)

    def _clear_scan_step_links(self, driver: Driver, sid: str) -> None:
        for role in ("consumed", "produced", "service"):
            exists = run_read_exists(
                driver,
                self.database,
                f"""
                match
                  $s isa scan_step, has scan_instance_id {literal_string(sid)};
                  $s links ({role}: $p);
                """,
            )
            if not exists:
                continue
            run_write(
                driver,
                self.database,
                f"""
                match
                  $s isa scan_step, has scan_instance_id {literal_string(sid)};
                  $s links ({role}: $p);
                delete
                  links ({role}: $p) of $s;
                """,
            )

    def get_scan_step(
        self, scan_instance_id: str, *, _driver: Optional[Driver] = None
    ) -> Optional[Dict[str, Any]]:
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};",
            )
            if not exists:
                return None
            row = _read_attrs(
                driver,
                self.database,
                "scan_step",
                "scan_instance_id",
                scan_instance_id,
                SCAN_STEP_ATTRS,
            )
            row["consumed_ids"] = sorted(
                _collect_strings(
                    driver,
                    self.database,
                    f"""
                    match
                      $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};
                      $s links (consumed: $n);
                      $n has nugget_instance_id $v;
                    """,
                )
            )
            row["produced_ids"] = sorted(
                _collect_strings(
                    driver,
                    self.database,
                    f"""
                    match
                      $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};
                      $s links (produced: $n);
                      $n has nugget_instance_id $v;
                    """,
                )
            )
            svc = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};
                  $s links (service: $svc);
                  $svc has module_id $v;
                """,
            )
            row["service_module_id"] = svc[0] if svc else None
            return row
        finally:
            if own:
                driver.close()

    def get_scan_status(
        self, scan_instance_id: str, *, _driver: Optional[Driver] = None
    ) -> Optional[str]:
        """Thin read of ``scan_status`` only (SPEC-015 R15-02 — no four-form attrs)."""
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};",
            )
            if not exists:
                return None
            row = _read_attrs(
                driver,
                self.database,
                "scan_step",
                "scan_instance_id",
                scan_instance_id,
                ("scan_status",),
            )
            status = row.get("scan_status")
            return str(status) if status is not None else None
        finally:
            if own:
                driver.close()

    def update_scan_step(
        self, scan_instance_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        link_keys = {"consumed_ids", "produced_ids", "service_module_id"}
        current = self.get_scan_step(scan_instance_id)
        if current is None:
            raise CrudError(f"scan_step not found: {scan_instance_id}")
        if link_keys & set(data):
            merged = {**current, **data, "scan_instance_id": scan_instance_id}
            self.delete_scan_step(scan_instance_id)
            return self.create_scan_step(merged)
        driver = self._driver()
        try:
            _set_attributes(
                driver,
                self.database,
                "scan_step",
                "scan_instance_id",
                scan_instance_id,
                data,
                SCAN_STEP_ATTRS,
            )
            return self.get_scan_step(scan_instance_id, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def delete_scan_step(self, scan_instance_id: str) -> bool:
        driver = self._driver()
        try:
            if self.get_scan_step(scan_instance_id, _driver=driver) is None:
                return False
            run_write(
                driver,
                self.database,
                f"""
                match $s isa scan_step, has scan_instance_id {literal_string(scan_instance_id)};
                delete $s;
                """,
            )
            return True
        finally:
            driver.close()

    def list_scan_steps(self) -> List[Dict[str, Any]]:
        driver = self._driver()
        try:
            ids = _collect_strings(
                driver,
                self.database,
                "match $s isa scan_step, has scan_instance_id $v;",
            )
            return [self.get_scan_step(i, _driver=driver) for i in sorted(ids)]  # type: ignore[misc]
        finally:
            driver.close()

    # --------------------------------------------------------------- subgraphs

    def create_subgraph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        kind = data.get("kind")
        if kind not in _SUBGRAPH_META:
            raise CrudError(
                f"kind must be one of {list(_SUBGRAPH_META)}; got {kind!r}"
            )
        meta = _SUBGRAPH_META[kind]
        id_attr = meta["id_attr"]
        sg_id = data.get(id_attr)
        owner_id = data.get(meta["json_owner_key"])
        if not sg_id:
            raise CrudError(f"{id_attr} is required")
        if not owner_id:
            raise CrudError(f"{meta['json_owner_key']} is required")
        driver = self._driver()
        try:
            if self.get_subgraph(kind, sg_id, _driver=driver) is not None:
                raise CrudError(f"{kind} already exists: {sg_id}")
            run_write(
                driver,
                self.database,
                f"""
                match
                  $owner isa {meta["owner_type"]},
                    has {meta["owner_id_attr"]} {literal_string(owner_id)};
                insert
                  $g isa {kind}, has {id_attr} {literal_string(sg_id)};
                  $g links ({meta["owner_role"]}: $owner);
                """,
            )
            graph = data.get("graph")
            if graph is None and ("nodes" in data or "edges" in data):
                graph = {
                    "nodes": data.get("nodes") or [],
                    "edges": data.get("edges") or [],
                }
            if graph is not None:
                try:
                    store_dual_form(driver, self.database, kind, sg_id, graph)
                except SubgraphCodecError as exc:
                    raise CrudError(str(exc)) from exc
                return self.get_subgraph_dual(kind, sg_id, _driver=driver)
            return self.get_subgraph(kind, sg_id, _driver=driver)  # type: ignore[return-value]
        finally:
            driver.close()

    def get_subgraph(
        self,
        kind: str,
        subgraph_id: str,
        *,
        _driver: Optional[Driver] = None,
    ) -> Optional[Dict[str, Any]]:
        if kind not in _SUBGRAPH_META:
            raise CrudError(f"unknown subgraph kind: {kind}")
        meta = _SUBGRAPH_META[kind]
        id_attr = meta["id_attr"]
        own = _driver is None
        driver = _driver or self._driver()
        try:
            exists = run_read_exists(
                driver,
                self.database,
                f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};",
            )
            if not exists:
                return None
            owners = _collect_strings(
                driver,
                self.database,
                f"""
                match
                  $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
                  $g links ({meta["owner_role"]}: $owner);
                  $owner has {meta["owner_id_attr"]} $v;
                """,
            )
            row: Dict[str, Any] = {
                "kind": kind,
                id_attr: subgraph_id,
                meta["json_owner_key"]: owners[0] if owners else None,
            }
            js = read_json_string(driver, self.database, kind, subgraph_id)
            row["json_string"] = js
            return row
        finally:
            if own:
                driver.close()

    def update_subgraph(
        self, kind: str, subgraph_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Re-point owner and/or replace dual-form graph payload (AL1 + AL2)."""
        if kind not in _SUBGRAPH_META:
            raise CrudError(f"unknown subgraph kind: {kind}")
        meta = _SUBGRAPH_META[kind]
        owner_key = meta["json_owner_key"]
        current = self.get_subgraph(kind, subgraph_id)
        if current is None:
            raise CrudError(f"{kind} not found: {subgraph_id}")

        graph = data.get("graph")
        if graph is None and ("nodes" in data or "edges" in data):
            graph = {"nodes": data.get("nodes") or [], "edges": data.get("edges") or []}

        owner_id = data.get(owner_key)
        if owner_id and owner_id != current.get(owner_key):
            # Owner is the only ownership role; unlinking drops the relation — recreate.
            self.delete_subgraph(kind, subgraph_id)
            payload = {
                "kind": kind,
                meta["id_attr"]: subgraph_id,
                owner_key: owner_id,
            }
            if graph is not None:
                payload["graph"] = graph
            return self.create_subgraph(payload)

        if graph is not None:
            return self.put_subgraph_dual(kind, subgraph_id, graph)
        return current

    def put_subgraph_dual(
        self, kind: str, subgraph_id: str, graph: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store both json_string and in-graph entity/relation form (R10-18)."""
        driver = self._driver()
        try:
            try:
                store_dual_form(driver, self.database, kind, subgraph_id, graph)
            except SubgraphCodecError as exc:
                raise CrudError(str(exc)) from exc
            return self.get_subgraph_dual(kind, subgraph_id, _driver=driver)
        finally:
            driver.close()

    def get_subgraph_dual(
        self,
        kind: str,
        subgraph_id: str,
        *,
        _driver: Optional[Driver] = None,
    ) -> Dict[str, Any]:
        """Read dual-form: json_string attribute + reconstructed in-graph graph."""
        own = _driver is None
        driver = _driver or self._driver()
        try:
            meta = self.get_subgraph(kind, subgraph_id, _driver=driver)
            if meta is None:
                raise CrudError(f"{kind} not found: {subgraph_id}")
            try:
                dual = load_dual_form(driver, self.database, kind, subgraph_id)
            except SubgraphCodecError as exc:
                raise CrudError(str(exc)) from exc
            return {**meta, **dual}
        finally:
            if own:
                driver.close()

    def get_subgraph_graph(
        self, kind: str, subgraph_id: str
    ) -> Optional[Dict[str, Any]]:
        """Reconstruct graph JSON from the in-graph form only."""
        driver = self._driver()
        try:
            if self.get_subgraph(kind, subgraph_id, _driver=driver) is None:
                return None
            try:
                return load_graph_from_typedb(
                    driver, self.database, kind, subgraph_id
                )
            except SubgraphCodecError as exc:
                raise CrudError(str(exc)) from exc
        finally:
            driver.close()

    def delete_subgraph(self, kind: str, subgraph_id: str) -> bool:
        if kind not in _SUBGRAPH_META:
            raise CrudError(f"unknown subgraph kind: {kind}")
        meta = _SUBGRAPH_META[kind]
        driver = self._driver()
        try:
            if self.get_subgraph(kind, subgraph_id, _driver=driver) is None:
                return False
            run_write(
                driver,
                self.database,
                f"""
                match $g isa {kind}, has {meta["id_attr"]} {literal_string(subgraph_id)};
                delete $g;
                """,
            )
            return True
        finally:
            driver.close()

    def list_subgraphs(self, kind: str) -> List[Dict[str, Any]]:
        if kind not in _SUBGRAPH_META:
            raise CrudError(f"unknown subgraph kind: {kind}")
        meta = _SUBGRAPH_META[kind]
        driver = self._driver()
        try:
            ids = _collect_strings(
                driver,
                self.database,
                f"match $g isa {kind}, has {meta['id_attr']} $v;",
            )
            return [
                self.get_subgraph(kind, i, _driver=driver) for i in sorted(ids)
            ]  # type: ignore[misc]
        finally:
            driver.close()


def to_json(obj: Any) -> str:
    """Serialize a CRUD result to a JSON string (datetime-safe)."""
    return json.dumps(obj, indent=2, sort_keys=True)


def from_json(text: str) -> Any:
    return json.loads(text)
