"""FastAPI application factory."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from spiderfeet import __version__
from spiderfeet.api import settings
from spiderfeet.api.bootstrap import init_runtime
from spiderfeet.api.routes import catalogue, health, scan_ui, scans
from spiderfeet.api.schemas import (
    SCAN_CREATE_OPENAPI_EXAMPLES,
    SCAN_CREATE_SWAGGER_EXAMPLE,
    SCAN_UI_OPENAPI_EXAMPLES,
    SCAN_UI_SWAGGER_EXAMPLE,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = init_runtime()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="SpiderFeet API",
        description="REST API for SpiderFeet scans and catalogue data (Stage 2).",
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
