"""HTTP / in-process API client for the acceptance harness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol
from urllib.parse import urljoin

import httpx


class AcceptanceApi(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response: ...

    def close(self) -> None: ...


@dataclass
class HttpxApi:
    """Talk to a running v2 API (default ``http://127.0.0.1:8001/api/v1``)."""

    base_url: str
    timeout: float = 600.0
    _client: Optional[httpx.Client] = None

    def __post_init__(self) -> None:
        base = self.base_url.rstrip("/") + "/"
        self.base_url = base
        self._client = httpx.Client(base_url=base, timeout=self.timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        assert self._client is not None
        rel = path.lstrip("/")
        return self._client.request(method, rel, json=json, params=params)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None


@dataclass
class InProcessApi:
    """FastAPI TestClient + in-memory fakes (no TypeDB / no live server)."""

    test_client: Any
    crud: Any
    projections: Any

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        # TestClient paths are absolute from app root.
        url = path if path.startswith("/") else f"/{path}"
        if not url.startswith("/api/"):
            url = urljoin("/api/v1/", url.lstrip("/"))
        return self.test_client.request(method, url, json=json, params=params)

    def close(self) -> None:
        close = getattr(self.test_client, "close", None)
        if callable(close):
            close()
        from spiderfeet_v2.api import deps

        deps.set_crud_store(None)
        deps.set_projection_store(None)


def build_inprocess_api() -> InProcessApi:
    """Wire FakeCrudStore / FakeProjectionStore into create_app() TestClient."""
    from fastapi.testclient import TestClient

    from spiderfeet.api import bootstrap
    from spiderfeet.api.app import create_app
    from spiderfeet_v2.api import deps
    from spiderfeet_v2.api.tests.conftest import FakeCrudStore, FakeProjectionStore

    crud = FakeCrudStore()
    proj = FakeProjectionStore(crud)
    deps.set_crud_store(crud)  # type: ignore[arg-type]
    deps.set_projection_store(proj)  # type: ignore[arg-type]
    bootstrap._runtime = None
    client = TestClient(create_app())
    return InProcessApi(test_client=client, crud=crud, projections=proj)


def api_reachable(base_url: str, timeout: float = 2.0) -> bool:
    health = base_url.rstrip("/")
    if health.endswith("/api/v1"):
        health_url = health[: -len("/api/v1")] + "/api/v1/health"
    else:
        health_url = health + "/health"
    try:
        r = httpx.get(health_url, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False
