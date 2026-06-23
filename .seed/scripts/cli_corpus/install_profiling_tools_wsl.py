#!/usr/bin/env python3
"""Install nerva/netdiscover into WSL user-local bin (run via: wsl python3 this_script.py)."""
from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

CLI_ROOT = Path.home() / ".local" / "spiderfeet-cli"
BIN = CLI_ROOT / "bin"
BIN.mkdir(parents=True, exist_ok=True)


def install_nerva() -> Path:
    dest = BIN / "nerva"
    if dest.is_file():
        return dest
    url = "https://github.com/praetorian-inc/nerva/releases/download/v1.19.1/nerva_1.19.1_linux_amd64.tar.gz"
    tgz = Path("/tmp/nerva.tgz")
    urllib.request.urlretrieve(url, tgz)
    with tarfile.open(tgz) as tf:
        tf.extractall("/tmp")
    shutil.copy("/tmp/nerva", dest)
    dest.chmod(0o755)
    return dest


def install_netdiscover() -> Path | None:
    dest = BIN / "netdiscover"
    if dest.is_file():
        return dest
    # Try extracting from Ubuntu package (no sudo).
    deb_urls = [
        "http://archive.ubuntu.com/ubuntu/pool/universe/n/netdiscover/netdiscover_0.10-1build1_amd64.deb",
        "http://archive.ubuntu.com/ubuntu/pool/universe/n/netdiscover/netdiscover_0.9-3_amd64.deb",
    ]
    tmp = Path("/tmp/nddeb")
    tmp.mkdir(parents=True, exist_ok=True)
    for url in deb_urls:
        deb = tmp / "nd.deb"
        try:
            urllib.request.urlretrieve(url, deb)
            subprocess.run(["dpkg-deb", "-x", str(deb), str(tmp / "extract")], check=True)
            built = tmp / "extract" / "usr" / "sbin" / "netdiscover"
            if built.is_file():
                shutil.copy(built, dest)
                dest.chmod(0o755)
                return dest
        except Exception as exc:  # noqa: BLE001
            print(f"netdiscover deb {url}: {exc}")
    pcap = Path("/usr/include/pcap.h")
    if not pcap.is_file() and not Path("/usr/include/pcap/pcap.h").is_file():
        print("netdiscover: skip build (libpcap headers missing)")
        return None
    src = CLI_ROOT / "netdiscover-src"
    if not (src / ".git").exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/netdiscover-scanner/netdiscover", str(src)],
            check=True,
        )
    subprocess.run(["make", "-C", str(src)], check=True)
    built = src / "src" / "netdiscover"
    shutil.copy(built, dest)
    dest.chmod(0o755)
    return dest


def main() -> None:
    nerva = install_nerva()
    print("nerva:", nerva)
    nd = install_netdiscover()
    print("netdiscover:", nd or "MISSING")


if __name__ == "__main__":
    main()
