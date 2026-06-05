"""Unit tests for TypeDB connection config loading."""

import json
from pathlib import Path

import pytest

from spiderfeet.map.config import TypeDBConfigError, TypeDBConnectionConfig, load_connection_config


def test_from_dict_minimal():
    cfg = TypeDBConnectionConfig.from_dict(
        {
            "addresses": "host:1729",
            "username": "admin",
            "password": "secret",
            "database": "spiderfeet-map",
        }
    )
    assert cfg.addresses == "host:1729"
    assert cfg.database == "spiderfeet-map"
    assert cfg.tls_enabled is False


def test_from_dict_rejects_empty_password():
    with pytest.raises(TypeDBConfigError):
        TypeDBConnectionConfig.from_dict({"username": "admin", "password": ""})


def test_load_connection_config(tmp_path: Path):
    path = tmp_path / "typedb.connection.json"
    path.write_text(
        json.dumps(
            {
                "addresses": "127.0.0.1:1729",
                "username": "admin",
                "password": "pw",
                "database": "spiderfeet-map",
            }
        ),
        encoding="utf-8",
    )
    cfg = load_connection_config(path)
    assert cfg.password == "pw"
