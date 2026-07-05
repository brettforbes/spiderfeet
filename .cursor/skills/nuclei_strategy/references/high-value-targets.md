# High-Value Chaining Targets

Template intents and attack-surface classes to prioritize in **selective** batches.

Source: `.seed/03EB_Rethinking_Nuclei_Strategy.md`

## Core template intents

| # | Intent |
|---|--------|
| 1 | Is admin panel accessible without login? |
| 2 | Can I read sensitive files? |
| 3 | Is there SQL injection in login form? |

## Stack follow-ups

| Signal | Follow-up |
|--------|-----------|
| WordPress | Run `-tags wordpress`; add templates from [nuclei-wordfence-cve](https://github.com/topscoder/nuclei-wordfence-cve) in addition to official WordPress templates |
| Apache / Joomla / Atlassian | Run matching stack tags after fingerprint |

## Exposure and misconfiguration classes

- Postman collections — public links or exported files
- GitHub leaks — `.env`, `.http`, API keys in public repos
- Swagger / OpenAPI — `/swagger.json`, `/openapi.json`
- Exposed admin panels
- Open metrics endpoints
- Debug endpoints
- Unauthenticated APIs
- Forgotten staging environments
- Misconfigured CORS
- Auth bypass patterns

## Mapping to Nuclei batches

| Target class | Typical tags / paths |
|--------------|----------------------|
| Admin without login | `panel`, `admin`, `exposure` |
| Sensitive files | `exposures/` path, `exposure` tag |
| SQLi on forms | `sqli`, CVE templates, API workflow SQLi subtemplates |
| WordPress CVEs | `wordpress`, `cve`, supplemental Wordfence repo |
| API surface | swagger detection → workflow (see api-pentest doc) |
| Default credentials | `default-logins/` path, `default-login` tag |

## Chainability reminder

Only add a target class to a batch if a positive hit enables a **defined next step** (deeper template set, workflow subtemplate, or manual verification).

## Related

- [scanning-principles.md](scanning-principles.md)
- [api-pentest-techniques.md](api-pentest-techniques.md)
- [selective-scan-techniques.md](selective-scan-techniques.md)
