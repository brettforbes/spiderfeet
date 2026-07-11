# Nmap OS Fingerprint & Port/Transport Graph Conversion Rules

Rules for converting nmap XML `<os>` (osmatch/osclass) and `<ports>` data into
graph nuggets and relations. Worked examples are drawn from two real scans of
`scanme.nmap.org` (45.33.32.156) — a top-1000-port scan and a targeted
22/80/443 scan.

**Relation convention used throughout:** *"A is linked by a `contains`
relation to B"* means **B contains A** (B is the parent/container, A is the
child).

---

## Hierarchy overview

```
ENVIRONMENT --[contains]--> OPERATING_SYSTEM --[contains]--> CPE_URL
```

Each `OPERATING_SYSTEM` nugget also carries descriptor nuggets via `had`,
and — for the top-accuracy candidate only — a `listens-to` relation to the
port(s) it was fingerprinted from (see Rule P3).

---

## Rule G1 — Generic: ENVIRONMENT contains OPERATING_SYSTEM

```
ENVIRONMENT --[contains]--> OPERATING_SYSTEM
```

Applies regardless of source tool — every OS-identification result feeds
into the same `ENVIRONMENT` category node.

> **Addendum (recommended, not mandated):** also emit
> `HOST --[contains]--> OPERATING_SYSTEM` so each OS candidate stays
> traceable to the specific host it was fingerprinted from. G1 alone loses
> that linkage since `ENVIRONMENT` is a flat category, not per-host.

---

## Rule N0 — OPERATING_SYSTEM data value (formal statement)

> The data value of the `OPERATING_SYSTEM` entity nugget must always equal
> the **exact, unmodified `osmatch@name` value, with no suffix, prefix, or
> disambiguator of any kind.** This holds even in the rare case where two
> sibling subgraphs end up with an identical name (Rule N4) — identical
> names across distinct nodes are permitted and expected in that case, not
> a bug to be engineered around.

This is a hard requirement, not a default that can be overridden by
convenience — every other naming approach considered earlier in this
document (bracketed disambiguators, numeric suffixes, etc.) is superseded
by this rule.

---

## Rule N1 — One OPERATING_SYSTEM nugget per `<osmatch>`

nmap's OS detection returns a **ranked list of candidate guesses**, not a
single answer — each `<osmatch>` is a distinct hypothesis with its own
accuracy score. Each `<osmatch>` element → at least one `OPERATING_SYSTEM`
entity nugget (see Rule N4 for the multi-osclass case), named from
`osmatch.name`, and **all** candidates are preserved — lower-accuracy
guesses are not discarded.

The nugget `name` field is always the **exact, unmodified value** of
`osmatch@name` — no suffixes, no disambiguators. In most cases every
`osmatch` in a host's `<os>` block already has a distinct name, so no
collision handling is needed at all.

**Example — 22/80/443 scan (`45.33.32.156`), 10 candidates:**

| OPERATING_SYSTEM nugget name | accuracy |
|---|---|
| Linux 2.6.18 - 2.6.22 | 94 |
| Linux 2.6.18 | 91 |
| Linux 2.6.32 | 90 |
| Linux 3.2.0 | 90 |
| Linux 2.6.9 - 2.6.18 | 89 |
| Tomato 1.27 - 1.28 (Linux 2.4.20) | 89 |
| MikroTik RouterOS 6.15 (Linux 3.3.5) | 89 |
| Linux 2.6.9 | 89 |
| OpenWrt Kamikaze 7.09 (Linux 2.6.22) | 89 |
| Linux 2.6.5 | 89 |

**Example — top-1000-port scan (`45.33.32.156`), 10 candidates:**

| OPERATING_SYSTEM nugget name | accuracy |
|---|---|
| Linux 2.6.18 - 2.6.22 | 94 |
| Linux 2.6.32 | 90 |
| Linux 2.6.32 or 3.10 | 90 |
| Linux 3.5 | 90 |
| Linux 4.2 | 90 |
| Linux 2.6.18 | 90 |
| Linux 4.8 | 90 |
| Linux 3.2.0 | 90 |
| Synology DiskStation Manager 5.1 | 90 |
| Linux 2.6.35 | 89 |

