"""TypeQL string helpers and transaction runners."""

from __future__ import annotations

from typing import Iterable, List, Optional

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType
from typedb.common.exception import TypeDBDriverException


def escape_string(value: str) -> str:
    """Escape a string for TypeQL double-quoted literals."""
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
        .replace("\r", "\\n")
    )


def literal_string(value: str) -> str:
    return f'"{escape_string(value)}"'


def literal_strings(values: Iterable[str]) -> List[str]:
    return [literal_string(v) for v in values]


def run_schema(driver: Driver, database: str, query: str) -> None:
    """Execute a schema query and commit."""
    with driver.transaction(database, TransactionType.SCHEMA) as tx:
        tx.query(query).resolve()
        tx.commit()


def run_write(driver: Driver, database: str, query: str) -> None:
    """Execute a write query and commit."""
    with driver.transaction(database, TransactionType.WRITE) as tx:
        tx.query(query).resolve()
        tx.commit()


def run_writes(driver: Driver, database: str, queries: List[str]) -> None:
    """Execute multiple write queries in one transaction."""
    if not queries:
        return
    with driver.transaction(database, TransactionType.WRITE) as tx:
        for query in queries:
            tx.query(query).resolve()
        tx.commit()


def run_read_exists(driver: Driver, database: str, query: str) -> bool:
    """Return True when a read query yields at least one concept row."""
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if hasattr(answer, "as_concept_rows"):
            for _ in answer.as_concept_rows():
                return True
        return False


def run_read_scalar(driver: Driver, database: str, query: str) -> Optional[int]:
    """Run a reduce query and return the first integer column (e.g. $c)."""
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_rows"):
            return None
        for row in answer.as_concept_rows():
            for name in row.column_names():
                concept = row.get(name)
                if concept is None:
                    continue
                value = concept.try_get_value()
                if value is not None:
                    return int(value)
        return None


def is_connection_refused(exc: BaseException) -> bool:
    text = str(exc)
    return isinstance(exc, TypeDBDriverException) and (
        "actively refused" in text or "Unable to connect" in text
    )


def split_define_blocks(schema_text: str) -> List[str]:
    """
    Split a .tql schema file into define statements.

    The seed file is one `define` block; TypeDB accepts it as a single query.
    """
    text = schema_text.strip()
    if not text:
        return []
    if text.endswith(";"):
        return [text]
    return [text + ";"]
