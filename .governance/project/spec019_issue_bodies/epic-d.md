Spec: SPEC-019 R19-10..12. Plan: `@spiderfeet/.governance/project/SPEC019_AGENT_PLAN.md`. Spec: `@spiderfeet/.governance/specs/SPEC-019-composer-refine-2.md`.

## Problem

SPEC-018 C3 stopped tagging HTTPX/Katana as `semantic-export`, but collector `dependencies` still include every step on the rank. Nice-DAG draws those edges; unlabeled deps default to `followed-by` (vertical-looking sequence on a horizontal collector).

## Outcome

Collector deps = exporters + previous collector. `followed-by`/`used-by` on vertical ports only; `semantic-export` on CX.

## Children

D1 deps → D2 ports → D3 smoke

## Forbidden

Removing Subfinder export edge; dropping rank collectors because a sibling has `export: none`; rewriting expand internals unless smoke fails after D1.

## Kickoff

D1 first, parallel to backend A1. Branch from `develop`; PR into `develop`; update `.governance/project/SPEC019_ISSUE_INDEX.md`.
