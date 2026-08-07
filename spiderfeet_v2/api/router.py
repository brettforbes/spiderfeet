"""Aggregate v2 routers for mounting on spiderfeet.api (dual-stack)."""

from __future__ import annotations

from fastapi import APIRouter

from spiderfeet_v2.api.routes import (
    contexts,
    execute,
    projects,
    scan_steps,
    targets,
    workflows,
)

v2_router = APIRouter()
v2_router.include_router(targets.router)
v2_router.include_router(workflows.router)
v2_router.include_router(projects.router)
v2_router.include_router(scan_steps.router)
v2_router.include_router(contexts.router)
v2_router.include_router(execute.router)
