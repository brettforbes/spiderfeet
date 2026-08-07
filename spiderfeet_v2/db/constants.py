"""Paths and defaults for the SpiderFeet v2 TypeDB database (spiderfeet-actual)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

ACTUAL_DATABASE_NAME = "spiderfeet-actual"

SCHEMA_TQL = REPO_ROOT / ".seed" / "spiderfeet_v2_semantic.tql"

DEFAULT_CONFIG_PATH = REPO_ROOT / ".config" / "typedb.connection.json"
EXAMPLE_CONFIG_PATH = REPO_ROOT / ".config" / "typedb.connection.example.json"

# Relation type (schema) -> (module_id attribute, display name)
CLI_APP_SERVICES = (
    ("sfp-cli-app-nmap", "sfp_cli_nmap", "Nmap CLI App"),
    ("sfp-cli-app-netdiscover", "sfp_cli_netdiscover", "Netdiscover CLI App"),
    ("sfp-cli-app-nerva", "sfp_cli_nerva", "Nerva CLI App"),
    ("sfp-cli-app-pius", "sfp_cli_pius", "Pius CLI App"),
    ("sfp-cli-app-subfinder", "sfp_cli_subfinder", "Subfinder CLI App"),
    ("sfp-cli-app-httpx", "sfp_cli_httpx", "httpx CLI App"),
    ("sfp-cli-app-katana", "sfp_cli_katana", "Katana CLI App"),
    ("sfp-cli-app-nuclei", "sfp_cli_nuclei", "Nuclei CLI App"),
)

SEED_NUGGET_ID = "ROOT"
SEED_NUGGET_INSTANCE = "archetype:ROOT"
SEED_NUGGET_ENTITY = "root"
