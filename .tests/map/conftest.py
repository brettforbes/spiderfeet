"""Fixtures for map / TypeDB tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from spiderfeet.map.config import load_connection_config
from spiderfeet.map.connection import ping
from spiderfeet.map.constants import DEFAULT_CONFIG_PATH


def typedb_integration_available() -> bool:
    if os.environ.get("SPIDERFEET_SKIP_TYPEDB") == "1":
        return False
    if not DEFAULT_CONFIG_PATH.is_file() and not os.environ.get("SPIDERFEET_TYPEDB_CONFIG"):
        return False
    try:
        cfg = load_connection_config()
    except Exception:
        return False
    return ping(cfg)


@pytest.fixture(scope="session")
def typedb_config():
    if not typedb_integration_available():
        pytest.skip("TypeDB not configured or server unreachable")
    return load_connection_config()


@pytest.fixture(scope="session")
def typedb_database(typedb_config):
    return typedb_config.database
