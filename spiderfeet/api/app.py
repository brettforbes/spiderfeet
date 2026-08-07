"""FastAPI application factory."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from spiderfeet import __version__
from spiderfeet.api import settings
from spiderfeet.api.bootstrap import init_runtime
from spiderfeet.api.routes import (
    catalogue,
    cli_corpus,
    content,
    health,
    map,
    scan_ui,
    scans,
    settings as settings_routes,
    subscriptions,
    tests,
)
from spiderfeet.api.schemas import (
    SCAN_CREATE_OPENAPI_EXAMPLES,
    SCAN_CREATE_SWAGGER_EXAMPLE,
    SCAN_UI_OPENAPI_EXAMPLES,
    SCAN_UI_SWAGGER_EXAMPLE,
)

logger = logging.getLogger(__name__)


def _auto_bootstrap_typedb_at_startup() -> None:
    """
    Create/seed both TypeDB databases when the server is up but a DB is missing:

    - spiderfeet-map — legacy Maps / Tests catalogue (Stage 3–4)
    - spiderfeet-actual — v2 semantic engine (SPEC-010)

    Both paths are create-if-missing / seed-if-incomplete; neither drops existing data.
    """
    try:
        from spiderfeet.map.bootstrap import ensure_map_ready
        from spiderfeet.map.config import load_connection_config
        from spiderfeet.map.connection import ping
        from spiderfeet.map.constants import MAP_DATABASE_NAME
        from spiderfeet_v2.db.bootstrap import ensure_actual_ready
        from spiderfeet_v2.db.constants import ACTUAL_DATABASE_NAME

        cfg = load_connection_config()
        if not ping(cfg):
            logger.warning(
                "TypeDB unreachable at %s; map/actual auto-bootstrap skipped",
                cfg.addresses,
            )
            return

        map_db = cfg.database or MAP_DATABASE_NAME
        if ensure_map_ready(cfg):
            logger.info("TypeDB map auto-bootstrapped (%s)", map_db)
        else:
            logger.info("TypeDB map already ready (%s)", map_db)

        if ensure_actual_ready(cfg):
            logger.info("TypeDB actual auto-bootstrapped (%s)", ACTUAL_DATABASE_NAME)
        else:
            logger.info("TypeDB actual already ready (%s)", ACTUAL_DATABASE_NAME)
    except Exception as exc:
        logger.warning("TypeDB auto-bootstrap skipped: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = init_runtime()
    _auto_bootstrap_typedb_at_startup()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="SpiderFeet API",
        description="REST API for SpiderFeet scans, catalogue data, TypeDB map + actual, and module tests (Stages 2–4 / SPEC-010).",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        swagger_ui_parameters={"tryItOutEnabled": True},
    )

    origins = list(settings.DEFAULT_CORS_ORIGINS)
    extra = os.environ.get("SPIDERFEET_CORS_ORIGINS", "")
    if extra:
        origins.extend(o.strip() for o in extra.split(",") if o.strip())

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefix = settings.API_PREFIX
    app.include_router(health.router, prefix=prefix)
    app.include_router(catalogue.router, prefix=prefix)
    app.include_router(scans.router, prefix=prefix)
    app.include_router(scan_ui.router, prefix=prefix)
    app.include_router(map.router, prefix=prefix)
    app.include_router(tests.router, prefix=prefix)
    app.include_router(subscriptions.router, prefix=prefix)
    app.include_router(settings_routes.router, prefix=prefix)
    app.include_router(cli_corpus.router, prefix=prefix)
    app.include_router(content.router, prefix=prefix)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        scan_post = (
            schema.get("paths", {})
            .get(f"{prefix}/scans", {})
            .get("post", {})
        )
        content = (
            scan_post.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
        )
        if content is not None:
            content["example"] = SCAN_CREATE_SWAGGER_EXAMPLE
            content.setdefault("examples", SCAN_CREATE_OPENAPI_EXAMPLES)
        scan_ui_post = (
            schema.get("paths", {})
            .get(f"{prefix}/scan_ui", {})
            .get("post", {})
        )
        scan_ui_content = (
            scan_ui_post.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
        )
        if scan_ui_content is not None:
            scan_ui_content["example"] = SCAN_UI_SWAGGER_EXAMPLE
            scan_ui_content.setdefault("examples", SCAN_UI_OPENAPI_EXAMPLES)
        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app
