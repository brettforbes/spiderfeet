#!/usr/bin/env python3
"""Report which external CLI tools required by sfp_tool_* modules are on PATH."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# module_id -> (binary name, install hint)
CLI_TOOLS = {
    "sfp_tool_cmseek": ("cmseek", "pip install cmseek OR clone CMSeeK repo"),
    "sfp_tool_dnstwist": ("dnstwist", "pip install dnstwist"),
    "sfp_tool_nbtscan": ("nbtscan", "OS package / http://www.unixwiz.net/tools/nbtscan.html"),
    "sfp_tool_nmap": ("nmap", "https://nmap.org/download.html"),
    "sfp_tool_nuclei": ("nuclei", "https://nuclei.projectdiscovery.io/"),
    "sfp_tool_onesixtyone": ("onesixtyone", "https://github.com/trailofbits/onesixtyone"),
    "sfp_tool_retirejs": ("retire", "npm install -g retire"),
    "sfp_tool_snallygaster": ("snallygaster", "pip install snallygaster"),
    "sfp_tool_testsslsh": ("testssl.sh", "https://testssl.sh"),
    "sfp_tool_trufflehog": ("trufflehog", "https://github.com/trufflesecurity/trufflehog"),
    "sfp_tool_wafw00f": ("wafw00f", "pip install wafw00f"),
    "sfp_tool_wappalyzer": ("wappalyzer", "npm install -g wappalyzer"),
    "sfp_tool_whatweb": ("whatweb", "gem install whatweb OR OS package"),
}


def ensure_venv_scripts_on_path() -> None:
    venv_scripts = REPO_ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin")
    if venv_scripts.is_dir():
        prefix = str(venv_scripts) + os.pathsep
        if not os.environ.get("PATH", "").startswith(prefix):
            os.environ["PATH"] = prefix + os.environ.get("PATH", "")


def _resolve_binary(name: str) -> str | None:
    found = shutil.which(name) or shutil.which(f"{name}.exe")
    if found:
        return found
    if sys.platform == "win32":
        for folder in os.environ.get("PATH", "").split(os.pathsep):
            for candidate_name in (name, f"{name}.exe"):
                candidate = os.path.join(folder, candidate_name)
                if os.path.isfile(candidate):
                    return candidate
    return None


def probe() -> list[dict]:
    rows = []
    for module_id, (binary, hint) in sorted(CLI_TOOLS.items()):
        found = _resolve_binary(binary)
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
    ensure_venv_scripts_on_path()
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
