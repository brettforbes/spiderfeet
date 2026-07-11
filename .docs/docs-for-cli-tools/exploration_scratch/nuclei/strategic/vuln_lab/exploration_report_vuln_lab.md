# Nuclei Strategic Exploration Report

Generated: 2026-07-05T10:11:58.320712+00:00

## Target ranking (signal score)

| Rank | Target | Score | Records | Critical+High | Medium | CVEs |
|------|--------|-------|---------|---------------|--------|------|
| 1 | `pg_weblogic` | 121.4 | 26 | 12 | 0 | 0 |
| 2 | `pg_dvwa` | 2.9 | 20 | 0 | 0 | 0 |
| 3 | `pg_graphql` | 2.8 | 28 | 0 | 0 | 0 |
| 4 | `pg_guardianleaks` | 2.1 | 21 | 0 | 0 | 0 |
| 5 | `pg_restflaw` | 1.8 | 18 | 0 | 0 | 0 |
| 6 | `testfire_demo` | 1.5 | 15 | 0 | 0 | 0 |
| 7 | `gruyere` | 1.1 | 11 | 0 | 0 | 0 |
| 8 | `dvwa_co_uk` | 0.9 | 9 | 0 | 0 | 0 |
| 9 | `testasp_vulnweb` | 0.5 | 5 | 0 | 0 | 0 |
| 10 | `vulnweb_netlify` | 0.0 | 0 | 0 | 0 | 0 |
| 11 | `itsecgames` | 0 | 0 | 0 | 0 | 0 |
| 12 | `hackthissite` | 0.0 | 0 | 0 | 0 | 0 |
| 13 | `testaspnet_vulnweb` | 0 | 0 | 0 | 0 | 0 |
| 14 | `testphp_vulnweb` | 0 | 0 | 0 | 0 | 0 |
| 15 | `testhtml5_vulnweb` | 0 | 0 | 0 | 0 | 0 |

## Per-target detail

### `vulnweb_netlify`
- Severities: `{}`
- Phases with hits: (none)

- **phase_a_tech**: skipped — severities `{}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`

### `itsecgames`
- Severities: `{}`
- Phases with hits: (none)

- **preflight**: unreachable — `<urlopen error timed out>`

### `dvwa_co_uk`
- Severities: `{'info': 9}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path

- **phase_a_tech**: skipped — severities `{'info': 1}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 8}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`

### `hackthissite`
- Severities: `{}`
- Phases with hits: (none)

- **phase_a_tech**: skipped — severities `{}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`

### `gruyere`
- Severities: `{'info': 11}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path

- **phase_a_tech**: skipped — severities `{'info': 1}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 10}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`

### `testaspnet_vulnweb`
- Severities: `{}`
- Phases with hits: (none)

- **preflight**: unreachable — `<urlopen error timed out>`

### `testasp_vulnweb`
- Severities: `{'info': 5}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path

- **phase_a_tech**: skipped — severities `{'info': 3}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 2}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`

### `pg_dvwa`
- Severities: `{'info': 19, 'low': 1}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path, phase_b_nginx

- **phase_a_tech**: skipped — severities `{'info': 4}`
- **phase_b_exposure**: skipped — severities `{'low': 1, 'info': 1}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 13}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`
- **phase_hint_sqli**: skipped — severities `{}`
- **phase_hint_xss**: skipped — severities `{}`
- **phase_b_nginx**: skipped — severities `{'info': 1}`

### `pg_graphql`
- Severities: `{'info': 28}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path, phase_hint_graphql, phase_b_nginx

- **phase_a_tech**: skipped — severities `{'info': 4}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 18}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`
- **phase_hint_graphql**: skipped — severities `{'info': 5}`
- **phase_hint_sqli**: skipped — severities `{}`
- **phase_hint_xss**: skipped — severities `{}`
- **phase_hint_rce**: skipped — severities `{}`
- **phase_b_nginx**: skipped — severities `{'info': 1}`

### `pg_restflaw`
- Severities: `{'info': 18}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path, phase_b_nginx

- **phase_a_tech**: skipped — severities `{'info': 5}`
- **phase_b_exposure**: skipped — severities `{'info': 1}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 11}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`
- **phase_hint_sqli**: skipped — severities `{}`
- **phase_hint_ssrf**: skipped — severities `{}`
- **phase_b_nginx**: skipped — severities `{'info': 1}`

### `pg_weblogic`
- Severities: `{'info': 14, 'critical': 8, 'high': 4}`
- Phases with hits: phase_a_tech, phase_b_cves_path, phase_b_misconfig_path, phase_c_crit_high, phase_hint_weblogic, phase_hint_rce

- **phase_a_tech**: skipped — severities `{'info': 2}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{'critical': 2, 'high': 1}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 10}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{'critical': 2, 'high': 1}`
- **phase_hint_weblogic**: skipped — severities `{'critical': 2, 'info': 2, 'high': 1}`
- **phase_hint_rce**: skipped — severities `{'critical': 2, 'high': 1}`

### `pg_guardianleaks`
- Severities: `{'info': 21}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path, phase_b_nginx

- **phase_a_tech**: skipped — severities `{'info': 6}`
- **phase_b_exposure**: skipped — severities `{}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 14}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`
- **phase_hint_xss**: skipped — severities `{}`
- **phase_hint_ssrf**: skipped — severities `{}`
- **phase_b_nginx**: skipped — severities `{'info': 1}`

### `testphp_vulnweb`
- Severities: `{}`
- Phases with hits: (none)

- **preflight**: unreachable — `<urlopen error timed out>`

### `testhtml5_vulnweb`
- Severities: `{}`
- Phases with hits: (none)

- **preflight**: unreachable — `<urlopen error timed out>`

### `testfire_demo`
- Severities: `{'info': 15}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path, phase_b_apache

- **phase_a_tech**: skipped — severities `{'info': 1}`
- **phase_b_exposure**: skipped — severities `{'info': 1}`
- **phase_b_vulnerabilities_path**: skipped — severities `{}`
- **phase_b_cves_path**: skipped — severities `{}`
- **phase_b_misconfig_path**: skipped — severities `{'info': 12}`
- **phase_b_default_logins**: skipped — severities `{}`
- **phase_b_network**: skipped — severities `{}`
- **phase_c_crit_high**: skipped — severities `{}`
- **phase_hint_sqli**: skipped — severities `{}`
- **phase_b_apache**: skipped — severities `{'info': 1}`

## Recommendation
Promote **`pg_weblogic`** batches with critical/high/CVE hits into formal examination scenarios.
