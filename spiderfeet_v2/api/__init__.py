"""FastAPI v2 engine routes (SPEC-010 Epic AN).

Routers are mounted on the existing ``spiderfeet.api`` app under ``/api/v1``
(dual-stack / additive cutover). Full AN1 G2 entrypoint replacement is gated.
"""

from spiderfeet_v2.api.router import v2_router

__all__ = ["v2_router"]
