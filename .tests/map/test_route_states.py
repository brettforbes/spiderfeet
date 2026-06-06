"""Tests for aggregated module test state overlay."""

from spiderfeet.map.route_states import overlay_test_state


def test_overlay_test_state_prefers_in_test():
    names = (
        "A-to-X-via-sfp_example",
        "A-to-Y-via-sfp_example",
    )
    states = {names[0]: "not-started", names[1]: "in-test"}
    assert overlay_test_state(names, states) == "in-test"


def test_overlay_test_state_not_started_when_empty():
    assert overlay_test_state((), None) == "not-started"
