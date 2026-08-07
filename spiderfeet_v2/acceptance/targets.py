"""Documented acceptance targets for SPEC-010 R10-29 / R10-30.

The canonical 4-target live set is defined by the spec. Operators may pass
``--target`` for a single host (lab or one of the documented four) without
claiming the full G3 acceptance run.
"""

from __future__ import annotations

from typing import Dict, List, TypedDict


class TargetDoc(TypedDict):
    host: str
    note: str


# Spec R10-29 example targets (AP1 live evidence / G3 operator gate).
DOCUMENTED_TARGETS: List[TargetDoc] = [
    {
        "host": "sbs.com.au",
        "note": "SPEC-010 R10-29 acceptance target (media / CDN-heavy)",
    },
    {
        "host": "k2am.com.au",
        "note": "SPEC-010 R10-29 acceptance target (smaller org)",
    },
    {
        "host": "venturecapitalopportunitiesfund.com.au",
        "note": "SPEC-010 R10-29 acceptance target (sparse / permissive lab-like)",
    },
    {
        "host": "squarepeg.vc",
        "note": "SPEC-010 R10-29 acceptance target (VC / alternate TLD)",
    },
]

DEFAULT_TARGETS: List[str] = [t["host"] for t in DOCUMENTED_TARGETS]

# Optional lab hosts for harness dry-runs / local smoke (not G3 evidence).
LAB_TARGETS: Dict[str, str] = {
    "example.com": "IANA example — dry-run / schedule smoke only",
}


def is_documented(host: str) -> bool:
    return host.lower().rstrip(".") in {t.lower() for t in DEFAULT_TARGETS}


def normalize_host(raw: str) -> str:
    host = raw.strip().lower()
    for prefix in ("https://", "http://"):
        if host.startswith(prefix):
            host = host[len(prefix) :]
    host = host.split("/")[0].rstrip(".")
    if not host:
        raise ValueError(f"empty target host from {raw!r}")
    return host
