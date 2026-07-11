# SPEC-004 program completion handoff (2026-07-12)

**Spec:** `.governance/specs/SPEC-004-cli-graph-rules-engine.md`  
**Issue index:** `.governance/project/SPEC004_ISSUE_INDEX.md`  
**Visual review:** `.governance/project/SPEC004_VISUAL_REVIEW_CHECKLIST.md`

## Program status

| Epic | Issue | Child stories | Status |
|------|-------|---------------|--------|
| A Foundations | #906 | A1–A6 (#911–#916) | **Complete** — all children closed |
| B Rule engine + pilots | #907 | B1–B5 (#917–#921) | **Complete** |
| C Nerva correlation | #908 | C1–C4 (#922–#925) | **Complete** |
| D Remaining tools + narratives | #909 | D1–D7 (#926–#932) | **Complete** |
| Phase 4 | — | F1 #950, F2 #949 | **Complete** (structural goldens; byte-lock gated on operator sign-off) |
| E Thin sfp modules | #910 | E1–E3 (#953, #952, #954) | **Complete** — bridge pilot + pattern docs |

## Acceptance evidence (SPEC-004 program)

1. **Adapters + YAML** — eight tools under `adapters/` with `rules/<tool>/mapping.yaml`
2. **Identity** — `core.graph_builder.nugget_instance_id` only; governance test enforces
3. **Nerva 07+07B** — correlation engine + adapter hooks with fired-rule evidence
4. **Harvest four artifacts** — `ADAPTER_TOOLS` includes netdiscover, nmap, nerva, pius, subfinder, httpx, katana, nuclei
5. **Visual review gate** — checklist doc (D7); operator UI sign-off still pending for byte goldens
6. **Anti-sprawl** — `.tests/test_spec004_governance.py`

## Verification command bundle

```bash
python -m pytest \
  .tests/test_spec004_governance.py \
  .tests/test_spec004_structural_goldens.py \
  .tests/test_spec004_narrative_coverage.py \
  .tests/test_harvest_adapter_dispatch.py \
  .tests/test_nmap_adapter.py \
  .tests/test_netdiscover_adapter.py \
  .tests/test_nerva_adapter.py \
  .tests/test_pius_adapter.py \
  .tests/test_subfinder_adapter.py \
  .tests/test_httpx_adapter.py \
  .tests/test_katana_adapter.py \
  .tests/test_nuclei_adapter.py \
  -q
```

Last run: **65 passed** (develop @ `72239686`, full SPEC-004 bundle including Epic E bridge).

## Residual / follow-up

- Operator visual sign-off on checklist before **byte-locked** graph/narrative fixtures
- Epic E: per-module `sfp_tool_*` rewrites (one issue per module under #723)
- TypeQL promotion for `nuggets_extension.json` entries (A4 follow-up)

## No Nexus

Per spec non-goals — no Nexus tool or adapters were created.
