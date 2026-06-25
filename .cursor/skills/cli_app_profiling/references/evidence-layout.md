# Evidence Layout

## Examination outputs (legacy numbered)

```
.docs/docs-for-cli-tools/app_examination_docs/<tool>/
  <n>_manifest.json
  <n>_command.txt
  <n>_output_text.txt
  <n>_output_structured.json|xml|yaml|csv   # when applicable
  <n>_review.status.json
```

`<n>` is a monotonic integer per tool directory. Pairs like `foo_xml` + `foo_text` are **one scenario** — store under `scenarios/<scenario_key>/` when consolidating.

## Scenario bundles (canonical for API + UI)

```
.docs/docs-for-cli-tools/app_examination_docs/<tool>/scenarios/<scenario_key>/
  manifest.json
  command.txt
  output_text.txt
  output_structured.{json|xml|yaml|csv}
  proposed_nuggets_edges.json
  nugget_graph_structure.md
  review.status.json
```

`scenario_key` strips suffixes such as `_text`, `_xml`, `_json`, `_jsonl`, `_parsable` from harvest `scenario_id`.

| Artifact | CLI Profiling tab |
|----------|-------------------|
| `output_text.txt` | Text |
| `output_structured.*` | Structured (Data Viewer) |
| `proposed_nuggets_edges.json` | Graph |
| `nugget_graph_structure.md` | Structure doc |

## Nugget proposals

```
.docs/docs-for-cli-tools/nugget_structure/
  <tool>_nugget_graph_structure.md
  <tool>_<n>_proposed_nuggets_edges.json
  <tool>_<n>_proposed_nuggets_edges.md
```

## Supporting artifacts

```
.docs/docs-for-cli-tools/cli_help_text/<tool>_cli_help_text.md
.strategy/<tool>_strategy.skill
.docs/docs-for-cli-tools/examination_plans/<tool>_formal_examination_plan.md
```

## Corpus tracking

Update `.docs/docs-for-cli-tools/corpus_index.json` when a tool advances phase.
