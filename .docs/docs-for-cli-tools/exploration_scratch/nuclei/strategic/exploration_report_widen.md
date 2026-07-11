# Nuclei Strategic Exploration Report

Generated: 2026-07-04T17:08:19.964420+00:00

## Target ranking (signal score)

| Rank | Target | Score | Records | Critical+High | Medium | CVEs |
|------|--------|-------|---------|---------------|--------|------|
| 1 | `scanme_nmap_org` | 4.2 | 15 | 0 | 0 | 0 |
| 2 | `vco_fund` | 2.0 | 20 | 0 | 0 | 0 |
| 3 | `testasp_vulnweb` | 0.7 | 7 | 0 | 0 | 0 |
| 4 | `testfire_demo` | 0.3 | 3 | 0 | 0 | 0 |
| 5 | `testphp_vulnweb` | 0.0 | 0 | 0 | 0 | 0 |
| 6 | `testhtml5_vulnweb` | 0.0 | 0 | 0 | 0 | 0 |

## Per-target detail

### `scanme_nmap_org`
- Severities: `{'info': 12, 'low': 3}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path, phase_b_apache

- **phase_a_tech**: 1 hits — severities `{'info': 1}`
- **phase_b_exposure**: 1 hits — severities `{'low': 1}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 11 hits — severities `{'info': 10, 'low': 1}`
- **phase_c_crit_high**: 0 hits — severities `{}`
- **phase_b_apache**: 2 hits — severities `{'low': 1, 'info': 1}`

### `testphp_vulnweb`
- Severities: `{}`
- Phases with hits: (none)

- **phase_a_tech**: 0 hits — severities `{}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `testasp_vulnweb`
- Severities: `{'info': 7}`
- Phases with hits: phase_a_tech, phase_b_misconfig_path

- **phase_a_tech**: 3 hits — severities `{'info': 3}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 4 hits — severities `{'info': 4}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `testhtml5_vulnweb`
- Severities: `{}`
- Phases with hits: (none)

- **phase_a_tech**: 0 hits — severities `{}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `testfire_demo`
- Severities: `{'info': 3}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path

- **phase_a_tech**: 1 hits — severities `{'info': 1}`
- **phase_b_exposure**: 1 hits — severities `{'info': 1}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 1 hits — severities `{'info': 1}`
- **phase_c_crit_high**: 0 hits — severities `{}`
- **phase_b_apache**: 0 hits — severities `{}`

### `vco_fund`
- Severities: `{'info': 20}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_misconfig_path, phase_b_drupal

- **phase_a_tech**: 8 hits — severities `{'info': 8}`
- **phase_b_exposure**: 1 hits — severities `{'info': 1}`
- **phase_b_vulnerabilities_path**: 0 hits — severities `{}`
- **phase_b_cves_path**: 0 hits — severities `{}`
- **phase_b_misconfig_path**: 9 hits — severities `{'info': 9}`
- **phase_c_crit_high**: 0 hits — severities `{}`
- **phase_b_drupal**: 2 hits — severities `{'info': 2}`

## Recommendation
No critical/high/medium richness on these four targets — widen target set or add stack-specific repos (e.g. Wordfence CVE).
