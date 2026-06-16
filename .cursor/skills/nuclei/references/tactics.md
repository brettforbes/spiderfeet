# Nuclei Scan Tactics

Adaptive sequences to maximize useful findings while respecting authorization, rate limits, and SpiderFeet defaults.

## Principles

1. **Signal over volume** — Full template tree minus `dos,fuzz,misc` is the SpiderFeet baseline; narrow manually when noise dominates.
2. **Severity layers** — Treat `info` as technology mapping; escalate with CVE/exposure templates on confirmed stacks.
3. **Host-aware concurrency** — Reduce `-c` when targets return 429/503 or scan times spike.
4. **Template currency** — Stale templates miss new CVEs; pin versions in CI, update deliberately in ops.
5. **No OOB by default** — Interactsh findings require `-no-interactsh` removal; only on authorized isolated tests.

## Tactic 1: Broad discovery → targeted CVE

**When:** New footprint of hostnames/IPs from passive modules.

**Sequence:**

1. Run SpiderFeet module (full tree, default flags).
2. Review `WEBSERVER_TECHNOLOGY` events for stack names.
3. Manual follow-up: `nuclei -tags cve,<stack> -severity critical,high,medium -jsonl -silent`.
4. If still empty, try `-tags exposure,misconfig,panel` on confirmed HTTP services.

**If empty:** Verify HTTP/HTTPS reachable; try `-follow-redirects`; check WAF blocking.

## Tactic 2: Technology-first fingerprint

**When:** Need fast asset inventory before invasive checks.

**Sequence:**

1. `nuclei -tags tech -severity info -jsonl -silent -no-interactsh`.
2. Map to `WEBSERVER_TECHNOLOGY` equivalent.
3. Build per-stack template ID list from `-tl` grep.
4. Run `-id` comma list on high-value hosts only.

## Tactic 3: Netblock expansion hygiene

**When:** `NETBLOCK_OWNER` events expand to per-IP stdin (SpiderFeet).

**Sequence:**

1. Confirm prefix ≤ `netblockscanmax` (/24 default).
2. Pre-filter live hosts with external ping/port discovery if timeout budget tight.
3. Batch IPs (e.g. 50 per subprocess) to avoid single 240s×N timeout.
4. Deduplicate: module skips IPs inside already-scanned netblocks.

## Tactic 4: Workflow-driven depth

**When:** Single host with many services (CMS, panels, APIs).

**Sequence:**

1. `nuclei -w workflows/ -t templates/ -u URL -jsonl -silent`.
2. Workflows run subtemplates only after parent detection — fewer wasted requests.
3. Promote workflow hits to `VULNERABILITY_GENERAL` or CVE events per mapping rules.

## Tactic 5: Rate-limit and WAF evasion (authorized only)

**When:** High error rate, empty results on known live apps.

**Sequence:**

1. Drop `-c` to 25–50; add `-rate-limit 30`.
2. Enable `-follow-redirects` if landing page redirects.
3. Add realistic `-H "User-Agent: ..."` if default blocked.
4. **Do not** re-enable `dos`/`fuzz` tags without explicit approval.

## Tactic 6: Authenticated attack surface

**When:** Internal apps with credentials (authorized pentest).

**Sequence:**

1. Build `-secret-file` or `-auth` YAML per PD docs.
2. Run template subsets with `tags: auth` or app-specific folders.
3. Parse JSONL separately — not via default `sfp_tool_nuclei` (no auth config today).

## Tactic 7: CI/CD regression gate

**When:** Staging deploy validation.

**Sequence:**

1. Fixed template commit hash.
2. `nuclei -l staging-hosts.txt -severity critical,high -jsonl -silent -no-interactsh`.
3. Fail build on non-zero critical count; archive JSONL as artifact.

## Response matrix

| Observation | Next action |
|-------------|-------------|
| Many `info` tech hits, no CVEs | Run `-tags cve` + stack-specific tags |
| CVE hits on redirect URL | Note true `matched-at`; verify on canonical host |
| Timeouts | Smaller batches, lower concurrency, shorter template set |
| Duplicate CVE events | Expected if multiple matchers reference same CVE |
| `matcher-name` missing in JSONL | Upgrade Nuclei; check `-nm` not set; template may use extractors only |
| All severity `unknown` | Update templates; map to `VULNERABILITY_GENERAL` in custom parser |

## Anti-patterns

- Running full tree against entire /16 without host discovery
- Enabling Interactsh on production SpiderFeet scans
- Treating template name as CVE without regex/classification check
- Ignoring `matched-at` host re-typing for netblock scans
- Re-enabling `dos` templates against production

## Related

- [cli-options.md](cli-options.md)
- [templates-and-workflows.md](templates-and-workflows.md)
- [nugget-mapping.md](nugget-mapping.md)
