#!/usr/bin/env python3
"""Report which external CLI tools required by sfp_tool_* modules are on PATH."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.tools.cli_paths import TOOLS_BIN, resolve_cli_binary  # noqa: E402

# module_id -> (binary name, install hint)
CLI_TOOLS = {
    "sfp_tool_cmseek": ("cmseek", "pip install cmseek OR clone CMSeeK repo"),
    "sfp_tool_dnstwist": ("dnstwist", "pip install dnstwist"),
    "sfp_tool_nbtscan": ("nbtscan", "OS package / http://www.unixwiz.net/tools/nbtscan.html"),
    "sfp_tool_nmap": ("nmap", "winget install Insecure.Nmap"),
    "sfp_tool_nuclei": ("nuclei", ".seed/scripts/install_dev_cli_tools.ps1"),
    "sfp_tool_onesixtyone": ("onesixtyone", "https://github.com/trailofbits/onesixtyone"),
    "sfp_tool_retirejs": ("retire", "npm install -g retire"),
    "sfp_tool_snallygaster": ("snallygaster", "pip install snallygaster"),
    "sfp_tool_testsslsh": ("testssl.sh", "https://testssl.sh"),
    "sfp_tool_trufflehog": ("trufflehog", ".seed/scripts/install_dev_cli_tools.ps1"),
    "sfp_tool_wafw00f": ("wafw00f", "pip install wafw00f"),
    "sfp_tool_wappalyzer": ("wappalyzer", "Legacy AliasIO cli.js required"),
    "sfp_tool_whatweb": ("whatweb", "gem install whatweb OR OS package"),
}


def ensure_dev_tool_paths() -> None:
    prefixes: list[str] = []
    venv_scripts = REPO_ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin")
    if venv_scripts.is_dir():
        prefixes.append(str(venv_scripts))
    if TOOLS_BIN.is_dir():
        prefixes.append(str(TOOLS_BIN))
    if sys.platform == "win32":
        for candidate in (
            r"C:\Program Files (x86)\Nmap",
            r"C:\Program Files\Nmap",
            r"C:\nvm4w\nodejs",
        ):
            if os.path.isdir(candidate):
                prefixes.append(candidate)

    current = os.environ.get("PATH", "")
    merged = os.pathsep.join(p for p in prefixes if p and p not in current.split(os.pathsep))
    if merged:
        os.environ["PATH"] = merged + os.pathsep + current


def probe() -> list[dict]:
    rows = []
    for module_id, (binary, hint) in sorted(CLI_TOOLS.items()):
        found = resolve_cli_binary(binary)
        rows.append(
            {
                "module_id": module_id,
                "binary": binary,
                "on_path": bool(found),
                "path": found or "",
                "install_hint": hint,
            }
        )
    return rows


def main() -> int:
    ensure_dev_tool_paths()
    rows = probe()
    present = sum(1 for r in rows if r["on_path"])
    print(f"CLI tools on PATH: {present}/{len(rows)}")
    for row in rows:
        status = "OK" if row["on_path"] else "MISSING"
        path = f" ({row['path']})" if row["path"] else ""
        print(f"  [{status}] {row['module_id']}: {row['binary']}{path}")
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2))
    return 0 if present == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
