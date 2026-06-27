## Problem

Nmap CLI profiling pilot (15 scenarios, evidence bundles, graphs, narrative reports) is complete but examinations were not uniformly operator-approved and corpus index still showed `nugget_proposal`.

## Desired outcome

All 15 Nmap scenarios operator-approved; `corpus_index.json` marks nmap `complete`; sign-off doc published; codebase clean for next tool (netdiscover).

## Spec binding

- `.seed/04_Driving and Integrating_CLI_Apps.md`
- Parent: #826
- Related: #830 (Nmap update epic)

## Acceptance criteria

- [ ] All 15 scenario keys `review_status: approved`
- [ ] API `list_scenarios` reflects legacy review aggregation
- [ ] `nmap_pilot_signoff.md` published
- [ ] Temp/scratch files removed
- [ ] Tests pass

## Verification

`python -m pytest .tests/api/test_cli_corpus.py .tests/test_narrative_report.py -q`
