Spec: SPEC-019 R19-15..22. Plan: `.governance/project/SPEC019_AGENT_PLAN.md`.

## Problem

Subfinder emits sibling `DOMAIN_NAME` nodes; there is no `SUBDOMAIN` type. Seed 09 forbids COMPANY without org evidence. HTTPX/Katana hang URLs off SCAN_RECORD. Pius uses `COMPANY_NAME` as the ENTITY root.

## Outcome

`SCAN_RECORD --contains--> COMPANY --contains--> DOMAIN_NAME --contains--> SUBDOMAIN`; website roots contain `LINKED_URL_INTERNAL`. `COMPANY_NAME` is a DESCRIPTOR. Validator enforces apex COMPANY ownership.

## Children

F1 catalogue → F2 helper (needs A1) → F3–F7 parallel → F8 validator

## Forbidden

Nested SUBDOMAIN trees; SCAN containing every URL; retyping HTTP_CODE; full Pius rewrite; corpus re-harvest; requiring COMPANY on every CDN CNAME.

## Kickoff

F1 parallel with A1. F2 after A1+F1. Branch from `develop`; PR into `develop`.
