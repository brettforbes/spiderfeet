"""R20-02, R20-03, and R20-05 identity contract."""

from __future__ import annotations

import pytest

from spiderfeet_v2.context.identity import (
    IdentityDecision,
    IdentityInputError,
    MergeEvent,
    literal_record,
    normalize_company_name,
    normalize_fqdn,
    normalize_ipv4,
    normalize_ipv6,
    normalize_mac,
    normalize_relation,
    port_identity_key,
    semantic_record,
    source_occurrence_id,
)


def test_same_host_port_fuses_and_other_host_remains_distinct() -> None:
    first = port_identity_key("host|203.0.113.10", "TCP", "443")
    repeat = port_identity_key("host|203.0.113.10", "tcp", 443)
    other = port_identity_key("host|203.0.113.11", "tcp", 443)
    assert first == repeat
    assert first != other


def test_hostname_literal_is_domain_not_system() -> None:
    record = literal_record("WWW.Example.COM.", source_occurrence_id="occ|sg|n1")
    assert record.nugget_id == "DOMAIN_NAME"
    assert record.strategy == "global"
    assert record.identity_key == "DOMAIN_NAME|www.example.com"


@pytest.mark.parametrize(
    ("function", "left", "right"),
    [
        (normalize_ipv4, "203.0.113.10", "203.0.113.10"),
        (normalize_ipv6, "2001:0db8:0000::0001", "[2001:db8::1]"),
        (normalize_mac, "00-1A-2B-3C-4D-5E", "001a.2b3c.4d5e"),
        (normalize_fqdn, "Bücher.Example.", "xn--bcher-kva.example"),
        (normalize_company_name, " Acme   Pty\tLtd ", "acme pty ltd"),
        (normalize_relation, "contains_this", "contains"),
    ],
)
def test_normalizers_are_deterministic_and_idempotent(function, left: str, right: str) -> None:
    assert function(left) == function(right)
    assert function(function(left)) == function(left)


def test_global_values_match_only_when_normalized_equal() -> None:
    occurrence = source_occurrence_id("temporary-subgraph--1", "node-1")
    matched = semantic_record(
        nugget_id="IPV4_ADDRESS",
        nugget_data="203.0.113.10",
        source_occurrence_id=occurrence,
        nugget_instance_id="IPV4_ADDRESS--one",
    )
    same = semantic_record(
        nugget_id="IPV4_ADDRESS",
        nugget_data="203.0.113.10",
        source_occurrence_id=source_occurrence_id("temporary-subgraph--2", "node-2"),
        nugget_instance_id="IPV4_ADDRESS--two",
    )
    different = semantic_record(
        nugget_id="IPV4_ADDRESS",
        nugget_data="203.0.113.11",
        source_occurrence_id=occurrence,
    )
    assert matched.identity_key == same.identity_key
    assert matched.identity_key != different.identity_key
    assert occurrence != matched.nugget_instance_id


def test_parent_scoped_categories_do_not_match_across_parents() -> None:
    left = semantic_record(
        nugget_id="NETWORKS",
        source_occurrence_id="occ|a|1",
        parent_key="host|203.0.113.10",
    )
    same_parent = semantic_record(
        nugget_id="NETWORKS",
        source_occurrence_id="occ|b|1",
        parent_key="host|203.0.113.10",
    )
    other_parent = semantic_record(
        nugget_id="NETWORKS",
        source_occurrence_id="occ|c|1",
        parent_key="host|203.0.113.11",
    )
    assert left.strategy == "parent_scoped"
    assert left.identity_key == same_parent.identity_key
    assert left.identity_key != other_parent.identity_key


def test_observations_remain_unique_when_values_repeat() -> None:
    left = semantic_record(
        nugget_id="HOST_STATUS",
        nugget_data="up",
        source_occurrence_id="occ|scan-a|status",
    )
    right = semantic_record(
        nugget_id="HOST_STATUS",
        nugget_data="up",
        source_occurrence_id="occ|scan-b|status",
    )
    assert left.strategy == "observation"
    assert left.identity_key != right.identity_key


def test_same_address_does_not_resolve_system_identity() -> None:
    left = semantic_record(
        nugget_id="SYSTEM",
        nugget_data="203.0.113.10",
        source_occurrence_id="occ|netdiscover|1",
        workflow_execution_id="workflow-run-1",
        evidence=("ipv4:203.0.113.10",),
    )
    right = semantic_record(
        nugget_id="SYSTEM",
        nugget_data="203.0.113.10",
        source_occurrence_id="occ|nmap|1",
        workflow_execution_id="workflow-run-1",
        evidence=("ipv4:203.0.113.10",),
    )
    grouped = semantic_record(
        nugget_id="SYSTEM",
        source_occurrence_id="occ|nmap|2",
        workflow_execution_id="workflow-run-1",
        same_system_group_id="group-1",
    )
    same_group = semantic_record(
        nugget_id="HOST",
        source_occurrence_id="occ|nerva|1",
        workflow_execution_id="workflow-run-1",
        same_system_group_id="group-1",
    )
    later_run = semantic_record(
        nugget_id="SYSTEM",
        source_occurrence_id="occ|nmap|3",
        workflow_execution_id="workflow-run-2",
        same_system_group_id="group-1",
    )
    assert left.strategy == "evidence_resolved"
    assert left.identity_key != right.identity_key
    assert grouped.identity_key == same_group.identity_key
    assert grouped.identity_key != later_run.identity_key


def test_event_and_decision_schemas_carry_data_without_policy() -> None:
    left = literal_record("203.0.113.10", source_occurrence_id="occ|a|1")
    right = literal_record("host.example", source_occurrence_id="occ|b|1")
    event = MergeEvent(left, right, workflow_execution_id="workflow-run-1")
    decision = IdentityDecision("distinct", "schema only")
    assert event.left.nugget_id == "IPV4_ADDRESS"
    assert event.right.nugget_id == "DOMAIN_NAME"
    assert decision.action == "distinct"
    assert decision.identity_key is None


def test_invalid_values_are_rejected() -> None:
    with pytest.raises(IdentityInputError):
        normalize_ipv4("999.1.1.1")
    with pytest.raises(IdentityInputError):
        semantic_record(nugget_id="PORT", nugget_data="443", source_occurrence_id="occ|1|1")
    with pytest.raises(IdentityInputError):
        semantic_record(
            nugget_id="SYSTEM",
            source_occurrence_id="occ|1|1",
        )