---

## Rule N2 — Descriptor nuggets via `had` relation

```
OPERATING_SYSTEM --[had]--> OS_TYPE      (osclass @type)
OPERATING_SYSTEM --[had]--> OS_VENDOR    (osclass @vendor)
OPERATING_SYSTEM --[had]--> OS_FAMILY    (osclass @osfamily)
OPERATING_SYSTEM --[had]--> ACCURACY     (osclass @accuracy)
OPERATING_SYSTEM --[had]--> OS_GEN       (osclass @osgen)
```

`had` is used (rather than `contains`) for scalar descriptor values;
`contains` is reserved for structural sub-entities like `CPE_URL`.

`ACCURACY` is read from the `osclass`-level `accuracy` attribute when
present, falling back to the parent `osmatch`-level `accuracy` only if
`osclass` omits it.

**Example — "Linux 2.6.18 - 2.6.22" (accuracy 94):**

| Descriptor nugget | Value |
|---|---|
| OS_TYPE | general purpose |
| OS_VENDOR | Linux |
| OS_FAMILY | Linux |
| ACCURACY | 94 |
| OS_GEN | 2.6.X |

---

## Rule N3 — CPE_URL sub-entity

```
OPERATING_SYSTEM --[contains]--> CPE_URL
```

Sourced from the `<cpe>` element inside each `osclass` block.

---

## Rule N4 — Multiple `<osclass>` per `<osmatch>` → multiple OPERATING_SYSTEM subgraphs

Where an `osmatch` element contains more than one `osclass` child, create a
**separate, complete `OPERATING_SYSTEM` subgraph for each osclass** — not
variant tags on a single nugget. Each subgraph independently follows Rules
N2 and N3 in full (its own `OS_TYPE`/`OS_VENDOR`/`OS_FAMILY`/`ACCURACY`/
`OS_GEN` descriptors and its own `CPE_URL` child), and each is linked to
`ENVIRONMENT` per G1 as its own top-level candidate.

**Name stays exactly `osmatch@name` for every subgraph — no suffix, no
disambiguator.** In the common case (as in both sample scans reviewed —
every `osmatch` in each file has exactly one `osclass`) this never comes up
at all. It only arises for the rarer multi-osclass osmatch, e.g. "Linux
2.6.32 or 3.10" or "Synology DiskStation Manager 5.1" from the top-1000-port
scan. When it does, **two separate nodes are allowed to share the same
name** — they're distinguished by node ID and by their differing
descriptor/CPE children, not by the label.

Two examples from the sample data:

**"Linux 2.6.32 or 3.10" (osmatch accuracy 90) → 2 subgraphs:**

```
ENVIRONMENT --[contains]--> OPERATING_SYSTEM("Linux 2.6.32 or 3.10")   [node A]
  --[had]--> OS_TYPE("general purpose"), OS_VENDOR("Linux"),
             OS_FAMILY("Linux"), ACCURACY("90"), OS_GEN("2.6.X")
  --[contains]--> CPE_URL("cpe:/o:linux:linux_kernel:2.6.32")

ENVIRONMENT --[contains]--> OPERATING_SYSTEM("Linux 2.6.32 or 3.10")   [node B]
  --[had]--> OS_TYPE("general purpose"), OS_VENDOR("Linux"),
             OS_FAMILY("Linux"), ACCURACY("90"), OS_GEN("3.X")
  --[contains]--> CPE_URL("cpe:/o:linux:linux_kernel:3.10")
```

**"Synology DiskStation Manager 5.1" (osmatch accuracy 90) → 2 subgraphs:**

```
ENVIRONMENT --[contains]--> OPERATING_SYSTEM("Synology DiskStation Manager 5.1")   [node A]
  --[had]--> OS_TYPE("storage-misc"), OS_VENDOR("Linux"),
             OS_FAMILY("Linux"), ACCURACY("90"), OS_GEN(null)
  --[contains]--> CPE_URL("cpe:/o:linux:linux_kernel")

ENVIRONMENT --[contains]--> OPERATING_SYSTEM("Synology DiskStation Manager 5.1")   [node B]
  --[had]--> OS_TYPE("storage-misc"), OS_VENDOR("Synology"),
             OS_FAMILY("DiskStation Manager"), ACCURACY("90"), OS_GEN("5.X")
  --[contains]--> CPE_URL("cpe:/a:synology:diskstation_manager:5.1")
```

