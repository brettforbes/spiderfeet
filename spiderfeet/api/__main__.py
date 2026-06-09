"""Run API with: poetry run python -m spiderfeet.api"""

import multiprocessing as mp

import uvicorn

from spiderfeet.api import settings
from spiderfeet.api.app import create_app

if __name__ == "__main__":
    mp.freeze_support()
    uvicorn.run(
        "spiderfeet.api.app:create_app",
        factory=True,
        host=settings.DEFAULT_HOST,
        port=settings.DEFAULT_PORT,
        reload=False,
    )
