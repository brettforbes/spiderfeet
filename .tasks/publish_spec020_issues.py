"""Publish SPEC-020 issue bodies, links, sub-issues, and project fields.

Idempotency key: exact issue title in the target repository.
GitHub operations are performed exclusively through the ``gh`` CLI.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / ".governance" / "project"
INDEX = GOV / "SPEC020_ISSUE_INDEX.md"


@dataclass(frozen=True)
class IssueSpec:
    code: str
    repo: str
    parent: str | None
    deps: tuple[str, ...]
    priority: str
    size: str
    labels: tuple[str, ...]
    source: Path


def run(*args: str, json_output: bool = False, allow_failure: bool = False) -> Any:
    command = ["gh", *args]
    result = subprocess.run(command, text=True, capture_output=True, encoding="utf-8")
    if result.returncode and not allow_failure:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    if json_output:
        return json.loads(result.stdout or "{}")
    return result


def story(
    code: str,
    repo: str,
    parent: str | None,
    deps: tuple[str, ...],
    priority: str,
    size: str,
    labels: tuple[str, ...],
    source: str,
) -> IssueSpec:
    return IssueSpec(
        code=code,
        repo=repo,
        parent=parent,
        deps=deps,
        priority=priority,
        size=size,
        labels=labels,
        source=GOV / "spec020_issue_bodies" / source,
    )


SPECS = [
    story("G0", "brettforbes/spiderfeet", None, (), "P0", "S", ("story", "documentation"), "backend.md"),
    story("Epic A", "brettforbes/spiderfeet", None, (), "P0", "L", ("epic", "infrastructure"), "backend.md"),
    story("A1", "brettforbes/spiderfeet", "Epic A", (), "P0", "M", ("story", "infrastructure"), "backend.md"),
    story("A2", "brettforbes/spiderfeet", "Epic A", ("A1",), "P0", "M", ("story", "backend"), "backend.md"),
    story("A3", "brettforbes/spiderfeet", "Epic A", ("A2",), "P0", "M", ("story", "backend"), "backend.md"),
    story("Epic B", "brettforbes/spiderfeet", None, (), "P0", "XL", ("epic", "backend"), "backend.md"),
    story("B1", "brettforbes/spiderfeet", "Epic B", (), "P0", "M", ("story", "backend"), "backend.md"),
    story("B2", "brettforbes/spiderfeet", "Epic B", ("B1",), "P0", "L", ("story", "backend"), "backend.md"),
    story("B3", "brettforbes/spiderfeet", "Epic B", ("B1",), "P0", "L", ("story", "backend"), "backend.md"),
    story("B4", "brettforbes/spiderfeet", "Epic B", ("B3",), "P0", "L", ("story", "backend", "testing"), "backend.md"),
    story("B5", "brettforbes/spiderfeet", "Epic B", ("A3", "B4"), "P0", "M", ("story", "backend"), "backend.md"),
    story("Epic C", "brettforbes/spiderfeet", None, (), "P0", "XL", ("epic", "backend"), "backend.md"),
    story("C1", "brettforbes/spiderfeet", "Epic C", (), "P0", "L", ("story", "backend"), "backend.md"),
    story("C2", "brettforbes/spiderfeet", "Epic C", ("C1",), "P1", "M", ("story", "backend"), "backend.md"),
    story("C3", "brettforbes/spiderfeet", "Epic C", ("B1", "C1", "C2"), "P0", "L", ("story", "backend"), "backend.md"),
    story("C4", "brettforbes/spiderfeet", "Epic C", ("C3",), "P0", "L", ("story", "backend"), "backend.md"),
    story("Epic D", "brettforbes/spiderfeet", None, (), "P0", "XL", ("epic", "backend"), "backend.md"),
    story("D1", "brettforbes/spiderfeet", "Epic D", ("B1", "C1"), "P0", "M", ("story", "backend"), "backend.md"),
    story("D2", "brettforbes/spiderfeet", "Epic D", ("A2", "B2", "B3", "C4", "D1"), "P0", "XL", ("story", "backend"), "backend.md"),
    story("D3", "brettforbes/spiderfeet", "Epic D", ("D2",), "P0", "L", ("story", "backend"), "backend.md"),
    story("D4", "brettforbes/spiderfeet", "Epic D", ("D2", "C4"), "P0", "L", ("story", "backend"), "backend.md"),
    story("D5", "brettforbes/spiderfeet", "Epic D", ("D2", "D3", "D4", "C4"), "P0", "L", ("story", "backend"), "backend.md"),
    story("D6", "brettforbes/spiderfeet", "Epic D", ("C3", "C4", "D2"), "P0", "L", ("story", "backend"), "backend.md"),
    story("Epic E", "brettforbes/spiderfeet", None, (), "P0", "L", ("epic", "testing"), "backend.md"),
    story("E1", "brettforbes/spiderfeet", "Epic E", ("D1", "D2"), "P0", "M", ("story", "testing"), "backend.md"),
    story("E2", "brettforbes/spiderfeet", "Epic E", ("B5", "C4", "D3", "E1"), "P0", "L", ("story", "testing"), "backend.md"),
    story("E3", "brettforbes/spiderfeet", "Epic E", ("D4", "D5", "D6", "E1"), "P0", "L", ("story", "testing"), "backend.md"),
    story("E4", "brettforbes/spiderfeet", "Epic E", ("I2",), "P1", "S", ("story", "documentation"), "backend.md"),
    story("Epic I", "brettforbes/spiderfeet", None, (), "P0", "L", ("epic", "integration"), "backend.md"),
    story("I1", "brettforbes/spiderfeet", "Epic I", ("D1", "D2", "D3", "D4", "D5", "D6", "W7", "H4"), "P0", "M", ("story", "integration", "testing"), "backend.md"),
    story("I2", "brettforbes/spiderfeet", "Epic I", ("E2", "E3", "I1"), "P0", "L", ("story", "integration", "testing"), "backend.md"),
    story("I3", "brettforbes/spiderfeet", "Epic I", ("I2", "E4"), "P0", "M", ("story", "operator-gate", "testing"), "backend.md"),
    story("Epic W", "brettforbes/widget-context-gorules", None, (), "P0", "XL", ("epic", "frontend"), "context_widget.md"),
    story("W0", "brettforbes/widget-context-gorules", "Epic W", (), "P0", "M", ("story", "infrastructure", "documentation"), "context_widget.md"),
    story("W1", "brettforbes/widget-context-gorules", "Epic W", ("W0",), "P0", "L", ("story", "frontend"), "context_widget.md"),
    story("W2", "brettforbes/widget-context-gorules", "Epic W", ("W1",), "P0", "M", ("story", "frontend", "integration"), "context_widget.md"),
    story("W3", "brettforbes/widget-context-gorules", "Epic W", ("W2", "A3"), "P0", "L", ("story", "frontend"), "context_widget.md"),
    story("W4", "brettforbes/widget-context-gorules", "Epic W", ("W2", "D2"), "P0", "L", ("story", "frontend"), "context_widget.md"),
    story("W5", "brettforbes/widget-context-gorules", "Epic W", ("W4", "D6"), "P0", "L", ("story", "frontend"), "context_widget.md"),
    story("W6", "brettforbes/widget-context-gorules", "Epic W", ("W3", "W4", "W5", "D4", "D5", "D6"), "P0", "L", ("story", "frontend"), "context_widget.md"),
    story("W7", "brettforbes/widget-context-gorules", "Epic W", ("W3", "W4", "W5", "W6"), "P0", "M", ("story", "frontend", "testing"), "context_widget.md"),
    story("Epic H", "brettforbes/spiderfeet-widget", None, (), "P0", "L", ("epic", "frontend", "integration"), "host_widget.md"),
    story("H1", "brettforbes/spiderfeet-widget", "Epic H", ("W2",), "P0", "M", ("story", "frontend", "integration"), "host_widget.md"),
    story("H2", "brettforbes/spiderfeet-widget", "Epic H", ("H1", "D1", "D2", "D3"), "P0", "M", ("story", "frontend"), "host_widget.md"),
    story("H3", "brettforbes/spiderfeet-widget", "Epic H", ("H1", "H2", "W4", "W5", "W6"), "P0", "L", ("story", "frontend", "integration"), "host_widget.md"),
    story("H4", "brettforbes/spiderfeet-widget", "Epic H", ("H1", "H2", "H3", "W7"), "P0", "M", ("story", "frontend", "testing"), "host_widget.md"),
]


LABELS = {
    "spec-020": ("1D76DB", "SPEC-020 GoRules Project Context"),
    "epic": ("5319E7", "Parent epic"),
    "story": ("0E8A16", "Implementation story"),
    "feature": ("A2EEEF", "Feature work"),
    "infrastructure": ("D4C5F9", "Infrastructure and local platform"),
    "backend": ("0052CC", "Backend and API"),
    "frontend": ("C2E0C6", "Frontend and iframe"),
    "integration": ("FEF2C0", "Cross-component integration"),
    "testing": ("BFDADC", "Testing and evidence"),
    "documentation": ("0075CA", "Documentation"),
    "blocked": ("D73A4A", "Blocked with evidence"),
    "operator-gate": ("FBCA04", "Requires operator execution or approval"),
}


def sections(path: Path) -> dict[str, tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(
        re.finditer(
            r"^## (?P<code>Epic [A-Z]|[A-Z]\d+) — (?P<title>.+)$",
            text,
            flags=re.MULTILINE,
        )
    )
    result: dict[str, tuple[str, str]] = {}
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        result[match.group("code")] = (match.group("title").strip(), body)
    return result


def ensure_labels(repos: set[str]) -> None:
    required = {"spec-020", "epic", "story", "feature"}
    required.update(label for spec in SPECS for label in spec.labels)
    for repo in sorted(repos):
        for name in sorted(required):
            color, description = LABELS[name]
            run(
                "label",
                "create",
                name,
                "--repo",
                repo,
                "--color",
                color,
                "--description",
                description,
                "--force",
            )


def existing_by_title(repo: str) -> dict[str, dict[str, Any]]:
    data = run(
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "all",
        "--search",
        "SPEC-020 in:title",
        "--limit",
        "100",
        "--json",
        "number,title,url,id,state",
        json_output=True,
    )
    return {item["title"]: item for item in data}


def spec_title(code: str, title: str) -> str:
    return f"[SPEC-020][{code}] {title}"


def repo_link(path: str) -> str:
    return f"https://github.com/brettforbes/spiderfeet/blob/develop/{path}"


def create_issues() -> dict[str, dict[str, Any]]:
    parsed: dict[Path, dict[str, tuple[str, str]]] = {}
    existing = {repo: existing_by_title(repo) for repo in {s.repo for s in SPECS}}
    issue_map: dict[str, dict[str, Any]] = {}
    for spec in SPECS:
        parsed.setdefault(spec.source, sections(spec.source))
        title_text, body = parsed[spec.source][spec.code]
        title = spec_title(spec.code, title_text)
        found = existing[spec.repo].get(title)
        if found is None:
            header = (
                f"> [SPEC-020]({repo_link('.governance/specs/SPEC-020-gorules-project-context.md')})"
                f" · [Agent plan]({repo_link('.governance/project/SPEC020_AGENT_PLAN.md')})"
                f" · [Issue index]({repo_link('.governance/project/SPEC020_ISSUE_INDEX.md')})\n\n"
            )
            labels = ("spec-020", "feature", *spec.labels)
            output = run(
                "issue",
                "create",
                "--repo",
                spec.repo,
                "--title",
                title,
                "--body",
                header + body,
                *sum((["--label", label] for label in labels), []),
            )
            url = output.stdout.strip()
            number = int(url.rsplit("/", 1)[1])
            found = run(
                "issue",
                "view",
                str(number),
                "--repo",
                spec.repo,
                "--json",
                "number,title,url,id,state",
                json_output=True,
            )
            print(f"created {spec.code}: {found['url']}", flush=True)
        else:
            print(f"reused {spec.code}: {found['url']}", flush=True)
        issue_map[spec.code] = {**found, "repo": spec.repo}
    return issue_map


def tracking_block(spec: IssueSpec, issue_map: dict[str, dict[str, Any]]) -> str:
    lines = ["## Tracking"]
    if spec.parent:
        parent = issue_map[spec.parent]
        lines.append(f"- Parent: [{spec.parent}]({parent['url']})")
    if spec.deps:
        linked = ", ".join(f"[{code}]({issue_map[code]['url']})" for code in spec.deps)
        lines.append(f"- Depends on: {linked}")
    else:
        lines.append("- Depends on: none")
    lines.extend(
        [
            f"- Priority: `{spec.priority}`",
            f"- Size: `{spec.size}`",
            "- Initial board state: `In progress`"
            if spec.code == "G0"
            else "- Initial board state: `Ready`"
            if spec.code in {"W0", "A1", "B1", "C1"}
            else "- Initial board state: `Backlog`",
        ]
    )
    if spec.code in {"A1", "A2", "A3", "B5", "I2"}:
        lines.append(
            "- License boundary: live BRMS proof is blocked until a valid self-hosted "
            "GoRules `LICENSE_KEY` is supplied; mocks are not direct live proof."
        )
    return "\n".join(lines)


def update_issue_bodies(issue_map: dict[str, dict[str, Any]]) -> None:
    parsed: dict[Path, dict[str, tuple[str, str]]] = {}
    children: dict[str, list[str]] = {}
    for spec in SPECS:
        if spec.parent:
            children.setdefault(spec.parent, []).append(spec.code)
    for spec in SPECS:
        parsed.setdefault(spec.source, sections(spec.source))
        _, source_body = parsed[spec.source][spec.code]
        header = (
            f"> [SPEC-020]({repo_link('.governance/specs/SPEC-020-gorules-project-context.md')})"
            f" · [Agent plan]({repo_link('.governance/project/SPEC020_AGENT_PLAN.md')})"
            f" · [Issue index]({repo_link('.governance/project/SPEC020_ISSUE_INDEX.md')})\n\n"
        )
        blocks = [header + source_body, tracking_block(spec, issue_map)]
        if spec.code in children:
            child_lines = ["## Child stories"]
            child_lines.extend(
                f"- [{child}]({issue_map[child]['url']})" for child in children[spec.code]
            )
            blocks.append("\n".join(child_lines))
        issue = issue_map[spec.code]
        run(
            "issue",
            "edit",
            str(issue["number"]),
            "--repo",
            spec.repo,
            "--body",
            "\n\n".join(blocks) + "\n",
        )


def add_subissues(issue_map: dict[str, dict[str, Any]]) -> None:
    for spec in SPECS:
        if not spec.parent:
            continue
        result = run(
            "api",
            "graphql",
            "-f",
            "query=mutation($issueId: ID!, $subIssueId: ID!) { "
            "addSubIssue(input: {issueId: $issueId, subIssueId: $subIssueId}) "
            "{ issue { id } subIssue { id } } }",
            "-f",
            f"issueId={issue_map[spec.parent]['id']}",
            "-f",
            f"subIssueId={issue_map[spec.code]['id']}",
            allow_failure=True,
        )
        if result.returncode:
            # A rerun may report an already-parented issue. Body links remain authoritative.
            print(
                f"warning: sub-issue link {spec.parent} -> {spec.code}: "
                f"{result.stderr.strip()}",
                file=sys.stderr,
                flush=True,
            )


def project_metadata() -> tuple[str, dict[str, tuple[str, dict[str, str]]]]:
    projects = run(
        "project", "list", "--owner", "brettforbes", "--format", "json", json_output=True
    )
    project = next(p for p in projects["projects"] if p["number"] == 1)
    fields = run(
        "project",
        "field-list",
        "1",
        "--owner",
        "brettforbes",
        "--format",
        "json",
        json_output=True,
    )
    selected: dict[str, tuple[str, dict[str, str]]] = {}
    for field in fields["fields"]:
        if field["name"] in {"VibeGov Status", "Priority", "Size"}:
            selected[field["name"]] = (
                field["id"],
                {option["name"]: option["id"] for option in field["options"]},
            )
    return project["id"], selected


def add_to_project(issue_map: dict[str, dict[str, Any]]) -> None:
    project_id, fields = project_metadata()
    for spec in SPECS:
        issue = issue_map[spec.code]
        added = run(
            "project",
            "item-add",
            "1",
            "--owner",
            "brettforbes",
            "--url",
            issue["url"],
            "--format",
            "json",
            json_output=True,
        )
        item_id = added["id"]
        values = {
            "VibeGov Status": "In progress"
            if spec.code == "G0"
            else "Ready"
            if spec.code in {"W0", "A1", "B1", "C1"}
            else "Backlog",
            "Priority": spec.priority,
            "Size": spec.size,
        }
        for name, value in values.items():
            field_id, options = fields[name]
            run(
                "project",
                "item-edit",
                "--id",
                item_id,
                "--project-id",
                project_id,
                "--field-id",
                field_id,
                "--single-select-option-id",
                options[value],
            )
        print(f"board {spec.code}: {values['VibeGov Status']}", flush=True)


def update_local_index(issue_map: dict[str, dict[str, Any]]) -> None:
    text = INDEX.read_text(encoding="utf-8")
    for spec in SPECS:
        issue = issue_map[spec.code]
        link = f"[#{issue['number']}]({issue['url']})"
        pattern = re.compile(
            rf"^(\| {re.escape(spec.code)}(?: — [^|]+)? \|) TBD (\|)",
            flags=re.MULTILINE,
        )
        text, count = pattern.subn(rf"\1 {link} \2", text, count=1)
        if count == 0 and link in text:
            count = 1
        if count != 1:
            raise RuntimeError(f"Could not replace one index row for {spec.code}")
    text = re.sub(
        r"^(\| (?:Epic [A-Z]|[A-Z]\d+)(?: — [^|]+)? "
        r"\| \[#\d+\]\([^)]+\) \| [^|]+ \| [^|]+ \|) planned (\|)$",
        r"\1 open \2",
        text,
        flags=re.MULTILINE,
    )
    text = text.replace(
        "> Publication status: issue bodies are complete, but GitHub issue creation is pending execution-mode approval. Replace `TBD` with issue links immediately after publication.",
        "> Publication status: all SPEC-020 epics and stories are published and linked. Board state is authoritative for execution status.",
    )
    INDEX.write_text(text, encoding="utf-8")


def comment_epics(issue_map: dict[str, dict[str, Any]]) -> None:
    message = (
        "SPEC-020 planning is published. The spec, dependency-ordered agent plan, "
        "child stories, and board fields are linked in this epic. Do not start "
        "dependent stories early. Production operands are Temporary Subgraph Viewer "
        "IDs resolved by FastAPI; golden files are test/development fixtures only."
    )
    for spec in SPECS:
        if not spec.code.startswith("Epic "):
            continue
        issue = issue_map[spec.code]
        run(
            "issue",
            "comment",
            str(issue["number"]),
            "--repo",
            spec.repo,
            "--body",
            message,
        )


def main() -> None:
    if len(SPECS) != 46:
        raise RuntimeError(f"Expected 46 issues, found {len(SPECS)}")
    if "--finalize" in sys.argv:
        issue_map = create_issues()
        update_local_index(issue_map)
        comment_epics(issue_map)
        print(json.dumps(issue_map, indent=2), flush=True)
        return
    if "--local-only" in sys.argv:
        issue_map = create_issues()
        update_local_index(issue_map)
        return
    ensure_labels({spec.repo for spec in SPECS})
    issue_map = create_issues()
    update_issue_bodies(issue_map)
    add_subissues(issue_map)
    add_to_project(issue_map)
    update_local_index(issue_map)
    comment_epics(issue_map)
    print(json.dumps(issue_map, indent=2), flush=True)


if __name__ == "__main__":
    main()
