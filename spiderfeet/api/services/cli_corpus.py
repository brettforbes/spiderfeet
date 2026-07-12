"""CLI corpus evidence reader for the profiling review UI (§2.1.3)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from spiderfeet.api.bootstrap import REPO_ROOT

_CLI_DOCS = REPO_ROOT / ".docs" / "docs-for-cli-tools"
_CORPUS_INDEX = _CLI_DOCS / "corpus_index.json"
_EXAM_ROOT = _CLI_DOCS / "app_examination_docs"
_NUGGET_ROOT = _CLI_DOCS / "nugget_structure"

_TOOL_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")
_SCENARIO_KEY_RE = re.compile(r"^[a-zA-Z0-9_-]+$")
_EXAM_ID_RE = re.compile(r"^\d+$")

# Suffixes stripped to merge format-variant pairs (e.g. nmap foo_xml + foo_text → foo).
# Do not include mode suffixes such as _parsable — those are distinct scenarios.
_SCENARIO_SUFFIXES = (
    "_text",
    "_jsonl",
    "_json",
    "_xml",
    "_yaml",
    "_yml",
    "_csv",
)

_STRUCTURED_EXTS = {
    ".json": "json",
    ".jsonl": "json",
    ".xml": "xml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".csv": "csv",
}


def scenario_key_from_id(scenario_id: str) -> str:
    for suffix in _SCENARIO_SUFFIXES:
        if scenario_id.endswith(suffix):
            return scenario_id[: -len(suffix)]
    return scenario_id


def data_viewer_url() -> str:
    return os.environ.get(
        "SPIDERFEET_DATA_VIEWER_URL",
        "http://localhost:3000/widget",
    ).rstrip("/")


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _safe_tool_dir(tool_id: str) -> Path:
    if not _TOOL_ID_RE.match(tool_id):
        raise ValueError(f"Invalid tool_id: {tool_id}")
    tool_dir = (_EXAM_ROOT / tool_id).resolve()
    if not str(tool_dir).startswith(str(_EXAM_ROOT.resolve())):
        raise ValueError(f"Invalid tool path: {tool_id}")
    return tool_dir


def _safe_scenario_key(scenario_key: str) -> str:
    if not _SCENARIO_KEY_RE.match(scenario_key):
        raise ValueError(f"Invalid scenario_key: {scenario_key}")
    return scenario_key


def tool_exists(tool_id: str) -> bool:
    try:
        return _safe_tool_dir(tool_id).is_dir()
    except ValueError:
        return False


def tool_in_index(tool_id: str) -> bool:
    for entry in load_corpus_index().get("tools", []):
        if entry.get("id") == tool_id:
            return True
    return False


def load_corpus_index() -> Dict[str, Any]:
    if not _CORPUS_INDEX.is_file():
        return {"tools": [], "schema_version": 1}
    return _read_json(_CORPUS_INDEX)


def corpus_config() -> Dict[str, str]:
    return {
        "data_viewer_url": data_viewer_url(),
        "corpus_index_path": str(_CORPUS_INDEX.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def _scenario_bundle_dirs(tool_dir: Path) -> List[Path]:
    scenario_root = tool_dir / "scenarios"
    if not scenario_root.is_dir():
        return []
    return sorted(p for p in scenario_root.iterdir() if p.is_dir())


def _count_scenarios(tool_dir: Path) -> int:
    bundles = _scenario_bundle_dirs(tool_dir)
    if bundles:
        return len(bundles)
    return len(_legacy_scenario_groups(tool_dir))


def list_tools() -> List[Dict[str, Any]]:
    index = load_corpus_index()
    rows: List[Dict[str, Any]] = []
    for entry in index.get("tools", []):
        tool_id = entry.get("id")
        if not tool_id:
            continue
        tool_dir = _EXAM_ROOT / tool_id
        exam_count = _count_scenarios(tool_dir) if tool_dir.is_dir() else 0
        rows.append(
            {
                "id": tool_id,
                "phase": entry.get("phase", "pending"),
                "priority": entry.get("priority"),
                "runtime": entry.get("runtime"),
                "exam_count": exam_count,
                "has_graph_structure": _tool_graph_structure_path(tool_id).is_file(),
                "notes": entry.get("notes"),
            }
        )
    return rows


def _artifact_flags(bundle_dir: Path) -> Dict[str, bool]:
    structured = any(
        (bundle_dir / f"output_structured{ext}").is_file() for ext in _STRUCTURED_EXTS
    )
    return {
        "has_text": (bundle_dir / "output_text.txt").is_file(),
        "has_structured": structured,
        "has_graph": (bundle_dir / "proposed_nuggets_edges.json").is_file(),
        "has_markdown": (bundle_dir / "proposed_nuggets_edges_description.md").is_file(),
    }


def _graph_deferred_fields(manifest: Dict[str, Any]) -> Dict[str, Any]:
    deferred = bool(manifest.get("graph_deferred"))
    fields: Dict[str, Any] = {"graph_deferred": deferred}
    if deferred:
        fields["graph_deferred_reason"] = manifest.get("graph_deferred_reason") or ""
    return fields


def _scenario_complete(flags: Dict[str, bool], manifest: Dict[str, Any]) -> bool:
    """Text-only graph_deferred scenarios are complete when text is captured."""
    if manifest.get("graph_deferred"):
        if not flags.get("has_structured"):
            return bool(flags.get("has_text"))
        return bool(flags.get("has_text")) and bool(flags.get("has_structured"))
    return all(flags.values())


def _review_status_bundle(bundle_dir: Path, manifest: Dict[str, Any]) -> str:
    review_path = bundle_dir / "review.status.json"
    if review_path.is_file():
        try:
            body = _read_json(review_path)
            return body.get("status") or manifest.get("review_status") or "pending"
        except (json.JSONDecodeError, OSError):
            pass
    return manifest.get("review_status") or "pending"


def _structured_file_in_bundle(bundle_dir: Path) -> Optional[Path]:
    for ext in _STRUCTURED_EXTS:
        candidate = bundle_dir / f"output_structured{ext}"
        if candidate.is_file():
            return candidate
    return None


def _load_scenario_bundle(tool_id: str, bundle_dir: Path) -> Dict[str, Any]:
    manifest_path = bundle_dir / "manifest.json"
    manifest = _read_json(manifest_path) if manifest_path.is_file() else {}
    scenario_key = bundle_dir.name
    flags = _artifact_flags(bundle_dir)
    struct_path = _structured_file_in_bundle(bundle_dir)
    structured_kind = manifest.get("structured_kind")
    if struct_path and not structured_kind:
        structured_kind = _STRUCTURED_EXTS.get(struct_path.suffix.lower(), "json")

    return {
        "scenario_key": scenario_key,
        "scenario_name": manifest.get("scenario_name") or scenario_key,
        "target": manifest.get("target"),
        "runtime": manifest.get("runtime"),
        "structured_kind": structured_kind,
        "review_status": _review_status_bundle(bundle_dir, manifest),
        "legacy_exam_ids": manifest.get("legacy_exam_ids") or [],
        **flags,
        **_graph_deferred_fields(manifest),
        "complete": _scenario_complete(flags, manifest),
    }


def _legacy_scenario_groups(tool_dir: Path) -> Dict[str, List[tuple[int, Dict[str, Any]]]]:
    groups: Dict[str, List[tuple[int, Dict[str, Any]]]] = {}
    for manifest_path in sorted(tool_dir.glob("*_manifest.json")):
        exam_id = int(manifest_path.name.split("_", 1)[0])
        manifest = _read_json(manifest_path)
        sid = manifest.get("scenario_id") or f"exam_{exam_id}"
        key = scenario_key_from_id(sid)
        groups.setdefault(key, []).append((exam_id, manifest))
    return groups


def _legacy_exam_review_status(
    tool_dir: Path, exam_id: int, manifest: Dict[str, Any]
) -> str:
    review_path = tool_dir / f"{exam_id}_review.status.json"
    if review_path.is_file():
        try:
            body = _read_json(review_path)
            return body.get("status") or manifest.get("review_status") or "pending"
        except (json.JSONDecodeError, OSError):
            pass
    return manifest.get("review_status") or "pending"


def _legacy_scenario_review_status(
    tool_dir: Path, members: List[tuple[int, Dict[str, Any]]]
) -> str:
    statuses = [
        _legacy_exam_review_status(tool_dir, exam_id, manifest)
        for exam_id, manifest in members
    ]
    if not statuses:
        return "pending"
    if all(status == "approved" for status in statuses):
        return "approved"
    if any(status == "rejected" for status in statuses):
        return "rejected"
    return "pending"


def list_scenarios(tool_id: str) -> List[Dict[str, Any]]:
    tool_dir = _safe_tool_dir(tool_id)
    if not tool_dir.is_dir():
        return []

    bundles = _scenario_bundle_dirs(tool_dir)
    if bundles:
        rows = [_load_scenario_bundle(tool_id, bundle_dir) for bundle_dir in bundles]
        rows.sort(key=lambda r: r["scenario_key"])
        return rows

    rows: List[Dict[str, Any]] = []
    for key, members in sorted(_legacy_scenario_groups(tool_dir).items()):
        primary = members[0][1]
        sid = primary.get("scenario_id") or key
        has_structured = any(
            (tool_dir / f"{eid}_output_structured.json").is_file()
            or (tool_dir / f"{eid}_output_structured.xml").is_file()
            or (tool_dir / f"{eid}_output_structured.jsonl").is_file()
            for eid, _ in members
        )
        has_text = any((tool_dir / f"{eid}_output_text.txt").is_file() for eid, _ in members)
        graph_path = _resolve_graph_path(tool_id, key, sid)
        md_path = _resolve_markdown_path(tool_id, key, sid)
        flags = {
            "has_text": has_text,
            "has_structured": has_structured,
            "has_graph": graph_path.is_file(),
            "has_markdown": md_path is not None,
        }
        rows.append(
            {
                "scenario_key": key,
                "scenario_name": primary.get("scenario_name") or key,
                "target": primary.get("target"),
                "runtime": primary.get("runtime"),
                "structured_kind": primary.get("structured_kind"),
                "review_status": _legacy_scenario_review_status(tool_dir, members),
                "legacy_exam_ids": [eid for eid, _ in members],
                **flags,
                **_graph_deferred_fields(primary),
                "complete": _scenario_complete(flags, primary),
            }
        )
    return rows


def list_examinations(tool_id: str) -> List[Dict[str, Any]]:
    """Backward-compatible alias: returns scenario rows with exam_id for first legacy id."""
    rows = list_scenarios(tool_id)
    for row in rows:
        legacy = row.get("legacy_exam_ids") or []
        row["exam_id"] = legacy[0] if legacy else None
        row["scenario_id"] = row["scenario_key"]
    return rows


def _resolve_graph_path(
    tool_id: str, scenario_key: str, scenario_id: str | None = None
) -> Path:
    candidates = []
    if scenario_id:
        candidates.append(_NUGGET_ROOT / f"{tool_id}_{scenario_id}_proposed_nuggets_edges.json")
    candidates.append(_NUGGET_ROOT / f"{tool_id}_{scenario_key}_proposed_nuggets_edges.json")
    candidates.append(_NUGGET_ROOT / f"{tool_id}_proposed_nuggets_edges.json")
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def _resolve_markdown_path(
    tool_id: str, scenario_key: str, scenario_id: str | None = None
) -> Path | None:
    """Resolve narrative Markdown using the same candidate order as graph paths."""
    candidates: list[Path] = []
    if scenario_id:
        candidates.append(
            _NUGGET_ROOT / f"{tool_id}_{scenario_id}_proposed_nuggets_edges_description.md"
        )
    candidates.append(
        _NUGGET_ROOT / f"{tool_id}_{scenario_key}_proposed_nuggets_edges_description.md"
    )
    for path in candidates:
        if path.is_file():
            return path
    return None


def _graph_for_scenario(
    tool_id: str,
    scenario_key: str,
    bundle_dir: Path,
    scenario_id: str | None = None,
) -> Optional[Dict[str, Any]]:
    bundle_graph = bundle_dir / "proposed_nuggets_edges.json"
    if bundle_graph.is_file():
        return _read_json(bundle_graph)
    graph_path = _resolve_graph_path(tool_id, scenario_key, scenario_id)
    if graph_path.is_file():
        return _read_json(graph_path)
    return None


def _tool_graph_structure_path(tool_id: str) -> Path:
    return _NUGGET_ROOT / f"{tool_id}_nugget_graph_structure.md"


def get_tool_graph_structure(tool_id: str) -> Optional[Dict[str, str]]:
    _safe_tool_dir(tool_id)
    md_path = _tool_graph_structure_path(tool_id)
    if not md_path.is_file():
        return None
    return {
        "tool_id": tool_id,
        "filename": md_path.name,
        "markdown": _read_text(md_path),
    }


def _scenario_graph_description(
    tool_id: str,
    scenario_key: str,
    bundle_dir: Path,
    scenario_id: str | None = None,
) -> Optional[str]:
    bundle_md = bundle_dir / "proposed_nuggets_edges_description.md"
    if bundle_md.is_file():
        return _read_text(bundle_md)
    md_path = _resolve_markdown_path(tool_id, scenario_key, scenario_id)
    if md_path:
        return _read_text(md_path)
    return None


def get_scenario(tool_id: str, scenario_key: str) -> Optional[Dict[str, Any]]:
    _safe_scenario_key(scenario_key)
    tool_dir = _safe_tool_dir(tool_id)
    bundle_dir = tool_dir / "scenarios" / scenario_key
    if bundle_dir.is_dir():
        return _get_scenario_from_bundle(tool_id, scenario_key, bundle_dir)

    groups = _legacy_scenario_groups(tool_dir)
    if scenario_key not in groups:
        return None
    return _merge_legacy_scenario(tool_id, scenario_key, groups[scenario_key])


def _get_scenario_from_bundle(tool_id: str, scenario_key: str, bundle_dir: Path) -> Dict[str, Any]:
    manifest_path = bundle_dir / "manifest.json"
    manifest = _read_json(manifest_path) if manifest_path.is_file() else {}

    command_path = bundle_dir / "command.txt"
    text_path = bundle_dir / "output_text.txt"
    structured_path = _structured_file_in_bundle(bundle_dir)

    structured: Optional[Dict[str, Any]] = None
    if structured_path:
        ext = structured_path.suffix.lower()
        structured = {
            "format": _STRUCTURED_EXTS.get(ext, manifest.get("structured_kind") or "json"),
            "filename": structured_path.name,
            "content": _read_text(structured_path),
        }

    flags = _artifact_flags(bundle_dir)
    scenario_id = manifest.get("scenario_id") or scenario_key
    markdown = _scenario_graph_description(
        tool_id, scenario_key, bundle_dir, scenario_id
    )
    flags["has_markdown"] = markdown is not None
    return {
        "tool_id": tool_id,
        "scenario_key": scenario_key,
        "exam_id": (manifest.get("legacy_exam_ids") or [None])[0],
        "manifest": manifest,
        "review_status": _review_status_bundle(bundle_dir, manifest),
        "command": _read_text(command_path) if command_path.is_file() else "",
        "output_text": _read_text(text_path) if text_path.is_file() else "",
        "structured": structured,
        "graph_proposal": _graph_for_scenario(
            tool_id, scenario_key, bundle_dir, scenario_id
        ),
        "graph_description_markdown": markdown,
        "markdown": markdown,
        "artifacts": flags,
        **_graph_deferred_fields(manifest),
        "complete": _scenario_complete(flags, manifest),
    }


def _structured_file_legacy(tool_dir: Path, exam_id: int, manifest: Dict[str, Any]) -> Optional[Path]:
    rel = manifest.get("structured_path")
    if rel:
        candidate = (REPO_ROOT / str(rel).replace("\\", "/")).resolve()
        if candidate.is_file() and str(candidate).startswith(str(REPO_ROOT.resolve())):
            return candidate
    for ext in _STRUCTURED_EXTS:
        candidate = tool_dir / f"{exam_id}_output_structured{ext}"
        if candidate.is_file():
            return candidate
    return None


def _merge_legacy_scenario(
    tool_id: str,
    scenario_key: str,
    members: List[tuple[int, Dict[str, Any]]],
) -> Dict[str, Any]:
    tool_dir = _safe_tool_dir(tool_id)
    structured_path: Optional[Path] = None
    structured_manifest: Optional[Dict[str, Any]] = None
    text_content = ""
    command = ""
    primary_manifest = members[0][1]

    if len(members) == 1:
        exam_id, manifest = members[0]
        structured_path = _structured_file_legacy(tool_dir, exam_id, manifest)
        structured_manifest = manifest if structured_path else None
        text_path = tool_dir / f"{exam_id}_output_text.txt"
        cmd_path = tool_dir / f"{exam_id}_command.txt"
        if text_path.is_file():
            text_content = _read_text(text_path)
        if cmd_path.is_file():
            command = _read_text(cmd_path).strip()
    else:
        for exam_id, manifest in sorted(members, key=lambda m: m[0]):
            sid = manifest.get("scenario_id", "")
            struct = _structured_file_legacy(tool_dir, exam_id, manifest)
            text_path = tool_dir / f"{exam_id}_output_text.txt"
            cmd_path = tool_dir / f"{exam_id}_command.txt"

            if struct and not structured_path:
                structured_path = struct
                structured_manifest = manifest
                if cmd_path.is_file():
                    command = _read_text(cmd_path).strip()

            if text_path.is_file() and (sid.endswith("_text") or not struct):
                text_content = _read_text(text_path)
                if not command and cmd_path.is_file():
                    command = _read_text(cmd_path).strip()

        if not text_content:
            for exam_id, _ in members:
                text_path = tool_dir / f"{exam_id}_output_text.txt"
                if text_path.is_file():
                    text_content = _read_text(text_path)
                    break

    structured: Optional[Dict[str, Any]] = None
    if structured_path:
        ext = structured_path.suffix.lower()
        kind = (structured_manifest or {}).get("structured_kind")
        structured = {
            "format": kind or _STRUCTURED_EXTS.get(ext, "json"),
            "filename": structured_path.name,
            "content": _read_text(structured_path),
        }

    bundle_dir = tool_dir / "scenarios" / scenario_key
    graph = _graph_for_scenario(
        tool_id, scenario_key, bundle_dir, primary_manifest.get("scenario_id")
    )
    markdown = _scenario_graph_description(
        tool_id,
        scenario_key,
        bundle_dir,
        primary_manifest.get("scenario_id"),
    )
    flags = {
        "has_text": bool(text_content),
        "has_structured": structured is not None,
        "has_graph": graph is not None,
        "has_markdown": markdown is not None,
    }

    return {
        "tool_id": tool_id,
        "scenario_key": scenario_key,
        "exam_id": members[0][0],
        "manifest": primary_manifest,
        "review_status": primary_manifest.get("review_status") or "pending",
        "command": command,
        "output_text": text_content,
        "structured": structured,
        "graph_proposal": graph,
        "graph_description_markdown": markdown,
        "markdown": markdown,
        "artifacts": flags,
        **_graph_deferred_fields(primary_manifest),
        "complete": _scenario_complete(flags, primary_manifest),
    }


def get_examination(tool_id: str, exam_id: int) -> Optional[Dict[str, Any]]:
    """Resolve legacy exam_id to scenario_key and return merged scenario detail."""
    if not _EXAM_ID_RE.match(str(exam_id)):
        raise ValueError(f"Invalid exam_id: {exam_id}")
    tool_dir = _safe_tool_dir(tool_id)
    manifest_path = tool_dir / f"{exam_id}_manifest.json"
    if manifest_path.is_file():
        manifest = _read_json(manifest_path)
        sid = manifest.get("scenario_id") or f"exam_{exam_id}"
        return get_scenario(tool_id, scenario_key_from_id(sid))
    return None


def set_review_status(tool_id: str, scenario_key: str, status: str) -> Dict[str, Any]:
    if status not in {"pending", "approved", "rejected"}:
        raise ValueError(f"Invalid review status: {status}")
    _safe_scenario_key(scenario_key)
    tool_dir = _safe_tool_dir(tool_id)
    bundle_dir = tool_dir / "scenarios" / scenario_key

    body = {
        "status": status,
        "scenario_key": scenario_key,
        "tool": tool_id,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if bundle_dir.is_dir():
        review_path = bundle_dir / "review.status.json"
        review_path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
        manifest_path = bundle_dir / "manifest.json"
        if manifest_path.is_file():
            manifest = _read_json(manifest_path)
            manifest["review_status"] = status
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return body

    groups = _legacy_scenario_groups(tool_dir)
    if scenario_key not in groups:
        raise FileNotFoundError(f"Scenario not found: {tool_id}/{scenario_key}")

    for exam_id, _ in groups[scenario_key]:
        review_path = tool_dir / f"{exam_id}_review.status.json"
        legacy_body = {**body, "exam_id": exam_id}
        review_path.write_text(json.dumps(legacy_body, indent=2) + "\n", encoding="utf-8")
        manifest_path = tool_dir / f"{exam_id}_manifest.json"
        if manifest_path.is_file():
            manifest = _read_json(manifest_path)
            manifest["review_status"] = status
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return body


def set_review_status_by_exam(tool_id: str, exam_id: int, status: str) -> Dict[str, Any]:
    detail = get_examination(tool_id, exam_id)
    if detail is None:
        raise FileNotFoundError(f"Examination not found: {tool_id}/{exam_id}")
    return set_review_status(tool_id, detail["scenario_key"], status)