`[node A]` / `[node B]` above are just this document's way of showing
they're distinct nodes on the page — they are **not** part of the actual
`name` value stored in the graph.

`OS_GEN` may be legitimately `null` for a given subgraph (Synology node A)
— keep the descriptor nugget present with a null value rather than omitting
it, so the schema stays uniform across all subgraphs.

---

## Rule N5 — Cross-scan consistency check (supplementary)

Where the same host is scanned more than once, the top-accuracy
`OPERATING_SYSTEM` candidate should match between scans as a sanity check.

- Top-1000-port scan → top candidate: **"Linux 2.6.18 - 2.6.22"** (94%)
- 22/80/443 scan → top candidate: **"Linux 2.6.18 - 2.6.22"** (94%)

Both agree — good integrity signal. Where repeat scans of the same host
disagree, flag the host for review (possible load-balancing across
different backend hosts, path changes, or fingerprint instability).

---

## Rule P1 — PORT/TRANSPORT containment

```
TRANSPORT --[contains]--> PORT
```

Sourced from each `<port protocol="..." portid="...">` element in `<ports>`.

**Example — top-1000-port scan:**

```
TRANSPORT("tcp") --[contains]--> PORT(22)    → ssh, OpenSSH 6.6.1p1, open
TRANSPORT("tcp") --[contains]--> PORT(80)    → http, Apache httpd 2.4.7, open
TRANSPORT("tcp") --[contains]--> PORT(31337) → tcpwrapped, open
```

**Example — 22/80/443 scan:**

```
TRANSPORT("tcp") --[contains]--> PORT(22)   → tcpwrapped, open
TRANSPORT("tcp") --[contains]--> PORT(80)   → http, Apache httpd 2.4.7, open
TRANSPORT("tcp") --[contains]--> PORT(443)  → https, filtered
```

If a `HOST` has open ports but no `PORT`/`TRANSPORT` containment structure
in the graph, treat this as a parser gap and flag for review before running
P2/P3.

---

## Rule P2 — Reconcile `<os>` probe ports against the `<ports>` list

**This is the core port check.** For each `<portused>` entry inside the
`<os>` block, check whether a matching `PORT` nugget (same port number **and**
same transport/protocol) already exists from Rule P1. If not, **create it**
— including adding a new `TRANSPORT` nugget if the protocol wasn't otherwise
present (e.g. a TCP-only port scan will have no `udp` `TRANSPORT` nugget
until a `portused` entry requires one).

```
<portused state="open"   proto="tcp" portid="22"/>     ← already in PORT graph, no action
<portused state="closed" proto="udp" portid="32689"/>  ← NOT in PORT graph → create it
```

**Example — top-1000-port scan:**

The scan's `scaninfo` shows `protocol="tcp"` only (a TCP connect scan), so
no `udp` `TRANSPORT` nugget exists yet. The `<os>` block references:

```
portused: tcp/22 open    → matches existing PORT(22) under TRANSPORT("tcp") — no action
portused: udp/32689 closed → no match → ADD:
   TRANSPORT("udp") --[contains]--> PORT(32689)   state=closed
```

**Example — 22/80/443 scan:**

```
portused: tcp/80 open     → matches existing PORT(80) under TRANSPORT("tcp") — no action
portused: udp/36975 closed → no match → ADD:
   TRANSPORT("udp") --[contains]--> PORT(36975)   state=closed
```

Newly-added `PORT` nuggets carry a `source: "os_probe"` tag (vs.
`source: "port_scan"` for ones from Rule P1) so downstream consumers can
distinguish "we actually scanned this port as part of the target port list"
from "nmap only touched this port incidentally while fingerprinting the
OS" — the latter is not a general port-scan result and shouldn't be treated
as evidence the port is part of the host's normal open-port profile beyond
that one probe.

---

## Rule P3 — Link the top-accuracy OPERATING_SYSTEM to its probe port(s) via `listens-to`

```
OPERATING_SYSTEM --[listens-to]--> PORT
```

