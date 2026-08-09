# Module Types and Datastore

## Module classes

| Class | SpiderFeet default role |
|-------|-------------------------|
| `auxiliary/scanner/*` | Host/service/protocol enumeration — **preferred** |
| `auxiliary/gather/*` | Credential/config/info gathering — **preferred** when authorized |
| `auxiliary/admin/*` | Administrative actions — elevated risk; confirm scope |
| `exploit/*` | Exploitation — **out of scope** unless explicitly approved |
| `payload/*` | Delivered by msfvenom or exploit context |
| `encoder/*`, `nop/*` | Encoding / sleds for constrained delivery |
| `post/*` | Post-exploitation — session required; sensitive |
| `evasion/*` | AV/EDR evasion — not a corpus default |

In-repo docs live under `documentation/modules/**` (example: `auxiliary/scanner/http/brute_dirs.md`). Prefer those + `info -d` over third-party blogs.

## Datastore discipline

1. Set **required** options first (`RHOSTS`, `RPORT`, auth fields).
2. Review **advanced** only when tuning threads, proxies, SSL, timing.
3. Review **evasion** only when the engagement explicitly includes that risk.
4. Prefer module-local `set` over `setg` in scripts unless every step needs the same global.
5. After module switch, re-check `show options` — required keys differ by module.

## Check vs exploit

| Situation | Action |
|-----------|--------|
| Module implements `check` | Run `check`; treat negative as “not vulnerable / not applicable,” not always “module broken” |
| Discovery only | Use `run` on auxiliary; never `exploit` |
| Authorized exploit | Re-read reliability/side effects; confirm target/payload; then `exploit` |
| `check` unsupported | Do not invent a check; rely on aux scanners + external tools |

## Reliability / side effects / stability

Official definitions: [Module reliability, side effects, and stability](https://docs.metasploit.com/docs/development/developing-modules/module-metadata/definition-of-module-reliability-side-effects-and-stability.html). For SpiderFeet graph building, skip modules whose side effects imply DoS or destructive writes unless the lab charter allows them.
