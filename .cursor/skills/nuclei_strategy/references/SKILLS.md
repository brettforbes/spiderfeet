# Nuclei Strategy References Index

Strategy skill for **sequential, tag-targeted** Nuclei examination—not full-template noise on hardened targets.

## Read order

1. [scanning-principles.md](scanning-principles.md) — when to narrow scans and how to batch goals
2. [sequential-playbook.md](sequential-playbook.md) — multi-phase execution for corpus tuning
3. [tags-and-categories.md](tags-and-categories.md) — which tags to use in each phase
4. [selective-scan-techniques.md](selective-scan-techniques.md) — concrete command patterns
5. [high-value-targets.md](high-value-targets.md) — what to hunt and chain
6. [api-pentest-techniques.md](api-pentest-techniques.md) — API workflows and example templates

## Related skills (execution layer)

| Skill | Path | Use for |
|-------|------|---------|
| Nuclei execution | [../../nuclei/SKILL.md](../../nuclei/SKILL.md) | CLI defaults, JSONL parse, nugget mapping |
| Nuclei tactics | [../../nuclei/references/tactics.md](../../nuclei/references/tactics.md) | Broad→narrow, tech-first, rate limits |
| CLI app profiling | [../../cli_app_profiling/SKILL.md](../../cli_app_profiling/SKILL.md) | Examination bundles, scenario matrix |

## Canonical source document

- [`.seed/03EB_Rethinking_Nuclei_Strategy.md`](../../../.seed/03EB_Rethinking_Nuclei_Strategy.md) — operator strategy notes this skill decomposes

## Operator guides (repo root)

- [Nuclei Zero to Hero](../../../.docs/docs-for-cli-tools/Nuclei-Zero-to-Hero.md)
- [Nuclei CLI Options](../../../.docs/docs-for-cli-tools/Nuclei-CLI-Options.md)
