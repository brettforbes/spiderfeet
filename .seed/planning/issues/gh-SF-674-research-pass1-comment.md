## Research pass 1 complete

**Wins:** 1 — registry updated (`sfp_googleobjectstorage` → `youtube.com`, 2 produced). See #688.

**Blocker summary (31 modules):**

| Class | Count | Examples |
|-------|------:|----------|
| `no-output-clean-input` | 18 | ahmia, crobat, emailformat, torch |
| `module-error` | 4 | dnsdumpster (CSRF), sublist3r, searchcode, myspace |
| `api-json` | 2 | crt, gravatar |
| `api-timeout` | 2 | commoncrawl, threatminer |
| `unknown` | 5 | gleif (HTTP_400 target), keybase, openstreetmap, s3bucket, venmo |

**Artifacts:**
- `.docs/analysis/pending_seed_research.md`
- `.docs/analysis/pending_seed_research.json`
- `.seed/scripts/research_pending_seeds.py`

**Next:** module-code fixes for `module-error` cluster; upstream API investigation for JSON/timeout; negative-fixture classification where silence is correct (e.g. reversewhois "no info").
