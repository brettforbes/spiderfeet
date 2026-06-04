"""FastAPI application factory."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from spiderfeet import __version__
from spiderfeet.api import settings
from spiderfeet.api.bootstrap import init_runtime
from spiderfeet.api.routes import catalogue, health, scans


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
    return app
