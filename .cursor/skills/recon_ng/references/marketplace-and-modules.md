# Marketplace and Modules

## Role

The marketplace ([recon-ng-marketplace](https://github.com/lanmaster53/recon-ng-marketplace)) distributes modules without changing core framework code. Modules are selected by path families such as `recon/domains-hosts/*`.

## Bootstrap vs stealth

Authoritative capture (**2026-08-10**): running with `--stealth` prints `Marketplace disabled.` and `recon-cli -M` returns `[!] No modules found.`

| Goal | Action |
|------|--------|
| Install / refresh modules | Run **without** `--stealth` and **without** `--no-marketplace` |
| Later OPSEC (no version/analytics/marketplace checks) | `--stealth` only **after** needed modules are installed locally |

## Lifecycle (console)

Typical interactive flow (wiki / Features):

1. Refresh marketplace index
2. Search by path or keyword
3. Inspect module info (dependencies, keys)
4. Install required modules only
5. `modules load <path>` → configure → run
6. Remove unused or broken modules when cleaning

Do not invent marketplace subcommand spellings beyond what the installed console documents via `help`.

## Category paths

| Path family | Intent |
|-------------|--------|
| `recon/domains-hosts/*` | Domain seeds → host rows |
| `recon/domains-contacts/*` | Domain seeds → contacts |
| `recon/hosts-ports/*` | Hosts → ports/services |
| `reporting/*` | Export / handoff artifacts |

Left side of `<input>-<output>` = prerequisite shape; right side = produced table shape.

## Disabled / stale modules

- Check marketplace and marketplace issues for breakage
- Pivot to another module in the same I/O family
- Revalidate output columns before downstream chaining

## Risk controls

- Treat third-party modules as variable quality
- Minimal install footprint for predictable automation
- Gate API-heavy modules on prior table growth
