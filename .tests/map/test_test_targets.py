"""Tests for pilot nugget sample targets (Stage 4c)."""

from spiderfeet import SpiderFeetHelpers
from spiderfeet.map.test_targets import all_nugget_samples, sample_target_for_nugget


def test_all_nugget_samples_are_valid_spiderfeet_targets():
    samples = all_nugget_samples()
    assert len(samples) >= 30
    for nugget_id, value in samples.items():
        assert SpiderFeetHelpers.targetTypeFromString(value) is not None, nugget_id


def test_internet_name_sample():
    assert sample_target_for_nugget("INTERNET_NAME") == "sbs.com.au"


def test_unknown_nugget_returns_none():
    assert sample_target_for_nugget("NOT_A_NUGGET") is None
