"""AI2 / R10-08: schema fun projections for project/workflow/scan_step + meta edges."""

from __future__ import annotations

from pathlib import Path
from typing import List, Set, Tuple

import pytest

REPO = Path(__file__).resolve().parents[1]
SCHEMA = REPO / ".seed" / "spiderfeet_v2_semantic.tql"
SMOKE_DB = "spiderfeet-ai2-smoke"

PID = "project--ai2"
WID = "workflow--ai2"
TID = "target--ai2"
SID = "scan_step--ai2"
HOST_ID = "HOST--ai2"
IP_ID = "IPV4_ADDRESS--ai2"
PORT_ID = "TCP_PORT_OPEN--ai2"
STATUS_ID = "HOST_STATUS--ai2"


def _collect_strings(driver, database: str, query: str, column: str = "v") -> List[str]:
    from typedb.api.connection.transaction import TransactionType

    out: List[str] = []
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        for row in answer.as_concept_rows():
            concept = row.get(column)
            if concept is None:
                continue
            value = concept.try_get_value()
            if value is not None:
                out.append(str(value))
    return out


def _collect_pairs(driver, database: str, query: str) -> Set[Tuple[str, str]]:
    from typedb.api.connection.transaction import TransactionType

    out: Set[Tuple[str, str]] = set()
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        for row in answer.as_concept_rows():
            sid = row.get("sid").try_get_value()
            tid = row.get("tid").try_get_value()
            out.add((str(sid), str(tid)))
    return out


def _seed(driver, database: str) -> None:
    from spiderfeet.map.typeql_util import run_write

    run_write(
        driver,
        database,
        f"""
        insert
          $host isa host,
            has nugget_id "HOST",
            has nugget_instance_id "{HOST_ID}",
            has nugget_data "ai2.example";
          $ip isa ipv4-address,
            has nugget_id "IPV4_ADDRESS",
            has nugget_instance_id "{IP_ID}",
            has nugget_data "203.0.113.20";
          $port isa tcp-port-open,
            has nugget_id "TCP_PORT_OPEN",
            has nugget_instance_id "{PORT_ID}",
            has nugget_data "443";
          $st isa host-status,
            has nugget_id "HOST_STATUS",
            has nugget_instance_id "{STATUS_ID}",
            has nugget_data "up";
        """,
    )
    # Edges: host contains ip; host had status; host listens-to port
    run_write(
        driver,
        database,
        f"""
        match
          $host isa host, has nugget_instance_id "{HOST_ID}";
          $ip isa ipv4-address, has nugget_instance_id "{IP_ID}";
          $port isa tcp-port-open, has nugget_instance_id "{PORT_ID}";
          $st isa host-status, has nugget_instance_id "{STATUS_ID}";
        insert
          $c isa contains_this, links (source: $host, target: $ip);
          $h isa has_this, links (source: $host, target: $st);
          $l isa listens_to_this, links (source: $host, target: $port);
        """,
    )
    run_write(
        driver,
        database,
        f"""
        insert
          $t isa target,
            has target_id "{TID}",
            has target_value "ai2.example";
        """,
    )
    run_write(
        driver,
        database,
        f"""
        match
          $ip isa ipv4-address, has nugget_instance_id "{IP_ID}";
          $host isa host, has nugget_instance_id "{HOST_ID}";
        insert
          $s isa scan_step,
            has scan_instance_id "{SID}",
            has scan_ui_cli_command "nmap -sn ai2.example",
            has scan_ui_text_form "text",
            has scan_ui_structured_form "{{}}",
            has scan_ui_graph_form "{{\\"nodes\\":[]}}",
            has scan_ui_markdown_narrative_form "# md";
          $s links (consumed: $host);
          $s links (produced: $ip);
        """,
    )
    run_write(
        driver,
        database,
        f"""
        match
          $s isa scan_step, has scan_instance_id "{SID}";
          $t isa target, has target_id "{TID}";
        insert
          $w isa workflow,
            has workflow_id "{WID}",
            has name "ai2-workflow",
            has workflow_yaml "name: ai2";
          $w links (target: $t);
          $w links (first_step: $s);
          $w links (prior_step: $s);
          $w links (next_step: $s);
        """,
    )
    run_write(
        driver,
        database,
        f"""
        match
          $w isa workflow, has workflow_id "{WID}";
          $s isa scan_step, has scan_instance_id "{SID}";
        insert
          $p isa project, has project_id "{PID}";
          $p links (workflow: $w);
          $pc isa project_context, has project_context_id "project-context--ai2";
          $pc links (project: $p);
          $ts isa temporary_subgraph, has temporary_subgraph_id "temporary-subgraph--ai2";
          $ts links (project: $p);
          $rg isa scan_result_graph, has scan_result_id "scan-result--ai2";
          $rg links (scan_step: $s);
        """,
    )


