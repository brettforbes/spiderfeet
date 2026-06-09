# SpiderFeet naming convention (post unified rebrand)

Canonical product name: **SpiderFeet** (capital F in Feet).

## Allowed lowercase `spiderfeet` (Python package path only)

- Import path: `from spiderfeet import SpiderFeetHelpers`
- On-disk package directory: `spiderfeet/` (PEP 8; required on case-insensitive Windows volumes)
- Path references in `.gitignore`, static assets, templates: `spiderfeet/static/...`

## Allowed camelCase `spiderFeet` (runtime / config identifiers)

- Logger namespaces: `logging.getLogger("spiderFeet....")`
- User data dir: `~/.spiderFeet/`
- Database filenames: `spiderFeet.db`, `spiderFeet.test.db`
- Docker image/service names where already migrated

## Disallowed legacy tokens (target: zero outside migration scripts)

- `SpiderFoot`, `Spiderfeet`, `spiderfoot` as branding or API names
- Exception: historical strings inside `.docs/analysis/apply_*.py` migration scripts only

## External URLs

- Public site host remains `spiderfeet.net` (DNS); display name is SpiderFeet
- Upstream fork links may still point at `github.com/smicallef/spiderfoot` until repo URL is updated

## Branding assets

- Logo: `.docs/branding/spiderfeet_logo_horizontal_dark.svg` (not legacy SpiderFoot)
- Do not add generated logo concept SVGs; replace only when firm/final artwork is delivered

## Vendor API strings

- GreyNoise user-agents were migrated to `greynoise-spiderFeet-*` (verify with provider if scans fail)
