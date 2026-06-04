"""Module and event-type catalogue endpoints."""

from fastapi import APIRouter, Depends

from spiderfeet import SpiderFeetDb
from spiderfeet.api.bootstrap import Runtime, get_runtime
from spiderfeet.api.schemas import EventTypeInfo, ModuleInfo

router = APIRouter(tags=["catalogue"])


def runtime_dep() -> Runtime:
    return get_runtime()


@router.get("/modules", response_model=list[ModuleInfo])
def list_modules(runtime: Runtime = Depends(runtime_dep)) -> list[ModuleInfo]:
    """List OSINT modules (CLI ``-M`` / CherryPy ``/modules`` parity)."""
    modules = runtime.config.get("__modules__") or {}
    items = []
    for name in sorted(modules.keys()):
        if "__" in name:
            continue
        items.append(
            ModuleInfo(name=name, description=modules[name].get("descr", ""))
        )
    return items


@router.get("/event-types", response_model=list[EventTypeInfo])
def list_event_types(runtime: Runtime = Depends(runtime_dep)) -> list[EventTypeInfo]:
    """List event types (CLI ``-T`` / CherryPy ``/eventtypes`` parity)."""
    dbh = SpiderFeetDb(runtime.config)
    typedata = dbh.eventTypes()
    items = [
        EventTypeInfo(name=row[1], description=row[0])
        for row in typedata
    ]
    return sorted(items, key=lambda x: x.name)
