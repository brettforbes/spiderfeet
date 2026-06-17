# Evidence Layout

## Examination outputs

```
.docs/docs-for-cli-tools/app_examination_docs/<tool>/
  <n>_manifest.json
  <n>_command.txt
  <n>_output_text.txt
  <n>_output_structured.json|xml|yaml|csv   # when applicable
  <n>_review.status.json
```

`<n>` is a monotonic integer per tool directory.

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
