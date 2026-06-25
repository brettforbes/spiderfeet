#!/usr/bin/env python3
"""Build .references/port_number_inventory.md from Wikipedia port list sources."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".references" / "port_number_inventory.md"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"

FETCH_CANDIDATES = [
    Path(
        r"C:\Users\brett\.cursor\projects\c-projects-spiderfeet\agent-tools\ee22c200-ffd9-4e4d-83aa-73fd28fd4fc7.txt"
    ),
    Path(
        r"C:\Users\brett\.cursor\projects\c-projects-spiderfeet\agent-tools\aca71bd1-03e0-4eea-a541-fcd82fb32c17.txt"
    ),
]
UPLOAD = Path(
    r"C:\Users\brett\.cursor\projects\c-projects-spiderfeet\uploads\List_of_TCP_and_UDP_port_numbers-0.md"
)

PORT_RE = re.compile(r"^(\d{1,5}(?:[–-]\d{1,5})?)(?:\[.*\])?$")
STATUS_WORDS = ("Yes", "No", "Unofficial", "Assigned", "Reserved", "compressible")
WIKI_LINK_RE = re.compile(r"\[([^\]]+)\]\((/wiki/[^)]+)\)")
CITE_FOOTNOTE_RE = re.compile(r"\[\\?\[\d+\\?\]\]\([^)]+\)")
PLAIN_FOOTNOTE_RE = re.compile(r"\[\d+\]")
HEADER_CELLS = {
    "port",
    "well-known ports",
    "registered ports",
    "dynamic, private or ephemeral ports",
}


def resolve_fetch() -> Path:
    for path in FETCH_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("No Wikipedia fetch snapshot found for port list")


def absolutize_wiki_links(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        label, path = m.group(1), m.group(2)
        url = "https://en.wikipedia.org" + unquote(path)
        return f"[{label}]({url})"

    return WIKI_LINK_RE.sub(repl, text)


def split_cells(line: str) -> list[str]:
    if not line.startswith("|"):
        return []
    parts = [p.strip() for p in line.strip().split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\|\s*[-:]+\s*\|", line))


def normalize_status(value: str) -> str:
    if not value:
        return ""
    for word in STATUS_WORDS:
        if value == word or value.startswith(f"{word}[") or value.startswith(f"{word}\\["):
            return word
    return value.strip()


def is_status(value: str) -> bool:
    return normalize_status(value) in STATUS_WORDS


def clean_description(text: str) -> str:
    text = CITE_FOOTNOTE_RE.sub("", text)
    text = PLAIN_FOOTNOTE_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,.")


def parse_row_cells(cells: list[str], current_port: str) -> dict[str, str] | None:
    if not cells or cells[0].lower() in HEADER_CELLS:
        return None

    port = ""
    idx = 0
    if PORT_RE.match(cells[0]):
        port = PORT_RE.match(cells[0]).group(1)
        idx = 1
    elif is_status(cells[0]) and current_port:
        port = current_port
        idx = 0
    else:
        return None

    rest = cells[idx:]
    proto = {"tcp": "", "udp": "", "sctp": "", "dccp": ""}
    desc_parts: list[str] = []
    proto_keys = ["tcp", "udp", "sctp", "dccp"]
    pi = 0
    for cell in rest:
        if pi < 4 and (is_status(cell) or cell == ""):
            if cell:
                proto[proto_keys[pi]] = normalize_status(cell)
            pi += 1
        else:
            desc_parts.append(cell)

    description = clean_description(" ".join(desc_parts))
    if not description and proto["dccp"] and not is_status(proto["dccp"]):
        description = clean_description(proto["dccp"])
        proto["dccp"] = ""

    return {
        "port": port,
        "tcp": proto["tcp"],
        "udp": proto["udp"],
        "sctp": proto["sctp"],
        "dccp": proto["dccp"],
        "observations": "",
        "description": description,
    }


def parse_table_lines(lines: list[str], linkify: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current_port = ""

    for line in lines:
        if not line.startswith("|") or is_separator(line):
            continue
        cells = split_cells(line)
        parsed = parse_row_cells(cells, current_port)
        if not parsed:
            continue
        if cells and PORT_RE.match(cells[0]):
            current_port = PORT_RE.match(cells[0]).group(1)
        if linkify:
            parsed["description"] = clean_description(absolutize_wiki_links(parsed["description"]))
        rows.append(parsed)
    return rows


def section_lines(text: str, start_marker: str, end_markers: list[str]) -> list[str]:
    start = text.find(start_marker)
    if start < 0:
        return []
    start = text.find("\n", start) + 1
    end = len(text)
    for marker in end_markers:
        pos = text.find(marker, start)
        if pos >= 0:
            end = min(end, pos)
    return text[start:end].splitlines()


def upload_table_lines(upload_text: str) -> list[str]:
    """Return only the well-known ports table rows from the saved Wikipedia HTML export."""
    lines = upload_text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("| Port") and "TCP" in line and "UDP" in line:
            start = i
            break
    return lines[start:]


def merge_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["port"], row["tcp"], row["udp"], row["sctp"])


def merge_linked(rows: list[dict[str, str]], linked: list[dict[str, str]]) -> None:
    by_key: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    by_port: dict[str, list[str]] = defaultdict(list)

    for item in linked:
        desc = item["description"]
        if not desc or "[" not in desc:
            continue
        by_key[merge_key(item)].append(desc)
        by_port[item["port"]].append(desc)

    port_cursor: dict[str, int] = defaultdict(int)

    for row in rows:
        key = merge_key(row)
        candidates = by_key.get(key, [])
        if candidates:
            row["description"] = max(candidates, key=len)
            continue

        port = row["port"]
        idx = port_cursor[port]
        port_list = by_port.get(port, [])
        if idx < len(port_list):
            row["description"] = port_list[idx]
        port_cursor[port] += 1


def esc_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def observation_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["port"], row["tcp"], row["udp"], row["description"])


def load_existing_observations(path: Path) -> dict[tuple[str, str, str, str], str]:
    """Preserve operator-filled observations when regenerating from Wikipedia."""
    if not path.exists():
        return {}
    saved: dict[tuple[str, str, str, str], str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or is_separator(line):
            continue
        cells = split_cells(line)
        if len(cells) < 5 or cells[0].lower() == "port":
            continue
        port, tcp, udp = cells[0], cells[1], cells[2]
        if not PORT_RE.match(port):
            continue
        # New format: Port | TCP | UDP | Observations | Description
        if len(cells) >= 5 and cells[3].lower() != "sctp":
            observations, description = cells[3], " | ".join(cells[4:])
        # Legacy format: Port | TCP | UDP | SCTP | DCCP | Description
        elif len(cells) >= 6:
            observations, description = "", " | ".join(cells[5:])
        else:
            continue
        if observations.strip():
            saved[(port, tcp, udp, description)] = observations.strip()
    return saved


def apply_observations(rows: list[dict[str, str]], saved: dict[tuple[str, str, str, str], str]) -> None:
    for row in rows:
        key = observation_key(row)
        if key in saved:
            row["observations"] = saved[key]


def rows_to_md(rows: list[dict[str, str]]) -> list[str]:
    out = [
        "| Port | TCP | UDP | Observations | Description |",
        "|------|-----|-----|--------------|-------------|",
    ]
    for row in rows:
        out.append(
            "| {port} | {tcp} | {udp} | {obs} | {desc} |".format(
                port=esc_cell(row["port"]),
                tcp=esc_cell(row["tcp"]),
                udp=esc_cell(row["udp"]),
                obs=esc_cell(row.get("observations", "")),
                desc=esc_cell(row["description"]),
            )
        )
    return out


def main() -> None:
    fetch_path = resolve_fetch()
    fetch_text = fetch_path.read_text(encoding="utf-8")
    upload_text = UPLOAD.read_text(encoding="utf-8") if UPLOAD.exists() else ""

    well_known = parse_table_lines(
        section_lines(fetch_text, "## Well-known ports", ["## Registered ports"])
    )
    registered = parse_table_lines(
        section_lines(
            fetch_text,
            "## Registered ports",
            ["## Dynamic, private or ephemeral ports"],
        )
    )
    dynamic = parse_table_lines(
        section_lines(fetch_text, "## Dynamic, private or ephemeral ports", ["## Note"])
    )

    if upload_text:
        linked = parse_table_lines(upload_table_lines(upload_text), linkify=True)
        for block in (well_known, registered, dynamic):
            merge_linked(block, linked)

    saved_observations = load_existing_observations(OUT)
    for block in (well_known, registered, dynamic):
        apply_observations(block, saved_observations)

    lines = [
        "# Port Number Inventory",
        "",
        f"**Source:** [{WIKI_URL}]({WIKI_URL})",
        "",
        "Comprehensive TCP/UDP port listing from Wikipedia, extended with an **Observations** column "
        "for scan-derived port/service combinations. This file is the working single source of truth "
        "until the inventory is promoted into TypeDB.",
        "",
        "Descriptions include Wikipedia article links (`https://en.wikipedia.org/wiki/...`) where the "
        "source article provides them.",
        "",
        f"**Generated from:** `{fetch_path.name}`"
        + (f" + `{UPLOAD.name}` (links)" if upload_text else ""),
        "",
        "## Observations column",
        "",
        "Record port/protocol/service combinations discovered during scanning that are not already "
        "captured in the IANA/Wikipedia description — for example an unexpected service banner on a "
        "well-known port, or a non-standard use of a registered port. Keep entries concise; one "
        "observation per cell unless multiple distinct findings warrant a semicolon-separated list.",
        "",
        "## Table legend",
        "",
        "| Cell | Meaning |",
        "|------|---------|",
        "| Yes | IANA-assigned and standardized, specified, or widely used on the port |",
        "| Unofficial | Not IANA-assigned but standardized, specified, or widely used |",
        "| Assigned | IANA-assigned but not standardized, specified, or widely used |",
        "| No | Not IANA-assigned or widely used |",
        "| Reserved | Reserved by IANA; may be available on request |",
        "",
        "---",
        "",
        "## Well-known ports (0–1023)",
        "",
        *rows_to_md(well_known),
        "",
        "---",
        "",
        "## Registered ports (1024–49151)",
        "",
        *rows_to_md(registered),
        "",
        "---",
        "",
        "## Dynamic, private or ephemeral ports (49152–65535)",
        "",
        *rows_to_md(dynamic),
        "",
        "---",
        "",
        "## External links",
        "",
        f"- [List of TCP and UDP port numbers — Wikipedia]({WIKI_URL})",
        "- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)",
        "- [RFC 6335 — Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry](https://www.rfc-editor.org/rfc/rfc6335)",
        "",
    ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    link_rows = sum(1 for r in well_known + registered + dynamic if "](https://en.wikipedia.org" in r["description"])
    print(
        f"Wrote {OUT} — well-known={len(well_known)}, "
        f"registered={len(registered)}, dynamic={len(dynamic)}, "
        f"rows_with_wiki_links={link_rows}"
    )


if __name__ == "__main__":
    main()
