# Recon-ng Zero to Hero

This guide walks from first launch to a full modular domain OSINT pipeline using workspace isolation, marketplace modules, `SOURCE`-driven chaining, and export for SpiderFeet ingestion.

## 1) Install and bootstrap

1. Install Recon-ng using your approved package/source channel.
2. Launch `recon-ng` once to initialize local paths and workspace structures.
3. Confirm baseline commands: `help`, `workspaces`, `marketplace`, `modules`, `keys`, `db`.

## 2) Create engagement workspace

Example:
- `workspaces create acme-ext-2026q2`
- `workspaces select acme-ext-2026q2`

Why:
- Keeps target data isolated.
- Preserves clean chain-of-custody for reports/exports.

## 3) Configure keys and global runtime posture

1. `keys list`
2. Add provider keys needed by chosen modules.
3. Set conservative global execution options when stealth/quota control matters.

Key tactic:
- Validate key-backed modules against tiny seed sets before full input scope.

## 4) Refresh marketplace and prepare modules

1. Refresh marketplace index.
2. Search/install required modules in these families:
   - `recon/domains-hosts/*`
   - `recon/domains-contacts/*`
   - `recon/hosts-ports/*`
   - `reporting/*`
3. Load one module at a time and inspect `show info` + `show options`.

## 5) Seed with domain and run domains->hosts

1. Load a `recon/domains-hosts/*` module.
2. `options set SOURCE <target-domain>` (or file/SQL source).
3. Run module.
4. Validate `hosts` table growth using `db query`.

If no growth:
- switch to alternate domains->hosts module,
- verify SOURCE correctness,
- check dependency/key requirements.

## 6) Expand domains->contacts in parallel lane

1. Load a `recon/domains-contacts/*` module.
2. Reuse same `SOURCE` domain seed (literal/file/SQL).
3. Run and validate `contacts` table growth.

Value:
- Increases graph breadth (people/email assets) without waiting for host-port enrichment.

## 7) Chain hosts->ports from database-backed SOURCE

1. Load a `recon/hosts-ports/*` module.
2. Set `SOURCE` from workspace hosts table (SQL strategy preferred for adaptive filtering).
3. Run and validate `ports` table growth.

API spend control:
- Filter SOURCE to newly discovered hosts first.
- Avoid re-running full historical host list unless module/provider changed.

## 8) Optional vulnerability enrichment

If enabled modules provide vulnerability mappings from host/service context:
1. Validate prerequisites exist.
2. Run on bounded host/port subsets.
3. Capture vulnerability table rows for SpiderFeet `VULNERABILITY_GENERAL` mapping.

## 9) Export and reporting

1. Load `reporting/*` modules suitable for your handoff format.
2. Generate report artifacts.
3. Keep naming tied to workspace and timestamp.

Recommended:
- Export both narrative and structured data when possible.

## 10) SpiderFeet ingestion mapping

Map Recon-ng outputs into nugget graph structures:
- `domains` -> `INTERNET_NAME`
- `hosts` -> `IP_ADDRESS` / host entities
- `contacts` -> `HUMAN_NAME`, `EMAILADDR`, `PHONE_NUMBER`
- `ports` -> `TCP_PORT_OPEN` / `UDP_PORT_OPEN`
- vulnerability rows -> `VULNERABILITY_GENERAL`

Edges:
- `contains`: domain->host, host->port
- `has`: contact->email/phone, host/service->vulnerability

Output tab alignment:
- text tab: spool/report artifacts
- data tab: normalized table extracts
- graph tab: nodes/edges with deduped IDs

## 11) Automation upgrade path

After successful interactive run:
1. Capture sequence with `script record`.
2. Replay via `script execute`.
3. Convert to resource script and run with `recon-ng -r`.
4. Integrate into headless orchestration via `recon-cli`.

## 12) Troubleshooting checkpoints

- Empty outputs: validate SOURCE and prerequisite table.
- Module failure: check dependency/key markers and verbosity.
- Low yield: pivot module family or provider.
- Quota risk: reduce scope and prioritize high-yield rows.

## Worked command-family examples

- **workspaces**: create/select/list for engagement isolation.
- **marketplace**: refresh/search/install/info/remove update cycle.
- **modules**: load path-family modules by current table state.
- **options**: explicit SOURCE and module option tuning.
- **keys**: provider setup before K-marked modules.
- **db/show**: row checks and module metadata inspection.
- **reporting**: export both narrative and structured artifacts.
