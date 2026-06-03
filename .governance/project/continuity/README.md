# Agent Continuity

Per GOV-09. Continuity is execution infrastructure—not optional cleanup.

## Layers

| Layer | Path | Holds |
|-------|------|--------|
| Session / thread | `.governance/project/continuity/session/` | Active thread diary, ephemeral decisions |
| Recent / daily | `.governance/project/continuity/recent/` | Last few days of cross-session notes |
| Project | `.governance/project/continuity/project/PROJECT_CONTINUITY.md` | Durable repo decisions, taxonomy, conventions |
| Global / operator | *(out of repo)* | Operator preferences; do not commit secrets |

## Checkpoint triggers

Write a compact checkpoint when any of these occur:

- New or corrected instructions from the operator
- A decision that affects module taxonomy, specs, or workflow
- A blocker discovered (also update `INIT-TODO.md`)
- Phase change (bootstrap → verification → implementation)
- Multi-step work exceeding ~30 minutes wall time
- Compaction / handoff / new agent session risk

## Promotion flow

```
session diary  →  recent note  →  PROJECT_CONTINUITY.md
                                      ↓
                              spec / BACKLOG update (when actionable)
```

Promote upward when information is **durable** and **actionable**. Do not promote raw chat transcripts.

## Session diary

Use `session/SESSION_DIARY_TEMPLATE.md` for recurring threads. One file per thread/context is fine (`session/<topic>.md`).

## Anti-patterns

- Relying on chat memory as the only state store
- Dumping full transcripts into continuity files
- Mixing provisional experiments into PROJECT_CONTINUITY without labelling status
