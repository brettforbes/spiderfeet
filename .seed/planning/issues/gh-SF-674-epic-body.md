## Problem

32 none-tier OSINT modules still lack smoke-validated entries in `module_test_seeds.json` after automated corpus validation and generic tuning (coverage stuck at **55/87**, 63.2%).

## Outcome

One child issue per module (**SF-675**–**SF-706**) with:
- per-module input research via `scan_ui` + scan logs
- registry update or documented `SPEC_GAP` (broken upstream API, negative fixture, etc.)

## Manifest

`.seed/planning/pending_seed_research_manifest.json`

## Spec

R2-04-07

## Verification

`poetry run python .seed/scripts/validate_test_seeds.py --tier none --write` shows increased `coverage_count`.
