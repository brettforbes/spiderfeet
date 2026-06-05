"""Read route_state from TypeDB for catalog overlay (Stage 4)."""

from __future__ import annotations

from typing import Dict, Optional

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map import typeql_util


def fetch_route_states(driver: Driver, database: str) -> Dict[str, str]:
    """Map route_name → route_state for all route relations in the database."""
    query = """
match
  $r isa route,
    has route_name $rn,
    has route_state $rs;
fetch {
  "route_name": $rn,
  "route_state": $rs
};
"""
    states: Dict[str, str] = {}
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_documents"):
            return states
        for row in answer.as_concept_documents():
            name = row.get("route_name")
            state = row.get("route_state")
            if name and state:
                states[str(name)] = str(state)
    return states


def overlay_route_state(
    route_name: str,
    typedb_states: Optional[Dict[str, str]],
) -> str:
    if typedb_states and route_name in typedb_states:
        return typedb_states[route_name]
    return "not-started"
