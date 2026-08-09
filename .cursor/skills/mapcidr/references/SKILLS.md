# mapcidr References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Captured help (2026-08-10), all flags, invocation notes |
| [output-and-parsing.md](output-and-parsing.md) | Line-oriented stdout shapes; parse into SpiderFeet JSON `records[]` |
| [nugget-mapping.md](nugget-mapping.md) | CIDR/IP lines → SpiderFeet netblock and address nuggets |
| [tactics.md](tactics.md) | Expand → slice → aggregate → scan sequencing |
| [sources.md](sources.md) | Official repo, README, releases, pkg.go.dev, issues |

**Read order for new agents**

1. `cli-options.md` — flags from live `-h` only (no invented `-json` / `-l`).
2. `output-and-parsing.md` — line types and harvest bundle shape.
3. `nugget-mapping.md` — emit SpiderFeet graph JSON.
4. `tactics.md` — when to expand vs slice vs aggregate.
5. `sources.md` — upstream docs.

**Operator docs**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/mapcidr-Zero-to-Hero.md` | Install → expand → slice → aggregate → nuggets |
| `.docs/docs-for-cli-tools/mapcidr-CLI-Options.md` | Full CLI reference + Captured help |

**Related skills:** [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md), [`../../uncover/SKILL.md`](../../uncover/SKILL.md)