After reconciliation (P2), connect the **single highest-accuracy**
`OPERATING_SYSTEM` nugget for the host to **every `PORT` whose port number
matches a `portused` entry for that host — and only those ports.**

```
match set = { PORT p : p.port_number == portused.portid  for some portused in <os> block }
```

No other filtering applies — the match is purely on port number against
`portused`. This is deliberately narrower than "link to every open port on
the host": the other open ports (e.g. 80/http, 443/https) already carry
their own distinct service identity in the graph, and linking the OS
candidate to them via `listens-to` would incorrectly suggest the OS
fingerprint itself is evidence for those services, when it isn't — the OS
fingerprint's evidence is specifically the probe(s) recorded in
`portused`, nothing more.

**Note on port state:** `portused` entries can be `open` or `closed` (nmap
uses one open and one closed port together as its two OS-detection data
points). This rule links to **both**, since the match criterion is the port
number appearing in `portused`, not its state. This does mean a `listens-to`
edge can point at a `closed` port — that's an accurate reflection of "this
port was used as OS-fingerprint evidence," even though nothing is
literally listening there. If you'd rather encode "was used as evidence"
and "is actually listening" as two different relations, that's a
straightforward split (e.g. `listens-to` for open, `probed-via` for
closed) — flag if you want that added.

**Example — top-1000-port scan:**

`portused`: tcp/22 open, udp/32689 closed.

```
OPERATING_SYSTEM("Linux 2.6.18 - 2.6.22", 94%) --[listens-to]--> PORT(22)    [tcp, open]
OPERATING_SYSTEM("Linux 2.6.18 - 2.6.22", 94%) --[listens-to]--> PORT(32689) [udp, closed]
```

Ports 80 (http) and 31337 (tcpwrapped) are **not** linked — they're not in
`portused`, and already carry their own service identity from Rule P1.

**Example — 22/80/443 scan:**

`portused`: tcp/80 open, udp/36975 closed.

```
OPERATING_SYSTEM("Linux 2.6.18 - 2.6.22", 94%) --[listens-to]--> PORT(80)    [tcp, open]
OPERATING_SYSTEM("Linux 2.6.18 - 2.6.22", 94%) --[listens-to]--> PORT(36975) [udp, closed]
```

Port 22 is **not** linked in this scan, even though it was linked in the
top-1000-port scan above — each scan's `listens-to` edges are derived
independently from that scan's own `portused` block, and the two scans
happened to probe different ports for OS detection.

---

## Supplementary (optional) checks — not part of the core required ruleset

These aren't part of what was specified above, but are useful additions if
you want more anomaly-detection value out of the same data:

- **Registry cross-reference:** compare port number against IANA
  well-known/registered ranges and flag mismatches between detected service
  and canonical expected service (e.g. port 31337/tcpwrapped is a
  historically backdoor-associated non-standard port — not itself proof of
  compromise, but worth flagging when combined with an unconfirmed service
  identity).
## `service_name_history` — explained in detail

This addresses a real inconsistency visible in the sample data: **the same
service, on the same host and port, is labelled differently by nmap
depending on the scan run.**

**What actually happened, concretely:**

| | Top-1000-port scan | 22/80/443 scan |
|---|---|---|
| Port 22 `service@name` | `ssh` | `tcpwrapped` |
| Port 22 `service@conf` | `10` (max confidence) | `8` |
| Port 22 `service@product`/`version` | `OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13` | *(not populated)* |
| `ssh-hostkey` script output | RSA fingerprint `20:3d:2d:44:62:2a:b0:5a:9d:b5:b3:05:14:c2:a6:b2` | **identical** RSA fingerprint |

