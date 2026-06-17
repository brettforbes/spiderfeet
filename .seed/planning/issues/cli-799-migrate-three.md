**Epic:** #723 · **Phase:** 2d · **Depends:** #797, #798

## Problem

Prove manifest-only path by replacing hand-written modules for the simplest CLIs.

## Desired outcome

Migrate **dnstwist**, **wafw00f**, and **snallygaster** to manifest-driven runner. Deprecate or thin-wrap existing `sfp_tool_*` modules.

## Acceptance criteria

- [ ] Manifests checked into `.docs/analysis/cli_manifests/` (or similar)
- [ ] Battery parity: same or better classification vs legacy module
- [ ] Legacy modules marked deprecated in meta or removed with migration note
- [ ] Seeds updated in `module_test_seeds.json`

## Verification

- Side-by-side battery run legacy vs manifest id
- PR with evidence comment on #777, #783, #786

## Spec

R3-05-07, R3-05-08
