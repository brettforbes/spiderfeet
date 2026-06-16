# dnsx Strategies, Tactics, and Workflows

## Core strategy

Run dnsx as a staged pipeline: validate candidates -> enrich record classes -> convert to nuggets -> pivot to next tools.

## Workflow 1 - Candidate validation

1. Inputs from subfinder/amass/passive sources.
2. `dnsx -silent -l candidates.txt -a -aaaa -j`.
3. Keep only names with successful answers for downstream scans.

## Workflow 2 - Infrastructure enrichment

1. Re-run live names with alias and authority records.
2. `dnsx -silent -l live.txt -cname -ns -mx -txt -j`.
3. Build CNAME cluster map and mail/security context.

## Workflow 3 - Wildcard suppression

1. Observe repeated synthetic answers across random subdomains.
2. Enable wildcard filters/threshold controls by installed version.
3. Compare with trusted resolver list and retain only stable positives.

## Workflow 4 - Pivot to service scanning

1. Convert host->IP outputs to `nodes[]`/`edges[]`.
2. Feed host/IP nodes into `httpx`, `naabu`, `nmap`, and `nerva`.
3. Re-enrich new hostnames found in TLS SAN/CNAME outputs using dnsx.

## Adaptive decision matrix

| Observation | Tactic |
|---|---|
| Too many false positives | tighten wildcard filtering + resolver quality |
| Many unresolved names | retry with alternate resolver set |
| Thin findings | add record classes beyond A/AAAA |
| Slow resolution | lower concurrency and split target lists |
| Downstream misses IPv6 services | ensure `-aaaa` enabled |
