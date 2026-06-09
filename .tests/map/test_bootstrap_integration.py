"""Integration tests against a live TypeDB (optional)."""

import pytest

from spiderfeet.map.bootstrap import bootstrap_map, nugget_exists, service_exists
from spiderfeet.map.connection import driver_session
from spiderfeet.map.constants import MAP_DATABASE_NAME


@pytest.mark.typedb
def test_bootstrap_idempotent(typedb_config, typedb_database):
    report1 = bootstrap_map(typedb_config, database=typedb_database)
    assert report1.database == typedb_database
    report2 = bootstrap_map(typedb_config, database=typedb_database)
    assert report2.created_database is False
    assert report2.applied_schema is False
    assert report2.ok

    with driver_session(typedb_config) as driver:
        assert nugget_exists(driver, typedb_database, "INTERNET_NAME")
        assert service_exists(driver, typedb_database, "sfp_virustotal")
