# Scan Record Host-Correlation Rulesets

A reference for parsing multi-record network scan output (e.g. nmap/nerva-style
JSON) to determine (a) whether separate IPv4/IPv6 records belong to the same
host, (b) whether that host is a standard directly-reachable host, and (c)
whether a CDN/edge vendor sits in front, making origin host count
indeterminate. Includes a full field/schema list for capturing CDN context
when Ruleset C fires.

---

## Background: Worked Example

From a sample scan of `scanme.nmap.org` and `praetorian.com, see below (**APPENDIX: Raw Data Example from Nerva CLI**):

- **scanme.nmap.org** — one IPv4 and one IPv6 address, both returning an
**identical SSH host key fingerprint**
(`SHA256:8iz5L6iZxKJ6YONmad4oMbC+m/+vI9vx5C5f+qTTGDc`) and identical Apache
banners. SSH host keys are generated per-machine and not shared across
independent hosts in normal operation — this is strong evidence of **one
dual-stack host**, not two. In general it is very common to have both ipv4 and ipv6 addresseson the same host in the networks category
- **praetorian.com** — two IPv4 and two IPv6 addresses, all on port 443, all
reporting `Server: cloudflare`, matching CSP/HSTS headers, and `CF-Ray` IDs
ending in `-SYD` (a Cloudflare Sydney point-of-presence code). These are
**Cloudflare edge/anycast IPs, not origin servers**. TLS terminates at
Cloudflare, so there is no way to fingerprint the real origin from this
data — the number of IPs returned reflects Cloudflare's edge
infrastructure, not the number of machines running behind it. Any
"detected technology" tags here (e.g. `nginx`, `checkpoint-gateway`,
`zyxel-firewall`) are best treated as edge-fingerprinting artifacts rather
than confirmed origin infrastructure.

This is the general shape of the problem: **identity should be established
from durable machine-specific artifacts (keys, certs), not from
address/header similarity alone — and CDN detection must run before any
host-count conclusion is trusted.**

---



## Ruleset A — Are IPv4 + IPv6 records the same system?

Run these checks in order. Each is a **strong signal** (near-certain) or
**weak signal** (contributory only). Strong signals alone can confirm a
match; weak signals need to accumulate.

- **A1. Identical SSH host key (strong)**
Same `host_key` + `host_key_type` across records → same system. SSH keys
are generated per-install and are not shared across independent hosts
under normal operation.
- **A2. Identical TLS certificate (strong)**
Same certificate serial number + public key (not just same SAN list) →
same system, *unless* the cert is a wildcard/SAN cert served from a shared
load-balancer pool (see Ruleset C — this is where it gets ambiguous).
- **A3. Identical service banner + version string, byte-for-byte
(moderate-strong)**
Same banner (e.g. `SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13`) on both
address families. Strong when combined with A1; on its own it's moderate,
since identical software versions can appear on different hosts (e.g. same
golden image, or a cluster).
- **A4. Identical response headers, byte-for-byte ordering + values
(weak-moderate)**
Same `Server`, header ordering, same custom headers (`X-*`), same error
page structure. Weak alone (could be same CDN/config template); moderate
when several distinctive headers match together.
- **A5. DNS co-resolution (weak, contextual)**
Both A and AAAA records resolve from the *same* hostname query. This tells
you the DNS answer groups them, not that they're the same machine —
dual-stack hosts and load-balanced pools both do this. Use only as a
prerequisite/filter, not as evidence.
- **A6. Rejection condition — divergent identity artifacts (overrides
everything)**
If A1 or A2 *differ* between the IPv4 and IPv6 record, treat as
**different systems**, regardless of how many weak signals match.
Divergent host keys/certs are the strongest possible signal of separate
machines.

**Decision logic:**

```
IF A1 matches OR A2 matches (non-wildcard) → SAME_SYSTEM (confidence: high)
ELSE IF A3 matches AND (A4 matches on ≥2 distinctive headers) → SAME_SYSTEM (confidence: medium)
ELSE IF only A4/A5 match → INCONCLUSIVE (flag for manual review)
ELSE → DIFFERENT_SYSTEMS
```

---



## Ruleset B — Is a confirmed same-system pair a "standard" (non-fronted) host?

Once Ruleset A says "same system," classify whether it's a standard origin
host (not sitting behind a reverse proxy/CDN).

- **B1. Presence of a durable machine identifier (required for "standard")**
At least one of: SSH host key, TLS cert with a non-shared/non-wildcard
key, or a unique non-generic banner (build ID, hostname leak, uptime
counter). No durable identifier → cannot classify as standard; fall to
Ruleset C.
- **B2. Port profile consistent with an origin, not an edge (supporting)**
Presence of non-web management ports (22/SSH, 3389/RDP, database ports,
etc.) alongside 80/443. CDNs/edges almost never expose SSH or DB ports on
the same IP as the proxied site.
- **B3. TLS certificate issued directly to the host's own domain, non-shared
SAN pool (supporting)**
Cert SAN list is narrow (this domain + close variants only), not a broad
multi-tenant SAN shared across unrelated domains.
- **B4. Response latency / TTL characteristics (optional, if available)**
Consistent low-variance latency and normal IP TTL (~64/128 typical OS
defaults, not artificially rewritten) suggest direct host response, not
proxy relay. Weak signal, use only as a tie-breaker.

**Decision logic:**

```
IF B1 satisfied AND Ruleset C = NOT_FRONTED → STANDARD_HOST
ELSE IF B1 satisfied AND Ruleset C = FRONTED → ORIGIN_HOST_BEHIND_PROXY (not directly reachable/countable from this IP)
ELSE → UNKNOWN (insufficient identity data to classify)
```

---



## Ruleset C — Is a cloud/edge vendor sitting in front (host count unknowable)?

This should run **before** you trust any host-count conclusion from A/B.
Treat any match here as reason to flag the record as "edge/proxy — origin
count indeterminate."

- **C1. Known provider header/banner signatures (strong)**
Match `Server`, `Via`, `X-Served-By`, `X-CDN`, `CF-*`, `X-Amz-Cf-*`,
`X-Fastly*`, `X-Akamai*`, `X-Vercel*`, `X-Sucuri*`,
`X-Powered-By: *WPEngine*` etc. against a maintained provider signature
list. Any match → strong indicator of fronting. Keep this list
vendor-agnostic and updatable (Cloudflare, Fastly, Akamai, CloudFront,
Vercel, Netlify, Sucuri, Imperva, StackPath, Google Cloud CDN/LB, Azure
Front Door, etc.).
- **C2. ASN/IP range ownership lookup (strong)**
Resolve the IP's ASN/WHOIS owner. If it belongs to a known CDN/cloud-proxy
AS (not an ISP or the target org's own AS) → strong indicator of fronting.
This is the most reliable automatable check — build an ASN allowlist of
known edge providers and check membership per-record.
- **C3. Anycast pattern — many geographically-plausible IPs for one hostname,
each with edge-node metadata (strong)**
If the record includes geo/PoP identifiers (e.g. Cloudflare's `CF-Ray`
suffix, Fastly's POP codes, Akamai edge hostnames) that vary between
requests to the *same* hostname → confirms anycast edge, not distinct
origin hosts.
- **C4. TLS certificate is multi-tenant / shared SAN (moderate-strong)**
Certificate SAN list contains many unrelated domains not belonging to the
same organization → shared edge certificate, classic CDN behavior.
- **C5. Absence of any non-web/non-proxy ports (moderate)**
Only 80/443 (or 443 + QUIC/443-udp) open, nothing else — consistent with
edge-only exposure, though not conclusive alone (some real hosts are also
locked down).
- **C6. TTL/latency anomalies suggesting a relay hop (weak)**
Response timing pattern consistent with proxying (an extra hop's worth of
RTT relative to expected geo-distance), or IP TTL values inconsistent with
common OS defaults.

**Decision logic:**

```
IF C1 matches OR C2 matches (ASN in known-edge-provider list) → FRONTED (confidence: high)
    → set host_count = "indeterminate", origin_ip = null
