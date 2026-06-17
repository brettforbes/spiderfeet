**Epic:** #722 · **Program:** #723 (CLI integration Phase 1)

## Problem

All 13 external CLI tool wrappers are quarantined with battery classification `tool_missing_or_blocked`. They cannot be promoted until binaries are installed, module opts are set, and smoke routes produce evidence.

## Modules (13)

- [ ] `sfp_tool_cmseek` — #776
- [ ] `sfp_tool_dnstwist` — #777
- [ ] `sfp_tool_nbtscan` — #778
- [ ] `sfp_tool_nmap` — #779
- [ ] `sfp_tool_nuclei` — #780
- [ ] `sfp_tool_onesixtyone` — #781
- [ ] `sfp_tool_retirejs` — #782
- [ ] `sfp_tool_snallygaster` — #783
- [ ] `sfp_tool_testsslsh` — #784
- [ ] `sfp_tool_trufflehog` — #785
- [ ] `sfp_tool_wafw00f` — #786
- [ ] `sfp_tool_wappalyzer` — #787
- [ ] `sfp_tool_whatweb` — #788

## Tool install reference

| Module | Website |
|--------|---------|
| cmseek | https://github.com/Tuhinshubhra/CMSeeK |
| dnstwist | https://github.com/elceef/dnstwist |
| nbtscan | http://www.unixwiz.net/tools/nbtscan.html |
| nmap | https://nmap.org/ |
| nuclei | https://nuclei.projectdiscovery.io/ |
| onesixtyone | https://github.com/trailofbits/onesixtyone |
| retire.js | https://github.com/RetireJS/retire.js |
| snallygaster | https://github.com/hannob/snallygaster |
| testssl.sh | https://testssl.sh |
| trufflehog | https://github.com/trufflesecurity/trufflehog |
| wafw00f | https://github.com/EnableSecurity/wafw00f |
| wappalyzer | https://www.wappalyzer.com/ |
| whatweb | https://github.com/urbanadventurer/whatweb |

## Per-module work

1. Install CLI (+ interpreter deps: Ruby/Node where required)
2. Set `module_opts` path in scan config or global opts
3. Run `run_quarantine_battery.py --local --only <module_id> --write`
4. Update seeds + `service_state`; promote if hit
5. Close linked `[Quarantine]` issue with evidence

## Acceptance criteria

- [ ] `TOOL_INSTALL` notes in `.seed/scripts/enrich_quarantine_documentation.py` verified against live install
- [ ] Battery summary: 0 unresolved `tool_missing_or_blocked` (hit, negative, or explicit `error` with log)
- [ ] Each promoted tool: `service_origin: external`, `service_state: in-test`
- [ ] TypeDB map bootstrap includes promoted tool services

## Verification

- `python .seed/scripts/run_quarantine_battery.py --local --only sfp_tool_*`
- Targeted `pytest` for modules with unit tests under `test/unit/modules/test_sfp_tool_*.py`
- Maps/Tests smoke per module issue

## Spec

R3-05-02, R3-05-06, R3-05-07

## Next

After this batch closes, start Phase 2 (#796–#799) under epic #723.
