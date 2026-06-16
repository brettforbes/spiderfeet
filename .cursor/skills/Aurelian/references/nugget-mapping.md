# Aurelian Nugget Mapping

Convert Aurelian findings to SpiderFeet-style graph arrays.

## Node suggestions

- `CLOUD_ACCOUNT` (AWS account, Azure tenant/subscription, GCP project)
- `CLOUD_RESOURCE` (bucket, function, VM, database, policy object)
- `PUBLIC_EXPOSURE` (publicly accessible resource finding)
- `SECRET_EXPOSURE` (hardcoded/discovered secret evidence)
- `PRIVILEGE_ESCALATION_PATH` (IAM graph path)
- `INTERNET_NAME` (for takeover-related DNS targets)

## Edge suggestions

- `CLOUD_ACCOUNT` -> `CLOUD_RESOURCE` (`owns`)
- `CLOUD_RESOURCE` -> `PUBLIC_EXPOSURE` (`is_exposed_as`)
- `CLOUD_RESOURCE` -> `SECRET_EXPOSURE` (`contains`)
- `CLOUD_RESOURCE` -> `PRIVILEGE_ESCALATION_PATH` (`enables`)
- `INTERNET_NAME` -> `CLOUD_RESOURCE` (`resolves_to` or `targets`)

## Example arrays

```json
{
  "nodes": [
    {"id":"acct:aws:123456789012","type":"CLOUD_ACCOUNT","data":"123456789012"},
    {"id":"res:s3:my-public-bucket","type":"CLOUD_RESOURCE","data":"s3://my-public-bucket"},
    {"id":"risk:public:bucket","type":"PUBLIC_EXPOSURE","data":"public read enabled"}
  ],
  "edges": [
    {"source":"acct:aws:123456789012","target":"res:s3:my-public-bucket","type":"owns"},
    {"source":"res:s3:my-public-bucket","target":"risk:public:bucket","type":"is_exposed_as"}
  ]
}
```
