# SPEC-005 setup handoff (2026-07-12)

**Mode:** Development — planning + backlog hydration (no engine implementation in this turn)  
**Spec:** `.governance/specs/SPEC-005-narrative-v2-ip-classify.md`  
**Plan:** `.governance/project/SPEC005_AGENT_PLAN.md`  
**Index:** `.governance/project/SPEC005_ISSUE_INDEX.md`

## What was set up

1. SPEC-005 requirements for IP classify + narrative v2 + UI artifact trust
2. Lesser-agent playbook with locked architecture decisions (YAML-first, type-only Mermaid, factual intros)
3. GitHub epics G–K and children G0–K1 (#958–#979)
4. Visual review checklist VR rows linked to SPEC-005
5. Placeholder artifact inventory for G0

## First assignment

| Assign | Issue | Why first |
|--------|-------|-----------|
| G0 | [#963](https://github.com/brettforbes/spiderfeet/issues/963) | Separates UI resolution bugs from truly missing files |

Optional parallel after G0 lands: **H1** [#966](https://github.com/brettforbes/spiderfeet/issues/966) (IP classifier) can run beside **G1** [#964](https://github.com/brettforbes/spiderfeet/issues/964).

## Architecture snap

- `rules/_shared/ip_patterns.yaml` → `core/ip_classify.py`
- `rules/_shared/narrative_v2.yaml` → `core/narrative_engine.py`
- Adapters stay thin; regenerate corpus in Epic J
- Mermaid in body sections = **types + relations only**

## Not done in this turn

- No IP classifier implementation
- No narrative engine refactor
- No corpus regenerate beyond prior SPEC-004 backfill
