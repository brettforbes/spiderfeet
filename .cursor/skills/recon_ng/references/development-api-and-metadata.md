# Development API and Metadata

## Operator value

Even without writing modules, metadata and framework API concepts improve safe selection, troubleshooting, and upgrade resilience.

## Module metadata

Before load/run, inspect module info for:

- Category path and intended I/O
- Dependency (**D**) requirements
- Key (**K**) requirements
- Maintainability / description signals

Use metadata as automation preflight, not optional flavor text.

## Framework API / mixins

Modules share framework services (options, requests, parsing, DB). Failures may be:

- Framework-level → [recon-ng issues](https://github.com/lanmaster53/recon-ng/issues)
- Module-level → [marketplace issues](https://github.com/lanmaster53/recon-ng-marketplace/issues)

See [Development Guide](https://github.com/lanmaster53/recon-ng/wiki/Development-Guide).

## Marketplace indexing

- Refresh indexes before assuming a module is absent
- Re-verify after framework upgrades
- Update long-lived runbooks when modules are renamed/removed

## Troubleshooting order

1. Dependency / key / option metadata
2. Minimal SOURCE + higher `VERBOSITY`
3. Correct issue tracker (core vs marketplace)
4. Alternate module in the same I/O path

## Preflight checklist (scripted runs)

1. Metadata confirms required inputs exist
2. Dependencies installed
3. Keys present for K modules
4. SOURCE explicit and bounded
5. Marketplace modules installed if not using a pre-baked module tree
6. Output / reporting targets defined
