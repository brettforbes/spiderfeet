"""Resolve workflow ``uses`` / ``module_id`` to a ``modules_v2.sfp_cli_*`` runner."""

from __future__ import annotations

import importlib
from typing import Any, Callable, Dict, Mapping

from spiderfeet_v2.workflow.typedb_convert import module_id_for_step

RunFn = Callable[[Mapping[str, Any] | None], Dict[str, Any]]

_REGISTRY: Dict[str, RunFn] = {}


class ModuleResolveError(ValueError):
    """Unknown or unloadable v2 CLI module."""


def register_module(module_id: str, run_fn: RunFn) -> None:
    """Test / DI hook to inject a module runner."""
    _REGISTRY[module_id] = run_fn


def clear_module_registry() -> None:
    _REGISTRY.clear()


def resolve_module_id(step: Mapping[str, Any]) -> str:
    """Pick ``sfp_cli_*`` from step ``id`` / ``uses`` (AM2 helper)."""
    try:
        return module_id_for_step(dict(step))
    except Exception as exc:  # noqa: BLE001 — surface as resolve error
        raise ModuleResolveError(str(exc)) from exc


def load_module_runner(module_id: str) -> RunFn:
    """Import ``modules_v2.<module_id>`` and return its ``run`` callable."""
    if module_id in _REGISTRY:
        return _REGISTRY[module_id]
    if not module_id.startswith("sfp_cli_"):
        raise ModuleResolveError(
            f"module_id must be sfp_cli_*; got {module_id!r}"
        )
    try:
        mod = importlib.import_module(f"modules_v2.{module_id}")
    except ImportError as exc:
        raise ModuleResolveError(
            f"cannot import modules_v2.{module_id}: {exc}"
        ) from exc

    run_fn = getattr(mod, "run", None)
    if callable(run_fn):
        return run_fn  # type: ignore[return-value]

    cls = getattr(mod, module_id, None)
    if cls is not None:
        instance = cls()
        run_method = getattr(instance, "run", None)
        if callable(run_method):
            return run_method  # type: ignore[return-value]

    raise ModuleResolveError(
        f"modules_v2.{module_id} has no run() entrypoint"
    )