The `ssh-hostkey` script fired successfully in **both** scans and returned
the exact same host key fingerprints — this is the strongest possible
confirmation (per Ruleset A from earlier in this conversation) that it's
genuinely the same SSH service in both cases. Yet nmap's own `service`
element disagrees on what to call it: `ssh` with full version detection in
one run, generic `tcpwrapped` (nmap's label for "something is listening but
I couldn't positively identify the protocol") in the other.

**Why this happens:** nmap's service/version detection (`-sV`, implied by
`-A`) runs a probe sequence and assigns a confidence score (`conf`,
1–10) based on how many signature checks matched. This can vary
run-to-run for reasons that have nothing to do with the actual service
changing — network jitter affecting how much of a banner is captured in
time, scan timing template (`-T3` in both these scans, so not the cause
here, but `-T` levels commonly cause this), or which specific probes nmap
chose to send in that run's sequence. `tcpwrapped` specifically means nmap
saw a connection get closed immediately after the initial handshake in a
pattern consistent with TCP wrappers or a strict allow-list — a
misidentification that's common against SSH servers that rate-limit or
inspect connections before responding.

**Why this matters for the graph, not just as trivia:** if your parser
naively overwrites the `PORT` nugget's `service_name` field every time it
re-ingests a new scan of the same host, you lose the fact that a
higher-confidence, fully version-identified result exists. A downstream
consumer querying the graph after the second scan would see `tcpwrapped`
and have no idea nmap previously and independently confirmed it as
`OpenSSH 6.6.1p1` with a matched host key. That's a real loss of
information, not a cosmetic one — vulnerability matching, for instance,
needs the `product`/`version` fields, which only the higher-confidence scan
populated.

**The fix — treat it as a history, not a single overwritable field:**

- `service_name` (canonical, top-level field) is always set to the
  **highest-`conf`** observation across all scans of that
  `HOST+PORT+TRANSPORT` combination.
- Every individual scan's observation — regardless of whether it "won" —
  is appended to `service_name_history`, keyed by scan identity, so nothing
  is discarded.

**Example structure for `PORT(22)` on this host, after both scans have been ingested:**

```json
{
  "port_number": 22,
  "transport": "tcp",
  "service_name": "ssh",
  "service_conf": 10,
  "service_product": "OpenSSH",
  "service_version": "6.6.1p1 Ubuntu 2ubuntu2.13",
  "service_name_history": [
    {
      "scan_command": "nmap -sT -A -T3 --top-ports 1000 --open -oX -",
      "scan_start": "2026-06-23T19:03:03Z",
      "service_name": "ssh",
      "service_conf": 10,
      "service_product": "OpenSSH",
      "service_version": "6.6.1p1 Ubuntu 2ubuntu2.13"
    },
    {
      "scan_command": "nmap -sT -A -T3 -p 22,80,443 -oX -",
      "scan_start": "2026-06-23T19:01:10Z",
      "service_name": "tcpwrapped",
      "service_conf": 8,
      "service_product": null,
      "service_version": null
    }
  ]
}
```

Note the second scan actually ran *earlier* in wall-clock time
(19:01:10) than the first (19:03:03) — history entries should be ordered
by `scan_start`, not by which one happened to be ingested first or which
one "won" on confidence, so the history reads as a true timeline.

---

## Full Field Reference

### OPERATING_SYSTEM nugget

| Field | Type | Source |
|---|---|---|
| `name` | string | `osmatch@name`, exact value, unmodified |
| `accuracy` | int | `osclass@accuracy` (fallback: `osmatch@accuracy`) |
| `os_type` | string | `osclass@type` |
| `os_vendor` | string | `osclass@vendor` |
| `os_family` | string | `osclass@osfamily` |
| `os_gen` | string or null | `osclass@osgen` |
| `cpe_url` | string | `osclass/cpe` |
| `is_top_candidate` | bool | true for the single highest-accuracy nugget per host |

### PORT nugget

| Field | Type | Source |
|---|---|---|
| `port_number` | int | `port@portid` or `portused@portid` |
| `transport` | string | `port@protocol` or `portused@proto` |
| `state` | string | `port/state@state` or `portused@state` |
| `service_name` | string or null | `port/service@name` (null if sourced only from `portused`) |
| `service_conf` | int or null | `port/service@conf` |
| `source` | enum(port_scan, os_probe) | Rule P1 vs Rule P2 origin |
| `service_name_history` | array[object] | per-scan observations: `scan_command`, `scan_start`, `service_name`, `service_conf`, `service_product`, `service_version` — see full explanation above |

### TRANSPORT nugget

| Field | Type | Source |
|---|---|---|
| `protocol` | string | `port@protocol` / `portused@proto` (tcp/udp) |
