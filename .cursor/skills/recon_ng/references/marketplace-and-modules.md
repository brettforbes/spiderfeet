# Marketplace and Modules

## Marketplace role

The marketplace is Recon-ng's module distribution channel. It allows operators to discover, install, update, and remove modules without changing core framework code.

## Core marketplace workflow

1. Refresh module index.
2. Search by category/path/keyword.
3. Inspect module metadata before install/load.
4. Install only required modules for current engagement scope.
5. Re-check for updates during long-running campaigns.

## Module lifecycle commands (conceptual)

- Search catalog entries.
- Install selected modules.
- Remove unused/problematic modules.
- Show module info for dependencies and key requirements.
- Load module and inspect runtime options.

## Category path strategy

Use path families to maintain coherent chaining:
- `recon/domains-hosts/*`
- `recon/hosts-ports/*`
- `recon/domains-contacts/*`
- `reporting/*`

Interpretation:
- The left side of `<input>-<output>` is prerequisite data shape.
- The right side is newly produced table shape.

## Disabled/stale module handling

When a module is unavailable, stale, or failing:
- Check marketplace and issues for known breakage.
- Choose an alternate module in the same input-output family.
- Revalidate output schema before continuing downstream modules.

## Risk controls

- Treat third-party module behavior as variable quality.
- Validate dependencies and API requirements before full-scale runs.
- Avoid broad install-everything behavior; keep module footprint minimal for predictable operations.

## Tactical sequencing

- Prioritize passive/high-yield modules first.
- Gate expensive API-backed modules on prior table growth.
- Pivot paths when no net new rows are produced.
