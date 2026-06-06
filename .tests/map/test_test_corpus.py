"""Unit tests for test nugget corpus CSV and validation planning."""

from pathlib import Path

from spiderfeet.map.test_corpus import (
    CSV_COLUMNS,
    CorpusRow,
    load_test_corpus_csv,
    plan_validation_items,
    rows_from_seed_registry,
    write_test_corpus_csv,
)


def test_csv_columns_defined():
    assert "module_id" in CSV_COLUMNS
    assert "validated_produces" in CSV_COLUMNS


def test_registry_exports_corpus_rows():
    rows = rows_from_seed_registry()
    assert len(rows) >= 10
    duck = next(r for r in rows if r.module_id == "sfp_duckduckgo" and r.consumed_nugget_id == "INTERNET_NAME")
    assert duck.input_value == "bbc.co.uk"
    assert duck.region == "UK"


def test_csv_roundtrip(tmp_path: Path):
    sample = [
        CorpusRow(
            module_id="sfp_duckduckgo",
            consumed_nugget_id="INTERNET_NAME",
            region="UK",
            input_value="bbc.co.uk",
            validated_produces=True,
            notes="smoke",
        )
    ]
    path = tmp_path / "test_nugget_data.csv"
    write_test_corpus_csv(sample, path)
    loaded = load_test_corpus_csv(path)
    assert len(loaded) == 1
    assert loaded[0].validated_produces is True
    assert loaded[0].input_value == "bbc.co.uk"


def test_plan_validation_items_none_tier():
    items = plan_validation_items(configured_modules={}, subscription_tier="none", module_limit=5)
    assert len(items) == 5
    assert all(item["subscription_tier"] == "none" for item in items)
    assert all(item["input_value"] for item in items)
