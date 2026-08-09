"""SPEC-014 R14-01 — meta-concept registry loader tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.meta_concept_registry import (  # noqa: E402
    REQUIRED_CONCEPT_KEYS,
    MetaConceptRegistryError,
    clear_registry_cache,
    get_meta_concept,
    list_meta_concepts,
    load_narrative_v2,
    mermaid_settings,
    registry_path,
)

MIRROR_PATH = REPO_ROOT / "modules_v2" / "_rules" / "_shared" / "narrative_v2.yaml"


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_registry_cache()
    yield
    clear_registry_cache()


def test_registry_path_exists():
    assert registry_path().is_file()


def test_load_narrative_v2_has_required_concepts():
    data = load_narrative_v2()
    concepts = data["meta_concepts"]
    for key in REQUIRED_CONCEPT_KEYS:
        assert key in concepts
        concept = concepts[key]
        assert concept["root_nugget_ids"], key
        assert isinstance(concept["category_nugget_ids"], list)
        assert int(concept["example_cap"]) >= 1
        assert concept["heading"]


def test_list_meta_concepts_sorted_by_order():
    rows = list_meta_concepts()
    orders = [int(r["order"]) for r in rows]
    assert orders == sorted(orders)
    assert rows[0]["id"] == "scan"
    assert any(r["id"] == "trace" and r.get("category_like") for r in rows)


def test_get_meta_concept_domain_and_org():
    domain = get_meta_concept("domain")
    assert "DOMAIN_NAME" in domain["root_nugget_ids"]
    assert "DOMAIN_NAME" in (domain.get("child_nugget_ids") or [])
    org = get_meta_concept("org")
    assert "COMPANY_NAME" in org["root_nugget_ids"]
    assert "DOMAINS" in org["category_nugget_ids"]


def test_mermaid_settings_caps():
    settings = mermaid_settings()
    assert settings["shape_cap"] == 12
    assert settings["example_cap_default"] == 3
    assert settings["mode"] == "type_relation"


def test_modules_v2_mirror_matches_cli_corpus():
    active = yaml.safe_load(registry_path().read_text(encoding="utf-8"))
    mirror = yaml.safe_load(MIRROR_PATH.read_text(encoding="utf-8"))
    assert active == mirror


def test_invalid_registry_raises(tmp_path: Path):
    bad = tmp_path / "narrative_v2.yaml"
    bad.write_text("version: 2\nmeta_concepts: {}\n", encoding="utf-8")
    with pytest.raises(MetaConceptRegistryError):
        load_narrative_v2(str(bad))
