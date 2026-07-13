"""SpiderFeet CLI Workflow DSL runtime (SPEC-007).

Canonical docs:
  .seed/12A_Workflow_YAML_Example.yaml
  .seed/12B_Workflow_DSL_Description.md
  .seed/12C_Graph_Select_Language.md
"""

from .core.gse_eval import eval_binding, eval_select
from .core.loader import load_workflow, validate_workflow_dict
from .core.context_export import merge_graph

__all__ = [
    "eval_binding",
    "eval_select",
    "load_workflow",
    "validate_workflow_dict",
    "merge_graph",
]