ELSE IF C3 matches OR C4 matches → FRONTED (confidence: medium-high)
ELSE IF (C5 matches) AND (2+ weak signals) → FRONTED (confidence: medium, flag for review)
ELSE → NOT_FRONTED
```

---



## Chaining the rulesets in a parser

```
for each hostname:
    group records by hostname
    for each pair of records within group:
        run Ruleset A → same_system?
    for each same_system group:
        run Ruleset C first (fronting check)
        if FRONTED:
            mark group as "edge cluster — origin host count unknown"
            record provider name (from C1/C2 match) if identified
            do NOT attempt Ruleset B
        else:
            run Ruleset B → classify as STANDARD_HOST or UNKNOWN
    output: for each hostname, either:
        - N confirmed standard hosts (with identity evidence cited)
        - "fronted by <provider/unknown-provider>, origin count indeterminate"
```

**Practical notes:**

- Keep the ASN and header-signature lists as external, updatable config, not
hardcoded — new CDN/edge vendors appear constantly, and this is the
single highest-value maintenance task for keeping the ruleset accurate.
- Always prefer strong signals (A1/A2, C1/C2) over accumulated weak ones.
Weak signals are individually easy for infrastructure changes (config
templates, shared images) to produce false matches or false negatives.
- Log which rule fired, not just the verdict — when C1 vs C2 vs C3 disagree
(rare but happens, e.g. a self-hosted reverse proxy that isn't a known
commercial CDN), a human reviewer needs to see the evidence trail.

---



## What a CDN-fronted record can still tell you

Once a record is classified as `FRONTED`, it isn't a dead end — a fair
amount of edge/vendor metadata is still extractable and worth capturing.

### 1. Provider identity (beyond just the vendor name)

- **Vendor** — e.g. Cloudflare, Fastly, Akamai, CloudFront, Vercel, Azure
Front Door (from C1/C2 match).
- **Product line, if inferable** — e.g. Cloudflare plain proxy vs Workers vs
Pages vs APO (visible in the sample data as `Cf-Apo-Via: origin,resnok`)
vs Access/Zero Trust. This tells you *what kind* of edge logic sits in
front, not just "a CDN."
- **Confidence level** — record whether vendor ID came from a strong signal
(ASN, dedicated header) or a weaker one (generic `Server` string alone),
since header strings can occasionally be spoofed or reused by self-hosted
proxies mimicking a vendor.



### 2. Point-of-presence (PoP) / edge-node data

- **PoP location code** — e.g. `Cf-Ray: a13b857a1bf0ccf3-SYD` → `-SYD`
identifies the Sydney edge node. Fastly, Akamai, and others embed similar
codes (`X-Served-By`, `X-Cache` with POP tags).
- **Edge-node ID / ray ID** — useful for correlating which physical/virtual
edge machine served a given request, and for spotting load-balancing
across multiple PoPs.
- **Anycast vs unicast inference** — if repeated scans of the same hostname
return different PoP codes for the same IP over time, that IP is
anycast-routed, reinforcing "this is edge infrastructure."



### 3. Caching and routing behavior

- **Cache status** — e.g. `Cf-Cache-Status: BYPASS/HIT/MISS/DYNAMIC` — tells
you the CDN's caching decision for that request.
- **Edge vs origin timing breakdown** — e.g.
`Server-Timing: cfEdge;dur=217,cfOrigin;dur=0`. A non-zero origin duration
confirms the edge actually round-tripped to a real backend for that
request (vs. cache/static/Workers response).
- **HTTP protocol features offered at the edge** — e.g.
`Alt-Svc: h3=":443"` shows edge-negotiated HTTP/3/QUIC support, not
necessarily something the origin itself supports.

## Extending our Current Ontology with Concepts Brought by Nerva

You need to read through the Current Ontology first, before we describe the extensions

### 4. Security/config posture enforced by the CDN

- **HSTS policy** — max-age, preload, includeSubDomains.
- **CSP contents** — often leaks a genuinely useful list of other
first-/third-party domains the org uses (analytics, forms, video hosting,
chat widgets) — good OSINT independent of origin host count.
- **Reporting endpoints** — `Nel` / `Report-To` headers reveal active
Network Error Logging config.
- **WAF/bot-management fingerprints** — distinct headers or challenge-page
markers when WAF/bot protection is active; worth its own signature list.



### 5. What you still cannot determine

Explicitly null these out when `FRONTED`, so downstream consumers don't
infer them by accident:

- Number of origin hosts
- Origin OS/software stack (edge-fingerprinting tags like `nginx`,
`checkpoint-gateway` are very likely edge-side artifacts, not real origin
infrastructure)
- Origin IP address/geolocation
- Origin uptime/patch state

---

## Conversion to SpiderFeet Ontology


## Full Field / Schema Reference



### Identity & classification (Rulesets A/B/C outputs)


| Field                       | Type                                                               | Notes                                   |
| --------------------------- | ------------------------------------------------------------------ | --------------------------------------- |
| `record_id`                 | string                                                             | unique ID for this scan record          |
| `hostname`                  | string                                                             | queried hostname                        |
| `ip_address`                | string                                                             | IPv4 or IPv6                            |
| `ip_version`                | enum(4,6)                                                          |                                         |
| `port`                      | int                                                                |                                         |
| `protocol`                  | string                                                             | ssh, http, https, etc.                  |
| `same_system_group_id`      | string                                                             | groups records matched by Ruleset A     |
| `same_system_confidence`    | enum(high, medium, low, inconclusive)                              | which A-rule fired                      |
| `same_system_evidence`      | string                                                             | e.g. "A1: matching SSH host key"        |
| `host_classification`       | enum(standard_host, origin_behind_proxy, fronted_unknown, unknown) | Ruleset B/C outcome                     |
| `classification_confidence` | enum(high, medium, low)                                            |                                         |
| `classification_rule_fired` | string                                                             | e.g. "C1: Server header match", "B1+B2" |




### Durable machine identity (Ruleset A/B inputs)


| Field                      | Type                                         | Notes                                |
| -------------------------- | -------------------------------------------- | ------------------------------------ |
| `ssh_host_key`             | string                                       | raw key                              |
| `ssh_host_key_type`        | string                                       | e.g. ecdsa-sha2-nistp256             |
| `ssh_host_key_fingerprint` | string                                       | SHA256:...                           |
| `tls_cert_serial`          | string                                       |                                      |
| `tls_cert_public_key_hash` | string                                       |                                      |
| `tls_cert_san_list`        | array[string]                                |                                      |
| `tls_cert_san_scope`       | enum(narrow_own_domain, multi_tenant_shared) | supports B3/C4                       |
| `service_banner`           | string                                       | raw banner string                    |
| `banner_hash`              | string                                       | normalized hash for quick comparison |
| `open_ports`               | array[int]                                   | full port list per IP                |
| `non_web_ports_present`    | bool                                         | supports B2                          |




### CDN / edge vendor identity (Ruleset C outputs)


| Field                   | Type                    | Notes                                           |
| ----------------------- | ----------------------- | ----------------------------------------------- |
| `cdn_vendor`            | string                  | e.g. "Cloudflare"                               |
| `cdn_vendor_confidence` | enum(high, medium, low) |                                                 |
| `cdn_detection_signal`  | array[string]           | which signatures matched: header names, ASN     |
| `cdn_asn`               | int                     | resolved ASN of the IP                          |
| `cdn_asn_org`           | string                  | WHOIS org name for the ASN                      |
| `cdn_product_hint`      | string                  | e.g. "APO", "Workers", "Pages", null if unknown |




### Edge node / PoP data


| Field               | Type   | Notes                                                 |
| ------------------- | ------ | ----------------------------------------------------- |
| `pop_code`          | string | e.g. "SYD"                                            |
| `edge_node_id`      | string | e.g. Cf-Ray value                                     |
| `anycast_suspected` | bool   | true if multiple PoP codes seen for same IP over time |




### Caching & routing behavior


| Field                | Type          | Notes                                   |
| -------------------- | ------------- | --------------------------------------- |
| `cache_status`       | string        | HIT, MISS, BYPASS, DYNAMIC, etc.        |
| `edge_duration_ms`   | float         | from Server-Timing                      |
| `origin_duration_ms` | float         | from Server-Timing; null if unavailable |
| `protocols_offered`  | array[string] | e.g. ["h3", "h2"] from Alt-Svc          |




### Security/config posture


| Field                         | Type          | Notes                            |
| ----------------------------- | ------------- | -------------------------------- |
| `hsts_enabled`                | bool          |                                  |
| `hsts_max_age`                | int           | seconds                          |
| `hsts_preload`                | bool          |                                  |
| `hsts_include_subdomains`     | bool          |                                  |
| `csp_present`                 | bool          |                                  |
| `csp_third_party_domains`     | array[string] | extracted from CSP directives    |
| `nel_active`                  | bool          |                                  |
| `nel_report_endpoints`        | array[string] |                                  |
| `waf_bot_management_detected` | bool          |                                  |
| `waf_vendor_hint`             | string        | if distinguishable from base CDN |




### HTTP response context (general, not CDN-specific)


| Field                  | Type   | Notes            |
| ---------------------- | ------ | ---------------- |
| `status_code`          | int    |                  |
| `response_headers_raw` | object | full header dump |
| `redirect_location`    | string | if 3xx           |
| `server_header`        | string | raw Server value |




### Suppressed/withheld origin data (explicit nulls when fronted)


| Field                           | Type                  | Notes                                                                  |
| ------------------------------- | --------------------- | ---------------------------------------------------------------------- |
| `origin_host_count`             | int or null           | null when `host_classification = fronted_unknown`                      |
| `origin_ip`                     | string or null        |                                                                        |
| `origin_technologies`           | array[string] or null | e.g. nginx/checkpoint tags — suppressed, not deleted                   |
| `origin_fingerprint_suppressed` | bool                  | true if candidate origin data existed but was withheld due to fronting |
| `origin_fingerprint_raw`        | object or null        | store raw data here for audit, but exclude from host-count logic       |




### Scan/record metadata (housekeeping)


| Field                 | Type     | Notes                                              |
| --------------------- | -------- | -------------------------------------------------- |
| `scan_timestamp`      | datetime |                                                    |
| `scan_tool`           | string   | e.g. "nerva"                                       |
| `scan_command`        | string   | raw invocation                                     |
| `rule_engine_version` | string   | version of your A/B/C ruleset, for reproducibility |




### Example output snippet

```json
"cdn_context": {
  "vendor": "Cloudflare",
  "vendor_confidence": "high",
  "product_hint": "APO",
  "pop_code": "SYD",
  "edge_node_id": "a13b857a1bf0ccf3",
  "cache_status": "BYPASS",
  "edge_duration_ms": 217,
  "origin_duration_ms": 0,
  "protocols_offered": ["h3"],
  "hsts": true,
  "nel_active": true,
  "csp_third_parties": ["googletagmanager.com", "greenhouse.io", "hubspot.com"],
  "origin_host_count": null,
  "origin_fingerprint_suppressed": true
}
```



## APPENDIX: Raw Data Example from Nerva CLI

```json
{
  "schema": "nerva_fingerprint_v1",
  "tool": "nerva",
  "scenario": "Multi-target list file",
  "scenario_id": "tcp_list_file_json",
  "target": "scanme.nmap.org + praetorian.com",
  "command": "nerva -l .seed/scripts/cli_corpus/fixtures/nerva_targets.txt --json -w 8000",
  "runtime": "windows",
  "started_at": "2026-06-30T07:40:07.243348+00:00",
  "duration_s": 23.171,
  "exit_code": 0,
  "fingerprint_summary_lines": 8,
  "text_role": "one line per discovered service/IP (pipe-friendly summary)",
  "structured_role": "full JSON metadata per record (headers, findings, etc.)",
  "records": [
    {
      "host": "scanme.nmap.org",
      "ip": "2600:3c01::f03c:91ff:fe18:bb2f",
      "port": 22,
      "protocol": "ssh",
      "tls": false,
      "transport": "tcp",
      "metadata": {
        "banner": "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13\r\n",
        "password_auth_enabled": true,
        "algo": "map[CiphersClientServer:aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se CiphersServerClient:aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se CompressionClientServer:none,zlib@openssh.com CompressionServerClient:none,zlib@openssh.com Cookie:5431de43c494d68ee84d57df228d0d69 KexAlgos:curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 LanguagesClientServer: LanguagesServerClient: MACsClientServer:hmac-md5-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-ripemd160-etm@openssh.com,hmac-sha1-96-etm@openssh.com,hmac-md5-96-etm@openssh.com,hmac-md5,hmac-sha1,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96 MACsServerClient:hmac-md5-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-ripemd160-etm@openssh.com,hmac-sha1-96-etm@openssh.com,hmac-md5-96-etm@openssh.com,hmac-md5,hmac-sha1,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96 ServerHostKeyAlgos:ssh-rsa,ssh-dss,ecdsa-sha2-nistp256,ssh-ed25519]",
        "host_key": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMD46g67x6yWNjjQJnXhiz/TskHrqQ0uPcOspFrIYW382uOGzmWDZCFV8FbFwQyH90u+j0Qr1SGNAxBZMhOQ8pc=",
        "host_key_type": "ecdsa-sha2-nistp256",
        "host_key_fingerprint": "SHA256:8iz5L6iZxKJ6YONmad4oMbC+m/+vI9vx5C5f+qTTGDc"
      },
      "security_findings": [
        {
          "id": "ssh-weak-cipher",
          "severity": "low",
          "description": "SSH server offers weak encryption algorithms",
          "evidence": "3des-cbc,arcfour,arcfour128,arcfour256,blowfish-cbc,cast128-cbc"
        },
        {
          "id": "ssh-weak-kex",
          "severity": "low",
          "description": "SSH server offers weak key exchange algorithms",
          "evidence": "diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1"
        },
        {
          "id": "ssh-weak-mac",
          "severity": "low",
          "description": "SSH server offers weak MAC algorithms",
          "evidence": "hmac-md5,hmac-md5-96,hmac-md5-96-etm@openssh.com,hmac-md5-etm@openssh.com,hmac-sha1-96,hmac-sha1-96-etm@openssh.com"
        },
        {
          "id": "ssh-password-auth",
          "severity": "medium",
          "description": "SSH server allows password authentication, enabling brute-force attacks"
        }
      ]
    },
    {
      "host": "scanme.nmap.org",
      "ip": "45.33.32.156",
      "port": 22,
      "protocol": "ssh",
      "tls": false,
      "transport": "tcp",
      "metadata": {
        "banner": "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13\r\n",
        "password_auth_enabled": true,
        "algo": "map[CiphersClientServer:aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se CiphersServerClient:aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,arcfour,rijndael-cbc@lysator.liu.se CompressionClientServer:none,zlib@openssh.com CompressionServerClient:none,zlib@openssh.com Cookie:47a3856a7d71dd199830477d9f83349c KexAlgos:curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 LanguagesClientServer: LanguagesServerClient: MACsClientServer:hmac-md5-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-ripemd160-etm@openssh.com,hmac-sha1-96-etm@openssh.com,hmac-md5-96-etm@openssh.com,hmac-md5,hmac-sha1,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96 MACsServerClient:hmac-md5-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-ripemd160-etm@openssh.com,hmac-sha1-96-etm@openssh.com,hmac-md5-96-etm@openssh.com,hmac-md5,hmac-sha1,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-ripemd160,hmac-ripemd160@openssh.com,hmac-sha1-96,hmac-md5-96 ServerHostKeyAlgos:ssh-rsa,ssh-dss,ecdsa-sha2-nistp256,ssh-ed25519]",
        "host_key": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMD46g67x6yWNjjQJnXhiz/TskHrqQ0uPcOspFrIYW382uOGzmWDZCFV8FbFwQyH90u+j0Qr1SGNAxBZMhOQ8pc=",
        "host_key_type": "ecdsa-sha2-nistp256",
        "host_key_fingerprint": "SHA256:8iz5L6iZxKJ6YONmad4oMbC+m/+vI9vx5C5f+qTTGDc"
      },
      "security_findings": [
        {
          "id": "ssh-weak-cipher",
          "severity": "low",
          "description": "SSH server offers weak encryption algorithms",
          "evidence": "3des-cbc,arcfour,arcfour128,arcfour256,blowfish-cbc,cast128-cbc"
        },
        {
          "id": "ssh-weak-kex",
          "severity": "low",
          "description": "SSH server offers weak key exchange algorithms",
          "evidence": "diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1"
        },
        {
          "id": "ssh-weak-mac",
          "severity": "low",
          "description": "SSH server offers weak MAC algorithms",
          "evidence": "hmac-md5,hmac-md5-96,hmac-md5-96-etm@openssh.com,hmac-md5-etm@openssh.com,hmac-sha1-96,hmac-sha1-96-etm@openssh.com"
        },
        {
          "id": "ssh-password-auth",
          "severity": "medium",
          "description": "SSH server allows password authentication, enabling brute-force attacks"
        }
      ]
    },
    {
      "host": "scanme.nmap.org",
      "ip": "45.33.32.156",
      "port": 80,
      "protocol": "http",
      "tls": false,
      "transport": "tcp",
      "version": "Apache/2.4.7 (Ubuntu)",
      "metadata": {
        "status": "200 OK",
        "status_code": 200,
        "response_headers": {
          "Accept-Ranges": [
            "bytes"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Server": [
            "Apache/2.4.7 (Ubuntu)"
          ],
          "Vary": [
            "Accept-Encoding"
          ]
        },
        "technologies": [
          "Apache HTTP Server:2.4.7",
          "Ubuntu",
          "apache_httpd:2.4.7"
        ],
        "cpes": [
          "cpe:2.3:a:apache:http_server:*:*:*:*:*:*:*:*",
          "cpe:2.3:o:canonical:ubuntu_linux:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:apache:http_server:2.4.7:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "apache_httpd": {
            "os": "Ubuntu"
          }
        }
      }
    },
    {
      "host": "scanme.nmap.org",
      "ip": "2600:3c01::f03c:91ff:fe18:bb2f",
      "port": 80,
      "protocol": "http",
      "tls": false,
      "transport": "tcp",
      "version": "Apache/2.4.7 (Ubuntu)",
      "metadata": {
        "status": "200 OK",
        "status_code": 200,
        "response_headers": {
          "Accept-Ranges": [
            "bytes"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Server": [
            "Apache/2.4.7 (Ubuntu)"
          ],
          "Vary": [
            "Accept-Encoding"
          ]
        },
        "technologies": [
          "Ubuntu",
          "Apache HTTP Server:2.4.7",
          "apache_httpd:2.4.7"
        ],
        "cpes": [
          "cpe:2.3:o:canonical:ubuntu_linux:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:apache:http_server:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:apache:http_server:2.4.7:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "apache_httpd": {
            "os": "Ubuntu"
          }
        }
      }
    },
    {
      "host": "praetorian.com",
      "ip": "172.66.43.196",
      "port": 443,
      "protocol": "https",
      "tls": true,
      "transport": "tcp",
      "version": "cloudflare",
      "metadata": {
        "status": "301 Moved Permanently",
        "status_code": 301,
        "response_headers": {
          "Alt-Svc": [
            "h3=\":443\"; ma=86400"
          ],
          "Cf-Apo-Via": [
            "origin,resnok"
          ],
          "Cf-Cache-Status": [
            "BYPASS"
          ],
          "Cf-Ray": [
            "a13b857a1bf0ccf3-SYD"
          ],
          "Connection": [
            "keep-alive"
          ],
          "Content-Security-Policy": [
            "frame-src 'self' blob: *.googletagmanager.com *.greenhouse.io online.fliphtml5.com app.hubspot.com player.vimeo.com boards.greenhouse.io www.praetorian.com *.google.com *.youtube.com *.doubleclick.net *.twitter.com *.hsforms.com *.hsforms.net disqus.com *.vimeo.com vars.hotjar.com mlb.praetorian.com js.driftt.com widget.drift.com; frame-ancestors 'self' https://www.praetorian.com;"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Location": [
            "https://www.praetorian.com/"
          ],
          "Nel": [
            "{\"report_to\":\"cf-nel\",\"success_fraction\":0.0,\"max_age\":604800}"
          ],
          "Report-To": [
            "{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=AXGYHtBVh9RySQ8w6ey3%2FSxk2NILeH2qZrU4j6mCh7Rt7kUlg79xhOS9%2FDs59u0Z4Ze9UZSBbIx8X6NseGiN9BakOPoqyLpAa6c671c2g1hfNBMrvbYzmUnUCqtdwylZ\"}]}"
          ],
          "Server": [
            "cloudflare"
          ],
          "Server-Timing": [
            "cfCacheStatus;desc=\"BYPASS\"",
            "cfEdge;dur=217,cfOrigin;dur=0"
          ],
          "Strict-Transport-Security": [
            "max-age=31536000; includeSubDomains; preload"
          ],
          "X-Content-Type-Options": [
            "nosniff"
          ],
          "X-Frame-Options": [
            "SAMEORIGIN"
          ],
          "X-Xss-Protection": [
            "1; mode=block"
          ]
        },
        "technologies": [
          "Cloudflare",
          "HSTS",
          "HTTP/3",
          "Cloudflare Browser Insights",
          "checkpoint-gateway",
          "nginx",
          "zyxel-firewall"
        ],
        "cpes": [
          "cpe:2.3:o:checkpoint:gaia:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:f5:nginx:*:*:*:*:*:*:*:*",
          "cpe:2.3:o:zyxel:zld_firmware:*:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "checkpoint-gateway": {
            "product": "Security Gateway",
            "vendor": "Check Point"
          },
          "nginx": {
            "detection_method": "error_page",
            "product": "Nginx",
            "server_header": "cloudflare",
            "variant": "nginx",
            "vendor": "F5"
          },
          "zyxel-firewall": {
            "product": "Zyxel Firewall",
            "vendor": "Zyxel"
          }
        }
      }
    },
    {
      "host": "praetorian.com",
      "ip": "2606:4700:3108::ac42:2bc4",
      "port": 443,
      "protocol": "https",
      "tls": true,
      "transport": "tcp",
      "version": "cloudflare",
      "metadata": {
        "status": "301 Moved Permanently",
        "status_code": 301,
        "response_headers": {
          "Alt-Svc": [
            "h3=\":443\"; ma=86400"
          ],
          "Cf-Apo-Via": [
            "origin,resnok"
          ],
          "Cf-Cache-Status": [
            "BYPASS"
          ],
          "Cf-Ray": [
            "a13b857a18212def-SYD"
          ],
          "Connection": [
            "keep-alive"
          ],
          "Content-Security-Policy": [
            "frame-src 'self' blob: *.googletagmanager.com *.greenhouse.io online.fliphtml5.com app.hubspot.com player.vimeo.com boards.greenhouse.io www.praetorian.com *.google.com *.youtube.com *.doubleclick.net *.twitter.com *.hsforms.com *.hsforms.net disqus.com *.vimeo.com vars.hotjar.com mlb.praetorian.com js.driftt.com widget.drift.com; frame-ancestors 'self' https://www.praetorian.com;"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Location": [
            "https://www.praetorian.com/"
          ],
          "Nel": [
            "{\"report_to\":\"cf-nel\",\"success_fraction\":0.0,\"max_age\":604800}"
          ],
          "Report-To": [
            "{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=sfLMiIVk9m7ySwRveM22RYigQ7229RWXCtyBlBMeXJtYM5Won0We5SGJwvAo6UegwAmsxgcO4u6Jnt5P0KOw0lcebWLtYW9oXe%2FkDDBIaWvCnrMv%2Fiu3jjmNjsmSf7CVE85e3wdR2nzRF%2Frr\"}]}"
          ],
          "Server": [
            "cloudflare"
          ],
          "Server-Timing": [
            "cfCacheStatus;desc=\"BYPASS\"",
            "cfEdge;dur=228,cfOrigin;dur=0"
          ],
          "Strict-Transport-Security": [
            "max-age=31536000; includeSubDomains; preload"
          ],
          "X-Content-Type-Options": [
            "nosniff"
          ],
          "X-Frame-Options": [
            "SAMEORIGIN"
          ],
          "X-Xss-Protection": [
            "1; mode=block"
          ]
        },
        "technologies": [
          "Cloudflare",
          "HSTS",
          "HTTP/3",
          "Cloudflare Browser Insights",
          "zyxel-firewall",
          "nginx",
          "checkpoint-gateway"
        ],
        "cpes": [
          "cpe:2.3:o:zyxel:zld_firmware:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:f5:nginx:*:*:*:*:*:*:*:*",
          "cpe:2.3:o:checkpoint:gaia:*:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "checkpoint-gateway": {
            "product": "Security Gateway",
            "vendor": "Check Point"
          },
          "nginx": {
            "detection_method": "error_page",
            "product": "Nginx",
            "server_header": "cloudflare",
            "variant": "nginx",
            "vendor": "F5"
          },
          "zyxel-firewall": {
            "product": "Zyxel Firewall",
            "vendor": "Zyxel"
          }
        }
      }
    },
    {
      "host": "praetorian.com",
      "ip": "172.66.40.60",
      "port": 443,
      "protocol": "https",
      "tls": true,
      "transport": "tcp",
      "version": "cloudflare",
      "metadata": {
        "status": "301 Moved Permanently",
        "status_code": 301,
        "response_headers": {
          "Alt-Svc": [
            "h3=\":443\"; ma=86400"
          ],
          "Cf-Apo-Via": [
            "origin,resnok"
          ],
          "Cf-Cache-Status": [
            "BYPASS"
          ],
          "Cf-Ray": [
            "a13b857a182aaaf0-SYD"
          ],
          "Connection": [
            "keep-alive"
          ],
          "Content-Security-Policy": [
            "frame-src 'self' blob: *.googletagmanager.com *.greenhouse.io online.fliphtml5.com app.hubspot.com player.vimeo.com boards.greenhouse.io www.praetorian.com *.google.com *.youtube.com *.doubleclick.net *.twitter.com *.hsforms.com *.hsforms.net disqus.com *.vimeo.com vars.hotjar.com mlb.praetorian.com js.driftt.com widget.drift.com; frame-ancestors 'self' https://www.praetorian.com;"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Location": [
            "https://www.praetorian.com/"
          ],
          "Nel": [
            "{\"report_to\":\"cf-nel\",\"success_fraction\":0.0,\"max_age\":604800}"
          ],
          "Report-To": [
            "{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=2LHxmZiJG5oOCoHABCASpNzqJq6tmzotQ%2FJemm%2FTDEK8CkcigYsGh8lUhkVLfQl7wCuiTt8QEq1COyjCdOWa8LKC7W20vkqt5jt6OK7FstKf88xV8NdLQ7ely7N%2Bsgi7\"}]}"
          ],
          "Server": [
            "cloudflare"
          ],
          "Server-Timing": [
            "cfCacheStatus;desc=\"BYPASS\"",
            "cfEdge;dur=276,cfOrigin;dur=0"
          ],
          "Strict-Transport-Security": [
            "max-age=31536000; includeSubDomains; preload"
          ],
          "X-Content-Type-Options": [
            "nosniff"
          ],
          "X-Frame-Options": [
            "SAMEORIGIN"
          ],
          "X-Xss-Protection": [
            "1; mode=block"
          ]
        },
        "technologies": [
          "Cloudflare",
          "HSTS",
          "HTTP/3",
          "Cloudflare Browser Insights",
          "zyxel-firewall",
          "checkpoint-gateway",
          "nginx"
        ],
        "cpes": [
          "cpe:2.3:o:zyxel:zld_firmware:*:*:*:*:*:*:*:*",
          "cpe:2.3:o:checkpoint:gaia:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:f5:nginx:*:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "checkpoint-gateway": {
            "product": "Security Gateway",
            "vendor": "Check Point"
          },
          "nginx": {
            "detection_method": "error_page",
            "product": "Nginx",
            "server_header": "cloudflare",
            "variant": "nginx",
            "vendor": "F5"
          },
          "zyxel-firewall": {
            "product": "Zyxel Firewall",
            "vendor": "Zyxel"
          }
        }
      }
    },
    {
      "host": "praetorian.com",
      "ip": "2606:4700:3108::ac42:283c",
      "port": 443,
      "protocol": "https",
      "tls": true,
      "transport": "tcp",
      "version": "cloudflare",
      "metadata": {
        "status": "301 Moved Permanently",
        "status_code": 301,
        "response_headers": {
          "Alt-Svc": [
            "h3=\":443\"; ma=86400"
          ],
          "Cf-Apo-Via": [
            "origin,resnok"
          ],
          "Cf-Cache-Status": [
            "BYPASS"
          ],
          "Cf-Ray": [
            "a13b857a1be8561f-SYD"
          ],
          "Connection": [
            "keep-alive"
          ],
          "Content-Security-Policy": [
            "frame-src 'self' blob: *.googletagmanager.com *.greenhouse.io online.fliphtml5.com app.hubspot.com player.vimeo.com boards.greenhouse.io www.praetorian.com *.google.com *.youtube.com *.doubleclick.net *.twitter.com *.hsforms.com *.hsforms.net disqus.com *.vimeo.com vars.hotjar.com mlb.praetorian.com js.driftt.com widget.drift.com; frame-ancestors 'self' https://www.praetorian.com;"
          ],
          "Content-Type": [
            "text/html"
          ],
          "Date": [
            "Tue, 30 Jun 2026 07:40:11 GMT"
          ],
          "Location": [
            "https://www.praetorian.com/"
          ],
          "Nel": [
            "{\"report_to\":\"cf-nel\",\"success_fraction\":0.0,\"max_age\":604800}"
          ],
          "Report-To": [
            "{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=3HPUBTKg1Pb6isxzaHQPJCuiOEjei3a1PFJdcqsVH1yUMdnGUuI6Ta3j4GkGSI70Q%2FUaJtFe8BATnLky8thcPwdfcmEsLTfIpHRVO73PQL9EODCY259Su27JReUtjMrNcYDO%2BLVsRuvPfs1R\"}]}"
          ],
          "Server": [
            "cloudflare"
          ],
          "Server-Timing": [
            "cfCacheStatus;desc=\"BYPASS\"",
            "cfEdge;dur=229,cfOrigin;dur=0"
          ],
          "Strict-Transport-Security": [
            "max-age=31536000; includeSubDomains; preload"
          ],
          "X-Content-Type-Options": [
            "nosniff"
          ],
          "X-Frame-Options": [
            "SAMEORIGIN"
          ],
          "X-Xss-Protection": [
            "1; mode=block"
          ]
        },
        "technologies": [
          "HTTP/3",
          "Cloudflare",
          "Cloudflare Browser Insights",
          "HSTS",
          "checkpoint-gateway",
          "nginx",
          "zyxel-firewall"
        ],
        "cpes": [
          "cpe:2.3:o:checkpoint:gaia:*:*:*:*:*:*:*:*",
          "cpe:2.3:a:f5:nginx:*:*:*:*:*:*:*:*",
          "cpe:2.3:o:zyxel:zld_firmware:*:*:*:*:*:*:*:*"
        ],
        "fingerprint_metadata": {
          "checkpoint-gateway": {
            "product": "Security Gateway",
            "vendor": "Check Point"
          },
          "nginx": {
            "detection_method": "error_page",
            "product": "Nginx",
            "server_header": "cloudflare",
            "variant": "nginx",
            "vendor": "F5"
          },
          "zyxel-firewall": {
            "product": "Zyxel Firewall",
            "vendor": "Zyxel"
          }
        }
      }
    }
  ]
}
```

