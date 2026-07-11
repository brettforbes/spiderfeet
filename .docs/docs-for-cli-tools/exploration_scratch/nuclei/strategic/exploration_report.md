# Nuclei Strategic Exploration Report

Generated: 2026-07-04T14:28:51.256672+00:00

## Target ranking (signal score)

| Rank | Target | Score | Records | Critical+High | Medium | CVEs |
|------|--------|-------|---------|---------------|--------|------|
| 1 | `vco_fund` | 11.4 | 78 | 0 | 0 | 0 |
| 2 | `scanme_sh` | 11.2 | 58 | 0 | 0 | 2 |
| 3 | `squarepeg` | 5.4 | 54 | 0 | 0 | 0 |
| 4 | `k2am` | 0.0 | 0 | 0 | 0 | 0 |

## Per-target detail

### `scanme_sh`
- Severities: `{'info': 52, 'low': 6}`
- CVE IDs: CVE-2016-6210, CVE-2018-15473
- Phases with hits: phase_b_exposures_path, phase_b_default_logins

- **phase_a_tech**: 0 hits — severities `{}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_misconfig**: 0 hits — severities `{}`
- **phase_b_panel**: 0 hits — severities `{}`
- **phase_b_exposures_path**: 29 hits — severities `{'info': 26, 'low': 3}`
- **phase_b_default_logins**: 29 hits — severities `{'info': 26, 'low': 3}`
- **phase_b_cve**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `k2am`
- Severities: `{}`
- Phases with hits: (none)

- **phase_a_tech**: 0 hits — severities `{}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_misconfig**: 0 hits — severities `{}`
- **phase_b_panel**: 0 hits — severities `{}`
- **phase_b_exposures_path**: 0 hits — severities `{}`
- **phase_b_default_logins**: 0 hits — severities `{}`
- **phase_b_cve**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `vco_fund`
- Severities: `{'info': 74, 'low': 4}`
- Phases with hits: phase_a_tech, phase_b_exposure, phase_b_panel, phase_b_exposures_path, phase_b_default_logins

- **phase_a_tech**: skipped — severities `{'info': 8}`
- **phase_b_exposure**: 1 hits — severities `{'info': 1}`
- **phase_b_misconfig**: 0 hits — severities `{}`
- **phase_b_panel**: 1 hits — severities `{'info': 1}`
- **phase_b_exposures_path**: 34 hits — severities `{'info': 32, 'low': 2}`
- **phase_b_default_logins**: 34 hits — severities `{'info': 32, 'low': 2}`
- **phase_b_cve**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

### `squarepeg`
- Severities: `{'info': 54}`
- Phases with hits: phase_a_tech, phase_b_exposures_path, phase_b_default_logins

- **phase_a_tech**: skipped — severities `{'info': 4}`
- **phase_b_exposure**: 0 hits — severities `{}`
- **phase_b_misconfig**: 0 hits — severities `{}`
- **phase_b_panel**: 0 hits — severities `{}`
- **phase_b_exposures_path**: 25 hits — severities `{'info': 25}`
- **phase_b_default_logins**: 25 hits — severities `{'info': 25}`
- **phase_b_cve**: 0 hits — severities `{}`
- **phase_c_crit_high**: 0 hits — severities `{}`

## Recommendation
No critical/high/medium richness on these four targets — widen target set or add stack-specific repos (e.g. Wordfence CVE).
