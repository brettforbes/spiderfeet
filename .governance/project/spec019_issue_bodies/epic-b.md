Spec: SPEC-019 R19-05..06. Plan: `.governance/project/SPEC019_AGENT_PLAN.md`.

## Problem

Nerva writes JSONL to `--output` and leaves stdout empty. Hydrate does not read that file → empty SUCCESS graph. GSE cartesian (Epic A) also fed fake `ip:port` lines.

## Outcome

Nerva hydrates `--output`/`-o`; empty capture is ERROR; `--list` file of real `ip:port` lines produces fingerprint records.

## Children

- B1 hydrate (after A1) → B2 fixture (after A3)

## Forbidden

Switching 12A to comma-joined `-t`; Nerva↔Nmap special-case GSE; fake SUCCESS on empty output.

## Kickoff

B1 after A1. B2 after A3. Branch from `develop`; PR into `develop`.
