"""Paths and defaults for the SpiderFeet map TypeDB database."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

MAP_DATABASE_NAME = "spiderfeet-map"

SCHEMA_TQL = REPO_ROOT / ".seed" / "spiderfeet_map.tql"
NUGGETS_JSON = REPO_ROOT / ".docs" / "analysis" / "nuggets.json"
OSINT_SERVICES_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
MODULE_TEST_SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"

DEFAULT_CONFIG_PATH = REPO_ROOT / ".config" / "typedb.connection.json"
EXAMPLE_CONFIG_PATH = REPO_ROOT / ".config" / "typedb.connection.example.json"

ARCHETYPE_INSTANCE_PREFIX = "archetype:"
