"""Regression: v2 CLI modules resolve binaries from .tools/ when not on PATH."""

from __future__ import annotations

from pathlib import Path

from modules_v2._base import resolve_executable

_REPO = Path(__file__).resolve().parents[1]
_TOOLS_BIN = _REPO / ".tools" / "bin"


def test_resolve_executable_finds_repo_tools_bin_when_present(monkeypatch):
    monkeypatch.setattr("modules_v2._base.shutil.which", lambda name: None)
    # Avoid slow/flaky WSL probes in unit context.
    monkeypatch.setattr(
        "modules_v2._base.subprocess.run",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("WSL should not be needed")),
    )

    expected = {
        "subfinder": _TOOLS_BIN / "subfinder.exe",
        "httpx": _TOOLS_BIN / "httpx.exe",
        "katana": _TOOLS_BIN / "katana.exe",
        "nuclei": _TOOLS_BIN / "nuclei.exe",
        "nerva": _TOOLS_BIN / "nerva.exe",
        "pius": _REPO / ".tools" / "pius",
    }
    for name, path in expected.items():
        if not path.is_file():
            continue
        prefix, err = resolve_executable(name, prefer_wsl=True)
        assert err is None, name
        assert prefix == [str(path)], (name, prefix)


def test_resolve_executable_env_override(monkeypatch, tmp_path):
    fake = tmp_path / "subfinder.exe"
    fake.write_bytes(b"MZ")
    monkeypatch.setenv("SPIDERFEET_SUBFINDER", str(fake))
    monkeypatch.setattr("modules_v2._base.shutil.which", lambda name: None)
    prefix, err = resolve_executable("subfinder", prefer_wsl=False)
    assert err is None
    assert prefix == [str(fake)]
