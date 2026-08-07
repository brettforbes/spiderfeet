# SPEC-010 acceptance harness (Epic AP)

**Requirements:** R10-29 (AP1 / G3 live evidence) · R10-30 (AP2 script)

## Documented targets (R10-29)

| Host | Note |
|------|------|
| `sbs.com.au` | Media / CDN-heavy |
| `k2am.com.au` | Smaller org |
| `venturecapitalopportunitiesfund.com.au` | Sparse / permissive lab-like |
| `squarepeg.vc` | VC / alternate TLD |

AP1 records live 12A evidence under `evidence/` and waits for operator G3 sign-off.
**AP2 does not claim AP1 complete.**

## AP2 script

```bash
# Dry-run one target (default: in-process TestClient — no TypeDB / no G3)
poetry run python spiderfeet_v2/acceptance/run_four_targets.py --target sbs.com.au

# Dry-run all documented targets
poetry run python spiderfeet_v2/acceptance/run_four_targets.py --all

# Live against a running API (after AP1 tooling is ready; still not G3 sign-off)
poetry run python spiderfeet_v2/acceptance/run_four_targets.py --live --target sbs.com.au \
  --base-url http://127.0.0.1:8001/api/v1
```

### Assertions (R10-30)

- No `IP_ADDRESS` nugget nodes (use `IPV4_ADDRESS` / `IPV6_ADDRESS`)
- No orphan graph nodes when edges exist
- Four-form storage on persisted scan steps (`text` / `structured` / `graph` / `markdown`)
- Project / workflow / scan-step / context JSON queryable via the v2 API

Dry-run + in-process seeds a synthetic four-form scan_step so the validators are
exercised without a live CLI scan.
