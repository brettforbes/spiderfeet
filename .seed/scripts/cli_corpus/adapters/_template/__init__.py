"""Adapter template - copy to adapters/<tool>/ and implement.

Public contract (SPEC-004 / proj-07):
- CAPTURE_FAMILY: "structured_native" | "text_native"
- to_structured(...)
- to_text(...)
- to_graph(...)
- to_narrative(...)
"""

CAPTURE_FAMILY = "structured_native"


def to_structured(*_args, **_kwargs):
    raise NotImplementedError


def to_text(*_args, **_kwargs):
    raise NotImplementedError


def to_graph(*_args, **_kwargs):
    raise NotImplementedError


def to_narrative(*_args, **_kwargs):
    raise NotImplementedError
