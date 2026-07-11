#!/usr/bin/env python3
"""Resolve Windows WiFi adapters for nuclei interface binding (-i / -sip)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from typing import Any

# USB / secondary adapter naming variants seen on operator workstations.
WIFI2_ALIASES = re.compile(r"^wi[-\s]?fi\s*2$", re.IGNORECASE)
MAIN_WIFI_ALIASES = re.compile(r"^wi[-\s]?fi$", re.IGNORECASE)


def _powershell_adapters() -> list[dict[str, Any]]:
    if sys.platform != "win32":
        return []
    script = (
        "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {"
        " $ip = (Get-NetIPAddress -InterfaceAlias $_.Name -AddressFamily IPv4 -ErrorAction SilentlyContinue "
        "| Where-Object { $_.IPAddress -notlike '169.254*' } | Select-Object -First 1).IPAddress;"
        " [PSCustomObject]@{ name = $_.Name; ip = $ip }"
        "} | ConvertTo-Json -Compress"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    payload = json.loads(proc.stdout)
    if isinstance(payload, dict):
        return [payload]
    return list(payload)


def resolve_wifi_adapters() -> dict[str, str | None]:
    """Return {wifi2_name, wifi2_ip, wifi_name, wifi_ip} for connected adapters."""
    adapters = _powershell_adapters()
    wifi2_name: str | None = None
    wifi2_ip: str | None = None
    wifi_name: str | None = None
    wifi_ip: str | None = None

    for adapter in adapters:
        name = str(adapter.get("name") or "").strip()
        ip = adapter.get("ip")
        ip_str = str(ip).strip() if ip else None
        if not name:
            continue
        if WIFI2_ALIASES.match(name):
            wifi2_name, wifi2_ip = name, ip_str
        elif MAIN_WIFI_ALIASES.match(name):
            wifi_name, wifi_ip = name, ip_str

    return {
        "wifi2_name": wifi2_name,
        "wifi2_ip": wifi2_ip,
        "wifi_name": wifi_name,
        "wifi_ip": wifi_ip,
    }


def default_scan_interface(explicit: str | None = None) -> tuple[str | None, str | None]:
    """Pick nuclei -i / -sip values. Prefers WiFi 2 when connected."""
    if explicit:
        return explicit, None
    adapters = resolve_wifi_adapters()
    if adapters.get("wifi2_name"):
        return adapters["wifi2_name"], adapters.get("wifi2_ip")
    if adapters.get("wifi_name"):
        return adapters["wifi_name"], adapters.get("wifi_ip")
    return None, None


def dual_scan_plan() -> list[dict[str, str | None]]:
    """Ordered worker plan: WiFi 2 first, then main WiFi."""
    adapters = resolve_wifi_adapters()
    plan: list[dict[str, str | None]] = []
    if adapters.get("wifi2_name"):
        plan.append(
            {
                "worker_id": "0",
                "label": "wifi2",
                "interface": adapters["wifi2_name"],
                "source_ip": adapters.get("wifi2_ip"),
            }
        )
    if adapters.get("wifi_name"):
        plan.append(
            {
                "worker_id": str(len(plan)),
                "label": "wifi",
                "interface": adapters["wifi_name"],
                "source_ip": adapters.get("wifi_ip"),
            }
        )
    return plan
