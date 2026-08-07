"""TypeDB client + bootstrap for spiderfeet-actual (SPEC-010)."""

from typing import Any

__all__ = ["BootstrapReport", "bootstrap_actual"]


def __getattr__(name: str) -> Any:
    if name in __all__:
        from spiderfeet_v2.db import bootstrap as _bootstrap

        return getattr(_bootstrap, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
