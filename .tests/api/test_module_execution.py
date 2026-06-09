"""module_execution verdict inference (Stage 4c)."""

from spiderfeet.api.services.module_execution import infer_module_execution


def test_clean_miss_when_finished_zero_events():
    summary = infer_module_execution(
        module_id="sfp_spamcop",
        status="FINISHED",
        events_emitted=0,
        log_rows=[],
        expected_absent_types=["BLACKLISTED_IPADDR"],
        scan_results_by_type={"ROOT": 1, "IP_ADDRESS": 1},
    )
    assert summary.verdict == "clean_miss"
    assert summary.events_emitted == 0


def test_hit_when_module_emitted_events():
    summary = infer_module_execution(
        module_id="sfp_spamhaus",
        status="FINISHED",
        events_emitted=2,
        log_rows=[],
    )
    assert summary.verdict == "hit"


def test_error_failed_on_scan_status():
    summary = infer_module_execution(
        module_id="sfp_spamcop",
        status="ERROR-FAILED",
        events_emitted=0,
        log_rows=[],
    )
    assert summary.verdict == "error_failed"


def test_error_failed_on_module_log():
    summary = infer_module_execution(
        module_id="sfp_spamcop",
        status="FINISHED",
        events_emitted=0,
        log_rows=[(1, "sfp_spamcop", "ERROR", "lookup failed", 9)],
    )
    assert summary.verdict == "error_failed"


def test_absent_violation_when_blocked_type_present():
    summary = infer_module_execution(
        module_id="sfp_spamhaus",
        status="FINISHED",
        events_emitted=0,
        log_rows=[],
        expected_absent_types=["BLACKLISTED_IPADDR"],
        scan_results_by_type={"ROOT": 1, "BLACKLISTED_IPADDR": 1},
    )
    assert summary.verdict == "absent_violation"
    assert summary.absent_violations == ["BLACKLISTED_IPADDR"]
