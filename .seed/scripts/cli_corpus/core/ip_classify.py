"""Central IPv4/IPv6 nugget classification (SPEC-005 H1)."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_RULES_PATH = Path(__file__).resolve().parents[1] / "rules" / "_shared" / "ip_patterns.yaml"


def _normalize_ip(value: str) -> str:
    text = (value or "").strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1].strip()
    return text


@lru_cache(maxsize=1)
def _load_patterns() -> dict[str, Any]:
    data = yaml.safe_load(_RULES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{_RULES_PATH} must be a YAML mapping")
    patterns = data.get("patterns") or {}
    roles = data.get("roles") or {}
    ipv4_re = re.compile(str(patterns.get("ipv4", "")), re.VERBOSE)
    ipv6_raw = str(patterns.get("ipv6", ""))
    ipv6_re = re.compile(ipv6_raw.replace("\n", ""), re.VERBOSE)
    return {"ipv4_re": ipv4_re, "ipv6_re": ipv6_re, "roles": roles}


def _ip_version(value: str) -> str | None:
    if not value:
        return None
    if ":" in value:
        return "ipv6"
    if "." in value:
        return "ipv4"
    return None


def classify_ip(value: str, *, role: str = "host") -> str | None:
    """Return nugget_id for an IP literal, or None if not an IP."""
    normalized = _normalize_ip(value)
    version = _ip_version(normalized)
    if version is None:
        return None

    cfg = _load_patterns()
    roles = cfg["roles"]
    role_map = roles.get(role) or roles.get("host") or {}
    if version == "ipv4":
        if not cfg["ipv4_re"].fullmatch(normalized):
            return None
        return role_map.get("ipv4")
    if not cfg["ipv6_re"].fullmatch(normalized):
        return None
    return role_map.get("ipv6")


def assert_ip_nugget(value: str, nugget_id: str, *, role: str = "host") -> None:
    """Raise ValueError when value is an IP but nugget_id does not match classify_ip."""
    expected = classify_ip(value, role=role)
    if expected is None:
        return
    if expected != nugget_id:
        raise ValueError(
            f"IP {value!r} should use nugget_id {expected!r}, not {nugget_id!r} (role={role})"
        )


def ip_nugget_node(
    value: str,
    *,
    role: str = "host",
    description: str = "IP Address",
    **kwargs: Any,
) -> dict[str, Any]:
    """Build a catalogue-backed nugget node for an IP literal."""
    from .graph_builder import nugget_node

    nugget_id = classify_ip(value, role=role)
    if not nugget_id:
        raise ValueError(f"Not a classifiable IP address: {value!r}")
    return nugget_node(nugget_id, value, description=description, **kwargs)
