# Trajan Nugget Mapping

Map Trajan findings into SpiderFeet-style graph arrays.

## Node model

Use compact, deduplicated nodes:

- `CI_CD_PLATFORM` (e.g., GitHub Actions, GitLab CI)
- `CODE_REPOSITORY` (owner/repo or project path)
- `CI_WORKFLOW_FILE` (workflow YAML path)
- `CI_PIPELINE_FINDING` (detection + severity + summary)
- `SECRET_EXPOSURE` (when finding indicates secret/token leakage)
- `PRIVILEGE_ESCALATION_PATH` (when finding indicates risky trust/permission chain)

## Edge model

- `CODE_REPOSITORY` -> `CI_WORKFLOW_FILE` (`contains_workflow`)
- `CI_WORKFLOW_FILE` -> `CI_PIPELINE_FINDING` (`triggers_finding`)
- `CI_PIPELINE_FINDING` -> `SECRET_EXPOSURE` (`indicates`) when applicable
- `CI_PIPELINE_FINDING` -> `PRIVILEGE_ESCALATION_PATH` (`enables`) when applicable

## Example nodes/edges arrays

```json
{
  "nodes": [
    {"id":"repo:owner/repo","type":"CODE_REPOSITORY","data":"owner/repo"},
    {"id":"wf:.github/workflows/release.yml","type":"CI_WORKFLOW_FILE","data":".github/workflows/release.yml"},
    {"id":"finding:abc123","type":"CI_PIPELINE_FINDING","data":"high secret exposure in release.yml"}
  ],
  "edges": [
    {"source":"repo:owner/repo","target":"wf:.github/workflows/release.yml","type":"contains_workflow"},
    {"source":"wf:.github/workflows/release.yml","target":"finding:abc123","type":"triggers_finding"}
  ]
}
```