def test_schema_declares_projection_funs() -> None:
    src = SCHEMA.read_text(encoding="utf-8")
    for name in (
        "fun contains_recursive",
        "fun meta_member",
        "fun meta_related",
        "fun meta_contains_edge_ends",
        "fun meta_had_edge_ends",
        "fun meta_listens_edge_ends",
        "fun project_workflow_ids",
        "fun project_target_ids",
        "fun workflow_first_step_ids",
        "fun scan_step_text_form",
        "fun scan_step_graph_form",
        "fun scan_step_produced_ids",
        "fun scan_step_result_graph_ids",
    ):
        assert name in src, name


def test_fun_projections_seeded_round_trip() -> None:
    pytest.importorskip("typedb.driver")
    from spiderfeet.map.config import TypeDBConfigError, load_connection_config
    from spiderfeet.map.connection import open_driver, ping
    from spiderfeet.map.typeql_util import run_schema

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
        _seed(driver, SMOKE_DB)

        assert PID in _collect_strings(
            driver, SMOKE_DB, "match let $v in project_ids();"
        )
        assert WID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in project_workflow_ids("{PID}");',
        )
        assert TID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in project_target_ids("{PID}");',
        )
        assert "project-context--ai2" in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in project_context_ids("{PID}");',
        )
        assert "temporary-subgraph--ai2" in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in project_temporary_subgraph_ids("{PID}");',
        )
        assert SID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in workflow_first_step_ids("{WID}");',
        )
        assert SID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in workflow_prior_step_ids("{WID}");',
        )
        assert SID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in workflow_next_step_ids("{WID}");',
        )
        assert TID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in workflow_target_ids("{WID}");',
        )

        assert _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_text_form("{SID}");',
        ) == ["text"]
        assert _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_structured_form("{SID}");',
        ) == ["{}"]
        graph = _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_graph_form("{SID}");',
        )
        assert graph and "nodes" in graph[0]
        assert _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_markdown_narrative_form("{SID}");',
        ) == ["# md"]
        cli = _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_cli_command("{SID}");',
        )
        assert cli and cli[0].startswith("nmap")

        assert HOST_ID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_consumed_ids("{SID}");',
        )
        assert IP_ID in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_produced_ids("{SID}");',
        )
        assert "scan-result--ai2" in _collect_strings(
            driver,
            SMOKE_DB,
            f'match let $v in scan_step_result_graph_ids("{SID}");',
        )

        contains = _collect_pairs(
            driver,
            SMOKE_DB,
            f"""
            match
              $root isa host, has nugget_instance_id "{HOST_ID}";
              let $sid, $tid in meta_contains_edge_ends($root);
            """,
        )
        had = _collect_pairs(
            driver,
            SMOKE_DB,
            f"""
            match
              $root isa host, has nugget_instance_id "{HOST_ID}";
              let $sid, $tid in meta_had_edge_ends($root);
            """,
        )
        listens = _collect_pairs(
            driver,
            SMOKE_DB,
            f"""
            match
              $root isa host, has nugget_instance_id "{HOST_ID}";
              let $sid, $tid in meta_listens_edge_ends($root);
            """,
        )
        assert (HOST_ID, IP_ID) in contains
        assert (HOST_ID, STATUS_ID) in had
        assert (HOST_ID, PORT_ID) in listens
    finally:
        try:
            if driver.databases.contains(SMOKE_DB):
                driver.databases.get(SMOKE_DB).delete()
        finally:
            driver.close()
