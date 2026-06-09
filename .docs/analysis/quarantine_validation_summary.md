# Quarantine validation battery summary

**Run:** `2026-06-09` via `.seed/scripts/run_quarantine_battery.py --local`  
**Report:** `quarantine_battery_results.json`

## Results (54 modules)

| Classification | Count | Meaning |
|----------------|------:|---------|
| `validated_hit` | 17 | Primary route produces nuggets; seed recorded |
| `clean_miss` | 22 | FINISHED with zero output — candidate **negative fixture** or needs seed tuning |
| `tool_missing_or_blocked` | 13 | External CLI wrapper; tool not on PATH or blocked |
| `error_failed` | 1 | Module/scan error — investigate |
| `timeout` | 1 | Exceeded probe timeout — extend or narrow scope |

### Validated hits

`sfp_base64`, `sfp_bitcoin`, `sfp_company`, `sfp_countryname`, `sfp_creditcard`, `sfp_dnsbrute`, `sfp_dnsraw`, `sfp_dnsresolve`, `sfp_email`, `sfp_ethereum`, `sfp_filemeta`, `sfp_hashes`, `sfp_pgp`, `sfp_portscan_tcp`, `sfp_similar`, `sfp_spider`, `sfp_whois`

### Tool wrappers (blocked pending CLI install)

All `sfp_tool_*` modules except those classified otherwise.

## API / platform changes

- **Payload nugget injection:** `scan_ui` + `sfscan` inject consumed content events (`TARGET_WEB_CONTENT`, `WEBSERVER_HTTPHEADERS`, etc.) while anchoring the scan on `INTERNET_NAME`.
- **Catalogue enrichment:** `enrich_quarantine_documentation.py` writes long-form `data_source.description` and Stage 5 header blocks on modules.

## Follow-up

1. Tune `clean_miss` modules (negative fixture vs better positive input)
2. Install/document CLI tools for `tool_missing_or_blocked`
3. Replace placeholder icons — `generic_icon_design_briefs.md`
4. Re-bootstrap TypeDB map after `service_state` updates
