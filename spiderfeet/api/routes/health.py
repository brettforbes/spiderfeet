"""Health and version endpoints."""

from fastapi import APIRouter

from spiderfeet import __version__

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness check for load balancers, Requestly, and widget preflight."""
    return {
        "status": "ok",
        "service": "spiderfeet-api",
        "version": __version__,
    }
