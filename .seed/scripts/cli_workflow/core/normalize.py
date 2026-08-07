"""Input normalization helpers."""

from __future__ import annotations

from urllib.parse import urlparse


def hostname_from_url(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return v
    if "://" not in v:
        # host or host/path without scheme
        return v.split("/")[0].split(":")[0]
    parsed = urlparse(v)
    host = parsed.hostname or ""
    return host


def normalize_list(values: list[str], mode: str | None) -> list[str]:
    if not mode or mode == "none":
        return list(values)
    if mode == "hostname_from_url":
        return [hostname_from_url(v) for v in values]
    raise ValueError(f"unknown normalize mode: {mode}")
