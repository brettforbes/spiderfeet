# Generalization assessment

Can SpiderFeet’s “conversion to types” be **generic and extensible**, or is it **inherently per-module**?

## Short answer

**Both.** The *vocabulary* and *event bus* are generic. The *parsers* are almost entirely module-specific today. A strong platform layer can wrap the repetitive 80% without removing module-specific edge cases.

## What is already generic

| Layer | Generic? | Notes |
|-------|----------|-------|
| `SpiderFeetEvent` + `notifyListeners` | Yes | Universal emit contract |
| `producedEvents` / `watchedEvents` | Yes | Declarative routing |
| `nuggets.json` type registry | Yes | 172 archetypes, ENTITY/DESCRIPTOR/DATA |
| `sflib` validators (`validIP`, `isDomain`, …) | Partial | Reused widely; not a parser framework |
| `helpers` extractors (email, phone, hash, …) | Partial | 3 modules flagged `content_extract`; more use helpers ad hoc |
| `sf.cveInfo()` | Yes | Maps CVE id → severity tier + text |
| Map routes (`osint_services.json`) | Yes | consumed → produced contract for tests |
| TypeDB archetype entities | Yes | One entity subtype per nugget id |

## What is module-specific (today)

| Concern | Why bespoke |
|---------|-------------|
| API response shape | Every vendor JSON differs |
| CLI stdout format | nmap text vs nuclei JSON-lines vs testssl tables |
| Field → nugget mapping | Shodan `rec['data'][].port` vs Censys certificates vs … |
| `data` string formatting | `ip:port` vs free text vs `str(dict)` |
| Confidence / risk tuning | Per-module judgement |
| Affiliate vs owned variants | `INTERNET_NAME` vs `AFFILIATE_INTERNET_NAME` rules |
| Error handling / rate limits | Per API |

**231 modules × custom `handleEvent` bodies** — static analysis shows **112** `api_json_map`, **13** `cli_subprocess_parse`, but each still hand-codes field paths.

## Can we genericise?

### High leverage (recommended)

1. **Declarative JSON mappers** — For stable APIs, YAML/JSON spec: `jsonpath` → `(nugget_type, data_template)`. Covers ~40–60% of `api_json_map` modules with similar list-walking patterns.
2. **CLI adapter interface** — `run_cli(argv) → Iterator[TypedObservation]` with pluggable `StdoutParser` (line regex, jsonl, xml). All `sfp_tool_*` share subprocess, timeout, encoding, error state.
3. **Structured payload sidecar** — Keep `data: str` for compatibility; add optional `payload: dict` on events for graph insertion (port as int, nested host).
4. **Parser registry** — Register `(module_id, output_format) → Parser` for tests and documentation auto-sync.

### Medium leverage

5. **Shared netblock expansion** — Repeated IPNetwork loop + `IP_ADDRESS` emission; already copy-pasted across 50+ modules.
6. **RAW_* normalization** — Standard JSON storage instead of `str(rec)` for re-parsing downstream.
7. **Validation at emit time** — Assert `eventType` in registry; validate `data` against per-type regex/schema.

### Low leverage / keep bespoke

- Reputation “malicious” modules (context-dependent thresholds)
- Spider/crossref (graph of links)
- Modules that only transform upstream events (`sfp_email` on page content)

## Comparison to ideal “extractor platform”

| Capability | Current | Target |
|------------|---------|--------|
| Add new nugget type | Edit `nuggets.json`, db seed, TypeQL, icons | + code generator from schema |
| Add new API module | Copy 200-line module | Spec + thin adapter |
| Add new CLI tool | Copy subprocess boilerplate | Parser plugin + route seed |
| Prove conversion | Route-seed smoke test | + parser unit tests on fixture stdout |
| Graph nesting | String conventions | Typed relations (see doc 07) |

## Conclusion

**Do not try to replace all module logic with one mega-parser.** Do extract:

- subprocess + CLI lifecycle
- JSON list iteration patterns
- netblock/IP fan-out
- type validation and structured payloads

Leave module-specific **semantic** mapping (what counts as affiliate, when to emit `MALICIOUS_*`) in thin handler code or declarative rules with escape hatches.

See [06-recommendations-and-roadmap.md](06-recommendations-and-roadmap.md) for phased delivery.
