"""Regression: v2 CLI resolution must hit .tools/ when PATH is empty (PR #1245)."""

from __future__ import annotations

from pathlib import Path

from modules_v2._base import resolve_executable
from spiderfeet.tools import cli_paths


def test_resolve_cli_binary_finds_tools_bin_layout(tmp_path, monkeypatch):
    tools_root = tmp_path / ".tools"
    tools_bin = tools_root / "bin"
    tools_bin.mkdir(parents=True)
    fake = tools_bin / "subfinder.exe"
    fake.write_bytes(b"MZ")

    monkeypatch.setattr(cli_paths, "TOOLS_ROOT", tools_root)
    monkeypatch.setattr(cli_paths, "TOOLS_BIN", tools_bin)
    monkeypatch.setattr(cli_paths, "which", lambda name: None)
    monkeypatch.delenv("SPIDERFEET_SUBFINDER", raising=False)
    monkeypatch.delenv("SUBFINDER_BIN", raising=False)
    monkeypatch.setenv("PATH", "")

    assert cli_paths.resolve_cli_binary("subfinder") == str(fake)


def test_resolve_cli_binary_finds_tools_root_file(tmp_path, monkeypatch):
    tools_root = tmp_path / ".tools"
    tools_bin = tools_root / "bin"
    tools_bin.mkdir(parents=True)
    fake = tools_root / "pius"
    fake.write_bytes(b"MZ")

    monkeypatch.setattr(cli_paths, "TOOLS_ROOT", tools_root)
    monkeypatch.setattr(cli_paths, "TOOLS_BIN", tools_bin)
    monkeypatch.setattr(cli_paths, "which", lambda name: None)
    monkeypatch.delenv("SPIDERFEET_PIUS", raising=False)
    monkeypatch.delenv("PIUS_BIN", raising=False)
    monkeypatch.setenv("PATH", "")

    assert cli_paths.resolve_cli_binary("pius") == str(fake)


def test_resolve_executable_uses_cli_paths_then_wsl(tmp_path, monkeypatch):
    tools_root = tmp_path / ".tools"
    tools_bin = tools_root / "bin"
    tools_bin.mkdir(parents=True)
    fake = tools_bin / "httpx.exe"
    fake.write_bytes(b"MZ")

    monkeypatch.setattr(cli_paths, "TOOLS_ROOT", tools_root)
    monkeypatch.setattr(cli_paths, "TOOLS_BIN", tools_bin)
    monkeypatch.setattr(cli_paths, "which", lambda name: None)
    monkeypatch.setattr("modules_v2._base.shutil.which", lambda name: None)
    monkeypatch.setattr(
        "modules_v2._base.subprocess.run",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("WSL unused when .tools hits")),
    )
    monkeypatch.delenv("SPIDERFEET_HTTPX", raising=False)
    monkeypatch.delenv("HTTPX_BIN", raising=False)
    monkeypatch.setenv("PATH", "")

    prefix, err = resolve_executable("httpx", prefer_wsl=True)
    assert err is None
    assert prefix == [str(fake)]


def test_resolve_executable_env_override(monkeypatch, tmp_path):
    fake = tmp_path / "subfinder.exe"
    fake.write_bytes(b"MZ")
    monkeypatch.setenv("SPIDERFEET_SUBFINDER", str(fake))
    monkeypatch.setattr(cli_paths, "which", lambda name: None)
    monkeypatch.setattr("modules_v2._base.shutil.which", lambda name: None)
    prefix, err = resolve_executable("subfinder", prefer_wsl=False)
    assert err is None
    assert prefix == [str(fake)]
