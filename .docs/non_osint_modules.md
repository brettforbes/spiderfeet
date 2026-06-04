# Non-OSINT Spiderfeet Modules

A reference guide to Spiderfeet modules that are **generic infrastructure**—not tied to any external OSINT data source and not specialised scan logic.

These modules do not declare a `dataSource` in their metadata because they provide core platform behaviour (persisting or printing scan events). They are distinct from:

- [OSINT service modules](analysis/osint_services.json) — query third-party APIs and feeds
- [Quarantined modules](quarantine_modules.md) — lack `dataSource` but implement specialised scan logic; pending verification

**Total: 2 modules.**

---

## All Non-OSINT Modules

| Module | Name | Category | Use Cases | Flags |
|--------|------|----------|-----------|-------|
| `sfp__stor_db` | Storage | Storage & Output | — | — |
| `sfp__stor_stdout` | Command-line output | Storage & Output | — | — |

---

## Module Reference

Detailed notes for each module.

### Storage & Output

#### `sfp__stor_db` — Storage

**Category:** Storage & Output  
**Spiderfeet categories:** —  
**Use cases:** —  
**Flags:** —

**Summary:** Stores scan results into the back-end Spiderfeet database. You will need this.

**Listens for:** `*`

**Produces:** —

**How it works:** Subscribes to every event type (`*`) emitted during a scan and persists them to the Spiderfeet SQLite database via `scanEventStore()`. Optional `maxstorage` truncates oversized event payloads before storage.

**When to use:** Enable on **every scan** that uses the web UI or needs persistent results. Without it, events are lost after the scan completes.

#### `sfp__stor_stdout` — Command-line output

**Category:** Storage & Output  
**Spiderfeet categories:** —  
**Use cases:** —  
**Flags:** —

**Summary:** Dumps output to standard out. Used for when a Spiderfeet scan is run via the command-line.

**Listens for:** `*`

**Produces:** —

**How it works:** Subscribes to all events and prints them to standard output. Intended for CLI-driven scans where results are consumed in the terminal rather than the web UI database.

**When to use:** Use for **CLI-only** workflows (`sf.py -o tab`) where you want live event streaming without database storage.

---

*Generated from Spiderfeet module metadata. Total: 2 core non-OSINT modules.*
