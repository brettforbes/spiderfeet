"""R13-09 — SPEC-013 backend pytest coverage map (smoke pointers).

Run the bound suite with::

    poetry run pytest -q \\
      spiderfeet_v2/db/tests/test_crud.py::test_project_crud_round_trip \\
      spiderfeet_v2/db/tests/test_crud.py::test_create_new_project_info_only_workflow \\
      spiderfeet_v2/db/tests/test_crud.py::test_put_workflow_yaml_reparse_replace \\
      spiderfeet_v2/api/tests/test_v2_route_coverage.py::test_put_workflow_yaml_triggers_reparse \\
      spiderfeet_v2/api/tests/test_v2_route_coverage.py::test_get_project_complete_shape \\
      spiderfeet_v2/api/tests/test_v2_routes.py::test_openapi_includes_v2_paths_and_examples \\
      spiderfeet_v2/workflow/tests/test_new_project.py \\
      spiderfeet_v2/workflow/tests/test_seed_projects.py \\
      spiderfeet_v2/workflow/tests/test_r13_coverage.py
"""

from __future__ import annotations

from spiderfeet_v2.workflow.seed_projects import SEED_SPECS, build_seed_workflow_doc
from spiderfeet_v2.workflow.loader import validate_workflow_dict


def test_r13_09_seed_smoke_docs_validate():
    """R13-09 / R13-07: all five seed workflow docs validate."""
    assert len(SEED_SPECS) == 5
    for spec in SEED_SPECS:
        doc = build_seed_workflow_doc(spec)
        validate_workflow_dict(doc)
