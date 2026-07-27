#!/usr/bin/env python3
"""Generate options_schema.json (+ review sidecar) from *-CLI-Options.md help text."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CLI_DOCS = REPO_ROOT / ".docs" / "docs-for-cli-tools"
CONTENT_ROOT = REPO_ROOT / "modules_v2" / "content"

ADAPTER_TOOLS: dict[str, dict[str, str]] = {
    "nmap": {
        "options": "NMAP-CLI-Options.md",
        "display_name": "Nmap",
        "executable": "nmap",
    },
    "netdiscover": {
        "options": "NetDiscover-CLI-Options.md",
        "display_name": "Netdiscover",
        "executable": "netdiscover",
    },
    "nerva": {
        "options": "Nerva-CLI-Options.md",
        "display_name": "Nerva",
        "executable": "nerva",
    },
    "pius": {
        "options": "PIUS-CLI-Options.md",
        "display_name": "Pius",
        "executable": "pius",
    },
    "subfinder": {
        "options": "SubFinder-CLI-Options.md",
        "display_name": "Subfinder",
        "executable": "subfinder",
    },
    "httpx": {
        "options": "Httpx-CLI-Options.md",
        "display_name": "Httpx",
        "executable": "httpx",
    },
    "katana": {
        "options": "katana-CLI-Options.md",
        "display_name": "Katana",
        "executable": "katana",
    },
    "nuclei": {
        "options": "Nuclei-CLI-Options.md",
        "display_name": "Nuclei",
        "executable": "nuclei",
    },
}

SECTION_RE = re.compile(r"^([A-Z][A-Z0-9 /_-]{2,}):?\s*$")
VALUE_HINT_RE = re.compile(
    r"<\s*([^>]+)\s*>|"
    r"\b(string\[\]|string|int\[\]|int|integer|float|number|value|file|filename|host|portlist|port ranges)\b",
    re.I,
)
FLAG_TOKEN_RE = re.compile(r"^(-{1,2}[\w?-]+(?:,\s*-[\w?-]+)*)$")
CONTINUATION_RE = re.compile(r"^\s{4,}\S")


def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.strip().lower())
    return re.sub(r"_+", "_", s).strip("_") or "flag"


def extract_help_body(md_text: str) -> str:
    match = re.search(r"```(?:\n|\r\n?)(.*?)```", md_text, re.DOTALL)
    if match:
        return match.group(1).strip("\n")
    return md_text.strip()


def infer_type(flag_part: str, desc: str) -> str:
    joined = f"{flag_part} {desc}".lower()
    if VALUE_HINT_RE.search(flag_part):
        hint = VALUE_HINT_RE.search(flag_part)
        if hint:
            token = hint.group(0).lower()
            if "file" in token or "filename" in token or "path" in token:
                return "path"
            if "int" in token or "number" in token or "port" in token:
                return "integer"
            if "float" in token:
                return "float"
            return "string"
    if re.search(r"\b(enable|disable|do not|never|always)\b", desc.lower()) and "<" not in flag_part:
        if re.match(r"^-\w$", flag_part.split(",")[0].strip()) or flag_part.startswith("--"):
            if not VALUE_HINT_RE.search(flag_part):
                return "boolean"
    if "<" in flag_part or " string" in joined or " value" in joined:
        return "string"
    if re.match(r"^-\w$", flag_part.split(",")[0].strip()):
        return "boolean"
    return "string"


def parse_primary_flag(flag_part: str) -> tuple[str | None, list[str]]:
    tokens = [t.strip() for t in flag_part.split(",") if t.strip()]
    long_flags = [t for t in tokens if t.startswith("--")]
    short_flags = [t for t in tokens if t.startswith("-") and not t.startswith("--")]
    if long_flags:
        return long_flags[0], short_flags
    if short_flags:
        return short_flags[0], short_flags[1:]
    return None, []


def parse_flag_line(line: str, group: str, review: list[str]) -> dict[str, Any] | None:
    stripped = line.rstrip()
    if not stripped or stripped.startswith("#"):
        return None
    if SECTION_RE.match(stripped):
        return None

    # nmap style: "  -sn: Ping Scan"
    m = re.match(r"^(\s*)(.+?):\s*(.+)$", stripped)
    if m and (m.group(2).startswith("-") or m.group(2).startswith("--")):
        flag_part = m.group(2).strip()
        desc = m.group(3).strip()
    else:
        # httpx style: "   -l, -list string      description"
        parts = re.split(r"\s{2,}", stripped.strip(), maxsplit=1)
        if len(parts) < 2:
            return None
        flag_part = parts[0].strip()
        desc = parts[1].strip()
        if not flag_part.startswith("-"):
            return None

    flag_part = re.sub(r"\s+(string\[\]|string|int\[\]|int|integer|float|value|file|filename).*$", "", flag_part, flags=re.I)
    primary, aliases = parse_primary_flag(flag_part)
    if not primary:
        review.append(f"Could not parse flag token from line: {stripped}")
        return None

    field_type = infer_type(flag_part, desc)
    flag_id = _slug(primary.lstrip("-"))
    label = primary.lstrip("-").replace("-", " ").title()
    if not desc:
        desc = label
        review.append(f"Empty description for {primary}; used label as fallback")

    return {
        "id": flag_id,
        "flag": primary,
        "aliases": [a for a in aliases if a != primary],
        "label": label,
        "description": desc,
        "type": field_type,
        "default": False if field_type == "boolean" else None,
        "required": False,
        "choices": None,
        "group": group,
        "placeholder": None,
        "advanced": group not in ("Target Specification", "INPUT", "General", "General Options"),
    }


def parse_help_text(help_text: str, review: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    groups: list[str] = []
    flags: list[dict[str, Any]] = []
    current_group = "General"
    if current_group not in groups:
        groups.append(current_group)

    for raw_line in help_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if SECTION_RE.match(line.strip()):
            current_group = line.strip().rstrip(":").title()
            if current_group not in groups:
                groups.append(current_group)
            continue
        if CONTINUATION_RE.match(line) and flags:
            flags[-1]["description"] += " " + line.strip()
            continue
        entry = parse_flag_line(line, current_group, review)
        if entry:
            flags.append(entry)

    # Positional target for scanners that use {target specification}
    if "target specification" in help_text.lower() or "TARGET SPECIFICATION" in help_text:
        if not any(f["id"] == "target" for f in flags):
            groups.insert(0, "Target Specification")
            flags.insert(
                0,
                {
                    "id": "target",
                    "flag": None,
                    "aliases": [],
                    "label": "Target",
                    "description": "Host, IP, hostname, CIDR, URL, or range to scan",
                    "type": "string",
                    "default": None,
                    "required": True,
                    "choices": None,
                    "group": "Target Specification",
                    "placeholder": "scanme.nmap.org",
                    "advanced": False,
                },
            )

    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for f in flags:
        key = f["flag"] or f["id"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(f)
    return groups, deduped


def build_schema(tool_id: str, options_path: Path) -> tuple[dict[str, Any], list[str]]:
    review: list[str] = []
    md_text = options_path.read_text(encoding="utf-8")
    help_text = extract_help_body(md_text)
    groups, flags = parse_help_text(help_text, review)
    rel = options_path.relative_to(REPO_ROOT).as_posix()
    schema: dict[str, Any] = {
        "tool_id": tool_id,
        "generated_from": rel,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "groups": groups,
        "flags": flags,
    }
    return schema, review


def write_review(path: Path, tool_id: str, review: list[str]) -> None:
    lines = [f"# options_schema.review — {tool_id}", ""]
    if not review:
        lines.append("All flags parsed with confident types/descriptions.")
    else:
        lines.append("Resolve each entry before marking bundle Pass on C3:")
        lines.append("")
        for item in review:
            lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate options_schema.json from CLI options markdown")
    parser.add_argument("--tool", required=True, help="Tool id (e.g. nmap)")
    parser.add_argument(
        "--output-dir",
        help="Directory to write options_schema.json (default: modules_v2/content/<tool>/)",
    )
    parser.add_argument("--check", action="store_true", help="Validate schema shape only; exit 1 if review items remain")
    args = parser.parse_args(argv)

    tool_id = args.tool
    if tool_id not in ADAPTER_TOOLS:
        print(f"Unknown tool {tool_id!r}; known: {', '.join(sorted(ADAPTER_TOOLS))}", file=sys.stderr)
        return 2

    options_name = ADAPTER_TOOLS[tool_id]["options"]
    options_path = CLI_DOCS / options_name
    if not options_path.is_file():
        print(f"Missing options source: {options_path}", file=sys.stderr)
        return 2

    schema, review = build_schema(tool_id, options_path)
    out_dir = Path(args.output_dir) if args.output_dir else CONTENT_ROOT / tool_id
    out_dir.mkdir(parents=True, exist_ok=True)
    schema_path = out_dir / "options_schema.json"
    review_path = out_dir / "options_schema.review.md"

    schema_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    write_review(review_path, tool_id, review)
    print(f"Wrote {schema_path} ({len(schema['flags'])} flags, {len(review)} review items)")
    print(f"Wrote {review_path}")

    if args.check and review:
        return 1
    for flag in schema["flags"]:
        if not flag.get("description"):
            print(f"Flag missing description: {flag.get('id')}", file=sys.stderr)
            return 1
        if flag.get("type") == "select" and not flag.get("choices"):
            print(f"Select flag missing choices: {flag.get('id')}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
