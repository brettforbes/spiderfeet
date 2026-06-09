# Quarantine validation battery summary

**Run:** `2026-06-09` via `.seed/scripts/run_quarantine_battery.py --local`  
**Report:** `quarantine_battery_results.json`  
**Promotion:** `.seed/scripts/promote_quarantine_hits.py --write` (#794)

## Results (54 modules probed)

| Classification | Count | Meaning |
|----------------|------:|---------|
| `validated_hit` | 32 | Primary route produces nuggets; promoted to `external` + `in-test` |
| `validated_negative` | 9 | Expected clean miss / blocked config / slow smoke deferred |
| `tool_missing_or_blocked` | 13 | External CLI wrapper; tool not on PATH |
| `clean_miss` | 0 | All non-tool modules tuned or classified |

**Quarantine catalogue:** 54 → **22** (32 promoted out)

### Promoted hits (32)

`sfp_base64`, `sfp_binstring`, `sfp_bitcoin`, `sfp_company`, `sfp_cookie`, `sfp_countryname`, `sfp_creditcard`, `sfp_dnsbrute`, `sfp_dnsneighbor`, `sfp_dnsraw`, `sfp_dnsresolve`, `sfp_email`, `sfp_errors`, `sfp_ethereum`, `sfp_filemeta`, `sfp_hashes`, `sfp_iban`, `sfp_intfiles`, `sfp_names`, `sfp_pageinfo`, `sfp_pgp`, `sfp_phone`, `sfp_portscan_tcp`, `sfp_similar`, `sfp_social`, `sfp_spider`, `sfp_sslcert`, `sfp_strangeheaders`, `sfp_webanalytics`, `sfp_webframework`, `sfp_webserver`, `sfp_whois`

### Negative / deferred fixtures (9)

`sfp_accounts` (slow network smoke), `sfp_crossref`, `sfp_customfeed` (no feed URL), `sfp_dnscommonsrv`, `sfp_dnszonexfer`, `sfp_hosting` (ipcat range miss on probe IPs), `sfp_junkfiles` (no junk on example.com), `sfp_subdomain_takeover` (fingerprints OK; no hijack on probe host), `sfp_tldsearch` (`blocked-slow` — completes only with extended timeout)

### Investigations closed

- **`sfp_subdomain_takeover`:** upstream fingerprints URL moved to `subjack/fingerprints.json`; bundled `spiderfeet/dicts/subjack_fingerprints.json`; probe uses `AFFILIATE_INTERNET_NAME`.
- **`sfp_tldsearch`:** probe corrected to `INTERNET_NAME`; classified `validated_negative` / `blocked-slow` for default battery timeout.

## API / platform changes

- **Payload injection:** `sfscan` sets `actualSource` and `sfp_spider` source for content/header payloads; `LINKED_URL_EXTERNAL` and `PROVIDER_DNS` supported in `scan_targets.py`.
- **Promotion script:** `promote_quarantine_hits.py` moves validated modules from quarantine catalogue to `external` + `in-test`.

## Follow-up

1. Install/document CLI tools for remaining 13 `sfp_tool_*` modules
2. Replace placeholder icons — `generic_icon_design_briefs.md`
3. Re-bootstrap TypeDB map after `service_origin` / `service_state` promotion
