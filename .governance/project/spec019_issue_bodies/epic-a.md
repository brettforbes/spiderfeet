Spec: SPEC-019 R19-01..04. Plan: `.governance/project/SPEC019_AGENT_PLAN.md`. Spec file: `.governance/specs/SPEC-019-composer-refine-2.md`. Seed: `.seed/20_Refine_Composer_2.md`.

## Problem

uuid5 identity collapses `TRANSPORT(tcp)` / `PORT("22")` across hosts. GSE then cartesian-products Nmap IPs × ports (live k2am: 13×2=26 fake `ip:port` lines). Nested GSE `for_each` also fails to scope children to the parent.

## Outcome

Occurrence-scoped uuid4 for ENTITY/SUBENTITY/CATEGORY/INTERNAL with parent cache; host-scoped `ip_port_list`; docs that overwrite SPEC-004 R4-01-01.

## Children (execute in order)

- A1 uuid4 + parent cache → A2 topology parent_id → A3 host-scoped GSE → A4 docs

## Constraints / forbidden

- Do not value-dedupe uuid4 types.
- Do not re-harvest corpus or rewrite historical graph JSON.
- Do not rewrite GSE to TypeQL.
- Keep both `graph_builder.py` copies in sync.

## Kickoff

Lesser agents: pick A1 first (parallel with F1 and YAML D1). Branch from `develop`; PR into `develop`; comment start/PR/close; update `.governance/project/SPEC019_ISSUE_INDEX.md`.
