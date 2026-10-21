# SPEC-020 semantic identity

B1 defines identity keys. It does not decide merge actions.

| Strategy | Types | Key |
|----------|-------|-----|
| Global | IPv4, IPv6, MAC, domain, company | Normalized value |
| Parent scoped | Category, transport, port, service | Parent key plus local value |
| Observation | Scan record and time-varying facts | One key per source occurrence |
| Evidence resolved | SYSTEM, HOST, DEVICE, CDN | Explicit same-system group inside one workflow execution |

## Address evidence

- A normalized address match is strong candidate evidence only inside one workflow execution.
- The same address in a later execution does not share an evidence-resolved key.
- An address match never creates that key by itself. An explicit same-system group ID is required.
- Different addresses remain separate unless a later policy stage supplies strong linking evidence.
- A hostname literal creates a `DOMAIN_NAME` record, not a `SYSTEM`.

## Parent scope

TCP port 443 on two hosts produces two port keys. Repeats of that port on one host produce one key.

Company aliases normalize to comparable strings here. Alias authority and ambiguity handling belong to the later GoRules policy.
