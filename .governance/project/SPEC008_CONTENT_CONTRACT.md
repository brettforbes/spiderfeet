# SPEC-008 content platform contract

**Spec:** `.governance/specs/SPEC-008-cli-app-scan-ui-content-platform.md`
**Audience:** Lesser agents building/backfilling `modules_v2/content/` bundles and the `/api/v1/content/*` routes

A tool/service content bundle is **incomplete** until every row below is `Pass` or `N/A` (with reason).

## 1. Directory contract

```text
modules_v2/content/<tool_id>/
  manifest.json
  options.md
  options_schema.json
  zero_to_hero.md
  graph_structure.md
```

`tool_id` matches the id already used by `cli_corpus` / `corpus_index.json` (e.g. `nmap`, `netdiscover`, `nerva`, `pius`, `subfinder`, `httpx`, `katana`, `nuclei`). Do not invent new ids for existing tools.

| # | Requirement | Pass criteria |
|---|-------------|----------------|
| C1 | `manifest.json` | Valid JSON: `{ "tool_id", "display_name", "kind": "cli"\|"api", "category", "executable", "content_version": 1, "source_docs": { "options": "...", "zero_to_hero": "...", "graph_structure": "..." } }` |
| C2 | `options.md` | Byte-for-byte copy (or clearly dated re-export) of the tool's `.docs/docs-for-cli-tools/<Tool>-CLI-Options.md` |
| C3 | `options_schema.json` | Valid per §2 below; every flag in `options.md` has a corresponding entry or an explicit `"unmapped": true` note in the generator's review log |
| C4 | `zero_to_hero.md` | Copy of the tool's `*-Zero-to-Hero.md` |
| C5 | `graph_structure.md` | Copy or symlink-equivalent of `nugget_structure/<tool>_nugget_graph_structure.md` (SPEC-006 gold-bar output) |
| C6 | No drift | If the source `.docs/` file changes, the bundle must be regenerated (not hand-diverged) — cite the regeneration command in the PR |

## 2. `options_schema.json` format

```json
{
  "tool_id": "nmap",
  "generated_from": ".docs/docs-for-cli-tools/NMAP-CLI-Options.md",
  "generated_at": "2026-07-27T00:00:00Z",
  "groups": ["Target Specification", "Host Discovery", "Port Scanning", "Service/Version Detection", "OS Detection", "Timing and Performance", "NSE Scripts", "Output"],
  "flags": [
    {
      "id": "target",
      "flag": null,
      "aliases": [],
      "label": "Target",
      "description": "Host, IP, hostname, CIDR, or range to scan",
      "type": "string",
      "default": null,
      "required": true,
      "choices": null,
      "group": "Target Specification",
      "placeholder": "scanme.nmap.org",
      "advanced": false
    },
    {
      "id": "top_ports",
      "flag": "--top-ports",
      "aliases": [],
      "label": "Top ports",
      "description": "Scan <n> most common ports",
      "type": "integer",
      "default": 100,
      "required": false,
      "choices": null,
      "group": "Port Scanning",
      "placeholder": null,
      "advanced": false
    },
    {
      "id": "os_detection",
      "flag": "-O",
      "aliases": [],
      "label": "OS detection",
      "description": "Enable OS detection",
      "type": "boolean",
      "default": false,
      "required": false,
      "choices": null,
      "group": "OS Detection",
      "placeholder": null,
      "advanced": false
    }
  ]
}
```

| Field | Rule |
|-------|------|
| `type` | One of `string`, `boolean`, `integer`, `float`, `select`, `path` |
| `flag` | The literal CLI flag (e.g. `--top-ports`), `null` for positional args (e.g. bare target) |
| `choices` | Required (non-null array) when `type: "select"` |
| `group` | Must appear in the bundle-level `groups` array; used for Scan-tab collapsible sections |
| `required` | `true` only for flags/positionals the tool cannot run without |
| `advanced` | `true` hides the field behind an "Advanced" toggle in the Scan tab (used for flags a first-time user should not need) |

Generator implementation note: exact-fidelity parsing of arbitrary `--help` text is not always possible heuristically. The generator (`generate_options_schema.py`, R8-02/V1) should produce a best-effort draft plus a `review_log` sidecar (`options_schema.review.md`) listing any flags it could not confidently classify; a human/agent pass must resolve every entry in the review log before the bundle counts as `Pass` on C3.

## 3. API contract (R8-04)

| Route | Returns |
|-------|---------|
| `GET /api/v1/content/tools` | `{ tools: [{ tool_id, display_name, kind, category }] }` — paginated (`limit`/`offset`) once tool count exceeds ~50 |
| `GET /api/v1/content/tools/{id}` | `manifest.json` contents |
| `GET /api/v1/content/tools/{id}/options` | `{ markdown: "<options.md content>" }` |
| `GET /api/v1/content/tools/{id}/options-schema` | `options_schema.json` contents |
| `GET /api/v1/content/tools/{id}/zero-to-hero` | `{ markdown: "<zero_to_hero.md content>" }` |
| `GET /api/v1/content/tools/{id}/graph-structure` | `{ markdown: "<graph_structure.md content>" }` |

Scale requirement: these routes must not re-scan the entire `modules_v2/content/` tree on every request once the tool count grows. Use an in-memory registry keyed by `tool_id`, invalidated by directory mtime (same pattern class as `cli_corpus`'s index load, but cached — do not copy `cli_corpus`'s uncached-read-per-request pattern forward into this new surface).

## 4. Anti-patterns (reject in review)

- A `modules_v2/content/<tool>/` folder missing any of the 5 contract files
- `options_schema.json` with a flag that has no `description` (copy the raw `.md` line if nothing better exists — never leave it empty)
- Hand-edited `options_schema.json` that has drifted from `options.md` without updating both together
- Content routes that read the whole content tree from disk per request once more than a handful of tools exist
- A new tool onboarded without a content bundle (see R8-07 — this becomes a hard onboarding gate)

## 5. Verification hints

```bash
poetry run pytest .tests/test_content_routes.py -q
poetry run python .seed/scripts/cli_corpus/generate_options_schema.py --tool nmap --check
# Manual: curl http://127.0.0.1:8001/api/v1/content/tools/nmap/options-schema
```
