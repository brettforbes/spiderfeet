**Parent epic:** #710

## Problem statement

Before rewriting `sfp_binaryedge`, we need a validated mapping from legacy BinaryEdge query types to Coalition Control ASM endpoints, plus clarity on **free-account API entitlements**.

## Tasks

- [ ] Confirm free Coalition Control account can call `/auth/login` and `/asm/me`
- [ ] Document token lifetime / refresh behaviour (if any)
- [ ] Map legacy routes → Coalition endpoints (see transition doc table)
- [ ] Classify each legacy produced nugget: **supported**, **partial**, **unsupported**
- [ ] Flag routes with no Coalition equivalent (passive DNS, torrent, arbitrary subdomain enum)
- [ ] Propose module rename vs retain `sfp_binaryedge` module_id
- [ ] Update `.docs/analysis/binaryedge_coalition_control_transition.md` with findings

## Acceptance criteria

- Written mapping table with confidence levels and sample JSON shapes
- Operator can follow steps to obtain credentials + `entity_id` on free tier
- Recommendation on whether module remains `free_auth` or moves tier
- Linked follow-up issues updated with concrete endpoint + field names

## Spec binding

- SPEC_GAP → promote to SPEC-002 requirement IDs after spike

## References

- `.docs/analysis/binaryedge_coalition_control_transition.md`
- Coalition OpenAPI: https://api.control.coalitioninc.com/docs/api
