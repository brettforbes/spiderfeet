"""SPEC-019 E1 — smoke bundle paths referenced by SPEC019_E1_E2E_SMOKE.md exist."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

E1_DOC = REPO / ".docs" / "docs-for-cli-tools" / "SPEC019_E1_E2E_SMOKE.md"

PYTEST_PATHS = [
    "spiderfeet_v2/workflow/tests/test_gse_ip_port_host_scope.py",
    "spiderfeet_v2/workflow/tests/test_gse_12a_chain.py",
    "spiderfeet_v2/workflow/tests/test_gse_nerva_list_fixture.py",
    "modules_v2/tests/test_sfp_cli_nerva.py",
    "modules_v2/_core/tests/test_spec019_f3_subfinder.py",
    "modules_v2/_core/tests/test_spec019_f4_httpx.py",
    "modules_v2/_core/tests/test_spec019_f5_katana.py",
    "modules_v2/_core/tests/test_spec019_f7_nerva.py",
    "modules_v2/_core/tests/test_spec019_f8_validator.py",
    "modules_v2/tests/test_sfp_cli_nuclei.py",
]


def test_e1_smoke_doc_present() -> None:
    assert E1_DOC.is_file(), "E1 evidence doc missing"


def test_e1_smoke_referenced_tests_present() -> None:
    missing = [p for p in PYTEST_PATHS if not (REPO / p).is_file()]
    assert not missing, f"missing E1 test modules: {missing}"
