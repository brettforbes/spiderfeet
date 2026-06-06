"""Tests for pilot nugget sample targets (Stage 4c) and module seed registry (Stage 4b)."""

from spiderfeet import SpiderFeetHelpers
from spiderfeet.map.test_targets import (
    all_nugget_samples,
    load_module_test_seeds,
    pilot_module_ids,
    registry_input_value,
    sample_target_for_module,
    sample_target_for_nugget,
)


def test_all_nugget_samples_are_valid_spiderfeet_targets():
    samples = all_nugget_samples()
    assert len(samples) >= 30
    for nugget_id, value in samples.items():
        assert SpiderFeetHelpers.targetTypeFromString(value) is not None, nugget_id


def test_internet_name_sample():
    assert sample_target_for_nugget("INTERNET_NAME") == "sbs.com.au"


def test_unknown_nugget_returns_none():
    assert sample_target_for_nugget("NOT_A_NUGGET") is None


def test_registry_has_ten_pilot_modules():
    seeds = load_module_test_seeds()
    assert len(seeds) >= 10
    assert "sfp_duckduckgo" in seeds
    assert "sfp_robtex" in seeds
    assert len(pilot_module_ids()) >= 10


def test_registry_lookup_duckduckgo():
    assert registry_input_value("sfp_duckduckgo", "INTERNET_NAME") == "bbc.co.uk"
    assert (
        sample_target_for_module("sfp_duckduckgo", "INTERNET_NAME", "INTERNET_NAME")
        == "bbc.co.uk"
    )


def test_registry_lookup_robtex():
    assert registry_input_value("sfp_robtex", "IP_ADDRESS") == "8.8.8.8"


def test_registry_values_are_valid_targets():
    for module_id, consumed_map in load_module_test_seeds().items():
        for consumed_id, entry in consumed_map.items():
            value = entry.get("input_value")
            assert value, f"{module_id}:{consumed_id}"
            assert (
                SpiderFeetHelpers.targetTypeFromString(str(value)) is not None
            ), f"{module_id}:{consumed_id}"


def test_fallback_when_no_registry_entry():
    assert sample_target_for_module("sfp_not_in_registry", "DOMAIN_NAME", "DOMAIN_NAME") == (
        "sbs.com.au"
    )
