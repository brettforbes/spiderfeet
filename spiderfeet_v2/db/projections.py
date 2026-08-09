"""Python wrappers over AI2 TypeQL `fun` projections → JSON (R10-19 / AL3).

Contracts: `.governance/project/SPEC010_FUN_PROJECTIONS.md`
Edge names: `.governance/project/SPEC010_EDGE_NAMING.md`
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map.typeql_util import literal_string
from spiderfeet_v2.db.config import TypeDBConnectionConfig, load_connection_config
from spiderfeet_v2.db.connection import open_driver
from spiderfeet_v2.db.subgraph_codec import TYPEQL_TO_JSON

# Graph-JSON edge types assembled from meta_*_edge_ends funs
_META_EDGE_FUNS = (
    ("meta_contains_edge_ends", "contains"),
    ("meta_had_edge_ends", "had"),
    ("meta_listens_edge_ends", "listens-to"),
)


class ProjectionError(Exception):
    """Projection query or assembly failure."""


def _collect_strings(
    driver: Driver,
    database: str,
    query: str,
    column: str = "v",
) -> List[str]:
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


def _collect_pairs(
    driver: Driver,
    database: str,
    query: str,
    source_col: str = "sid",
    target_col: str = "tid",
) -> Set[Tuple[str, str]]:
    out: Set[Tuple[str, str]] = set()
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_rows"):
            return out
        for row in answer.as_concept_rows():
            src = row.get(source_col)
            tgt = row.get(target_col)
            if src is None or tgt is None:
                continue
            sv = src.try_get_value()
            tv = tgt.try_get_value()
            if sv is not None and tv is not None:
                out.add((str(sv), str(tv)))
    return out


def _first_or_none(values: List[str]) -> Optional[str]:
    return values[0] if values else None


def _sorted_unique(values: List[str]) -> List[str]:
    return sorted(set(values))


@dataclass
class ProjectionStore:
    """Fun-driven JSON projections for project / workflow / scan_step / meta subgraph."""

    cfg: TypeDBConnectionConfig
    database: str

    @classmethod
    def connect(
        cls,
        cfg: Optional[TypeDBConnectionConfig] = None,
        *,
        database: Optional[str] = None,
    ) -> "ProjectionStore":
        cfg = cfg or load_connection_config()
        return cls(cfg=cfg, database=database or cfg.database)

    def _driver(self) -> Driver:
        return open_driver(self.cfg)

    def _strings(self, driver: Driver, query: str, column: str = "v") -> List[str]:
        return _collect_strings(driver, self.database, query, column=column)

    def _fun_strings(self, driver: Driver, fun_call: str) -> List[str]:
        return self._strings(driver, f"match let $v in {fun_call};")

    # ------------------------------------------------------------------ catalogue

    def list_project_ids(self) -> List[str]:
        driver = self._driver()
        try:
            return _sorted_unique(self._fun_strings(driver, "project_ids()"))
        finally:
            driver.close()

    # ------------------------------------------------------------------ project

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Assemble project JSON per SPEC010_FUN_PROJECTIONS §2."""
        pid_lit = literal_string(project_id)
        driver = self._driver()
        try:
            ids = self._fun_strings(driver, "project_ids()")
            if project_id not in ids:
                return None
            workflows = _sorted_unique(
                self._fun_strings(driver, f"project_workflow_ids({pid_lit})")
            )
            targets = _sorted_unique(
                self._fun_strings(driver, f"project_target_ids({pid_lit})")
            )
            project_context = _sorted_unique(
                self._fun_strings(driver, f"project_context_ids({pid_lit})")
            )
            temporary_subgraph = _sorted_unique(
                self._fun_strings(driver, f"project_temporary_subgraph_ids({pid_lit})")
            )
            return {
                "project_id": project_id,
                "workflows": workflows,
                "targets": targets,
                "project_context": project_context,
                "temporary_subgraph": temporary_subgraph,
            }
        finally:
            driver.close()

    # ------------------------------------------------------------------ workflow

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Assemble workflow JSON per SPEC010_FUN_PROJECTIONS §3."""
        wid_lit = literal_string(workflow_id)
        driver = self._driver()
        try:
            has_entity = bool(
                _collect_strings(
                    driver,
                    self.database,
                    f"match $w isa workflow, has workflow_id $v; $v == {wid_lit};",
                )
            )
            if not has_entity:
                return None
            targets = self._fun_strings(driver, f"workflow_target_ids({wid_lit})")
            first = self._fun_strings(driver, f"workflow_first_step_ids({wid_lit})")
            prior = self._fun_strings(driver, f"workflow_prior_step_ids({wid_lit})")
            nxt = self._fun_strings(driver, f"workflow_next_step_ids({wid_lit})")
            yaml_vals = self._fun_strings(driver, f"workflow_yaml_string({wid_lit})")
            return {
                "workflow_id": workflow_id,
                "target": _first_or_none(_sorted_unique(targets)),
                "first_step": _first_or_none(_sorted_unique(first)),
                "prior_step": _sorted_unique(prior),
                "next_step": _sorted_unique(nxt),
                "workflow_yaml": _first_or_none(yaml_vals),
            }
        finally:
            driver.close()

    # ------------------------------------------------------------------ scan_step

    def get_scan_step(self, scan_instance_id: str) -> Optional[Dict[str, Any]]:
        """Assemble scan_step JSON (four UI forms + consumed/produced) per §4."""
        sid_lit = literal_string(scan_instance_id)
        driver = self._driver()
        try:
            has_entity = bool(
                _collect_strings(
                    driver,
                    self.database,
                    f"match $s isa scan_step, has scan_instance_id $v; $v == {sid_lit};",
                )
            )
            if not has_entity:
                return None
            cli = self._fun_strings(driver, f"scan_step_cli_command({sid_lit})")
            text = self._fun_strings(driver, f"scan_step_text_form({sid_lit})")
            structured = self._fun_strings(
                driver, f"scan_step_structured_form({sid_lit})"
            )
            graph = self._fun_strings(driver, f"scan_step_graph_form({sid_lit})")
            narrative = self._fun_strings(
                driver, f"scan_step_markdown_narrative_form({sid_lit})"
            )
            consumed = _sorted_unique(
                self._fun_strings(driver, f"scan_step_consumed_ids({sid_lit})")
            )
            produced = _sorted_unique(
                self._fun_strings(driver, f"scan_step_produced_ids({sid_lit})")
            )
            result_graphs = _sorted_unique(
                self._fun_strings(driver, f"scan_step_result_graph_ids({sid_lit})")
            )
            return {
                "scan_instance_id": scan_instance_id,
                "cli_command": _first_or_none(cli),
                "text_form": _first_or_none(text),
                "structured_form": _first_or_none(structured),
                "graph_form": _first_or_none(graph),
                "markdown_narrative_form": _first_or_none(narrative),
                "consumed": consumed,
                "produced": produced,
                "scan_result_graph": result_graphs,
            }
        finally:
            driver.close()

    # ----------------------------------------------------------- meta subgraph

    def get_meta_subgraph(self, root_nugget_instance_id: str) -> Optional[Dict[str, Any]]:
        """Assemble meta-concept subgraph edges (contains / had / listens-to).

        Uses meta_*_edge_ends funs; tags each pair with graph-JSON ``type``
        from SPEC010_EDGE_NAMING (inverse of TypeQL ``*_this``).
        """
        rid_lit = literal_string(root_nugget_instance_id)
        driver = self._driver()
        try:
            has_root = bool(
                _collect_strings(
                    driver,
                    self.database,
                    f"match $n isa nugget, has nugget_instance_id $v; $v == {rid_lit};",
                )
            )
            if not has_root:
                return None
            edges: List[Dict[str, str]] = []
            node_ids: Set[str] = {root_nugget_instance_id}
            for fun_name, json_type in _META_EDGE_FUNS:
                if json_type not in TYPEQL_TO_JSON.values():
                    raise ProjectionError(
                        f"edge type {json_type!r} missing from TYPEQL_TO_JSON"
                    )
                pairs = _collect_pairs(
                    driver,
                    self.database,
                    f"""
                    match
                      $root isa nugget, has nugget_instance_id {rid_lit};
                      let $sid, $tid in {fun_name}($root);
                    """,
                )
                for src, tgt in sorted(pairs):
                    node_ids.add(src)
                    node_ids.add(tgt)
                    edges.append({"from": src, "to": tgt, "type": json_type})
            return {
                "root": root_nugget_instance_id,
                "nodes": sorted(node_ids),
                "edges": edges,
            }
        finally:
            driver.close()


def assemble_project_complete(store: Any, project_id: str) -> Optional[Dict[str, Any]]:
    """One-call Composer load shape (R13-06).

    Returns ``{project, workflows:[{attrs…, workflow_yaml, steps:[summary], target}]}``
    assembled from CRUD rows (no TypeQL funs required).
    """
    project = store.get_project(project_id)
    if project is None:
        return None

    workflows_out: List[Dict[str, Any]] = []
    for wid in project.get("workflow_ids") or []:
        wf = store.get_workflow(wid)
        if wf is None:
            continue

        step_ids: Set[str] = set(wf.get("prior_step_ids") or [])
        step_ids.update(wf.get("next_step_ids") or [])
        if wf.get("first_step_id"):
            step_ids.add(wf["first_step_id"])

        steps: List[Dict[str, Any]] = []
        for sid in sorted(step_ids):
            step = store.get_scan_step(sid)
            if step is None:
                steps.append({"scan_instance_id": sid, "missing": True})
                continue
            roles: List[str] = []
            if sid == wf.get("first_step_id"):
                roles.append("first")
            if sid in (wf.get("prior_step_ids") or []):
                roles.append("prior")
            if sid in (wf.get("next_step_ids") or []):
                roles.append("next")
            steps.append(
                {
                    "scan_instance_id": sid,
                    "step_module_id": step.get("step_module_id"),
                    "scan_status": step.get("scan_status"),
                    "roles": roles,
                }
            )

        target = None
        tid = wf.get("target_id")
        if tid:
            target = store.get_target(tid)

        workflows_out.append(
            {
                "workflow_id": wf.get("workflow_id") or wid,
                "name": wf.get("name"),
                "description": wf.get("description"),
                "author": wf.get("author"),
                "created": wf.get("created"),
                "workflow_yaml": wf.get("workflow_yaml"),
                "project_id": wf.get("project_id") or project_id,
                "target_id": tid,
                "first_step_id": wf.get("first_step_id"),
                "prior_step_ids": list(wf.get("prior_step_ids") or []),
                "next_step_ids": list(wf.get("next_step_ids") or []),
                "steps": steps,
                "target": target,
            }
        )

    return {"project": project, "workflows": workflows_out}


# Module-level convenience wrappers (stateless connect-per-call)

def project_json(
    project_id: str,
    *,
    cfg: Optional[TypeDBConnectionConfig] = None,
    database: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    return ProjectionStore.connect(cfg, database=database).get_project(project_id)


def workflow_json(
    workflow_id: str,
    *,
    cfg: Optional[TypeDBConnectionConfig] = None,
    database: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    return ProjectionStore.connect(cfg, database=database).get_workflow(workflow_id)


def scan_step_json(
    scan_instance_id: str,
    *,
    cfg: Optional[TypeDBConnectionConfig] = None,
    database: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    return ProjectionStore.connect(cfg, database=database).get_scan_step(scan_instance_id)


def meta_subgraph_json(
    root_nugget_instance_id: str,
    *,
    cfg: Optional[TypeDBConnectionConfig] = None,
    database: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    return ProjectionStore.connect(cfg, database=database).get_meta_subgraph(
        root_nugget_instance_id
    )
