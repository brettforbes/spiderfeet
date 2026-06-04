"""Shared API test fixtures."""

import pytest
from fastapi.testclient import TestClient

from spiderfeet.api.app import create_app
from spiderfeet.api import bootstrap


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    bootstrap._runtime = None
    with TestClient(create_app()) as client:
        yield client
