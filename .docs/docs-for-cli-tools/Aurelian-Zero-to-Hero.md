# Aurelian Zero to Hero

Aurelian is a unified multi-cloud reconnaissance framework for AWS, Azure, and GCP.

## 1) Install

```bash
git clone https://github.com/praetorian-inc/aurelian.git
cd aurelian
go build -o aurelian main.go
```

## 2) First commands

```bash
aurelian aws recon whoami
aurelian list-modules
```

## 3) Core recon modules

```bash
aurelian aws recon public-resources
aurelian aws recon find-secrets
aurelian aws recon subdomain-takeover
```

Azure/GCP equivalents:

```bash
aurelian azure recon public-resources --subscription-id <id>
aurelian gcp recon find-secrets --project-id <id>
```

## 4) IAM path analysis (AWS)

```bash
aurelian aws recon graph --neo4j-uri bolt://localhost:7687
aurelian aws analyze analyze-iam-permissions --gaad-file gaad.json
```

## 5) Practical workflow

1. identity check
2. public exposure scan
3. secrets discovery
4. IAM path analysis
5. takeover checks

## 6) Convert to SpiderFeet nuggets

Build `nodes` and `edges` arrays from module output:
- nodes: cloud account/project, resources, exposures, secrets, IAM paths
- edges: ownership, exposure relationship, privilege path relationship

## 7) Common pitfalls

- skipping permissions validation and misreading empty output as clean
- running too broad before validating one account/project parser path
- sharing findings without redacting cloud identifiers and secret artifacts
