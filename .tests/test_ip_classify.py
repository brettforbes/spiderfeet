"""Tests for SPEC-005 central IP classification."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.ip_classify import assert_ip_nugget, classify_ip


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("192.168.1.1", "IPV4_ADDRESS"),
        ("10.0.0.5", "IPV4_ADDRESS"),
        ("2001:db8::1", "IPV6_ADDRESS"),
        ("[2001:db8::1]", "IPV6_ADDRESS"),
        ("::1", "IPV6_ADDRESS"),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", "IPV6_ADDRESS"),
    ],
)
def test_classify_ip_host_role(value: str, expected: str) -> None:
    assert classify_ip(value) == expected


@pytest.mark.parametrize(
    ("value", "role", "expected"),
    [
        ("172.16.0.1", "internal", "INTERNAL_IP_ADDRESS"),
        ("203.0.113.9", "affiliate", "AFFILIATE_IPADDR"),
        ("2001:db8:aff::9", "affiliate", "AFFILIATE_IPV6_ADDRESS"),
    ],
)
def test_classify_ip_roles(value: str, role: str, expected: str) -> None:
    assert classify_ip(value, role=role) == expected


@pytest.mark.parametrize("value", ["", "example.com", "not-an-ip", "999.999.999.999"])
def test_classify_ip_rejects_non_ip(value: str) -> None:
    assert classify_ip(value) is None


def test_assert_ip_nugget_passes_for_correct_id() -> None:
    assert_ip_nugget("192.168.0.1", "IPV4_ADDRESS")


def test_assert_ip_nugget_raises_for_ipv6_mislabel() -> None:
    with pytest.raises(ValueError, match="IPV6_ADDRESS"):
        assert_ip_nugget("2001:db8::1", "IPV4_ADDRESS")


def test_ip_nugget_node_emits_ipv4_entity() -> None:
    from core.graph_builder import GraphBuilder
    from core.ip_classify import ip_nugget_node

    builder = GraphBuilder()
    node = builder.add_node(ip_nugget_node("8.8.8.8"))
    assert node["nugget_id"] == "IPV4_ADDRESS"
    assert node["nugget_data"] == "8.8.8.8"


def test_ip_nugget_node_emits_ipv6_entity() -> None:
    from core.graph_builder import GraphBuilder

    builder = GraphBuilder()
    from core.ip_classify import ip_nugget_node

    node = builder.add_node(ip_nugget_node("2001:db8::1"))
    assert node["nugget_id"] == "IPV6_ADDRESS"
    assert node["nugget_data"] == "2001:db8::1"
