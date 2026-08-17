Spec: SPEC-019 R19-07..09. Plan: `.governance/project/SPEC019_AGENT_PLAN.md`.

## Problem

`sfp_cli_nuclei` can chunk targets (DEFAULT_BATCH_SIZE=20) but the workflow engine only passes `argv` + first `target`. `_collect_urls` sees one URL; one 900s process runs the full template tree.

## Outcome

Full URL list batches of 20; Composer `i/n` = batches; per-batch `timeout` + `overall_timeout`; `crawl_urls` is URL/LINK only.

## Children

- C1 wire urls → C2 progress/timeouts → C3 tests + crawl_urls

## Forbidden

Per-URL fan-out; extra option_passes in 12A; host-widget work; switching to HTTP_CODE.

## Kickoff

C1 can start parallel to A/B. Branch from `develop`; PR into `develop`.
