**Parent epic:** #710  
**Depends on:** spike issue (auth flow)

## Problem statement

Subscriptions UI and API assume a **single static API key** (`binaryedge_api_key`). Coalition Control uses **username/password login → Bearer token** and **entity-scoped** ASM calls.

## Scope

- Design secret storage for Coalition credentials (username/password and/or cached bearer token)
- API schema: module opts exposed on `GET/PUT /api/v1/subscriptions/modules/{id}`
- Subscriptions widget: replace “API key” field with Coalition-appropriate fields + setup instructions
- Signup checklist: update `signup_links` / `free_auth_api_key_signup` for Coalition Control (not binaryedge.io)
- MFA note: API user must disable MFA per Coalition docs

## Acceptance criteria

- [ ] Operator can save Coalition credentials via Subscriptions without 422 unsupported-opt errors
- [ ] Instructions link to https://www.coalitioninc.com/control and API QuickStart
- [ ] Token handling documented (refresh strategy or re-login on 401)
- [ ] `entity_id` discoverable via `/asm/me` or stored as opt after first login

## Spec binding

- SPEC-002: R2-02-xx (subscriptions API) + R2-04-03
- SPEC_GAP: Bearer-token auth pattern for `free_auth` modules

## Verification

- Manual Subscriptions save + module scan smoke after module rewrite lands
