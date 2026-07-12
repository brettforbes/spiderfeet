# Current CLI Profiling Ontology

Living summary of the **unified** nugget graph model built incrementally from CLI application profiling. Individual tools each contribute **sub-graphs** — validated slices of the same ontology — that **compose** into one semantic investigation graph. Start here for the full-extent vocabulary; drill into per-tool structure docs and generators when implementing parsers.


| Sub-graph (tool) | Status | Structure doc | Generator |
|------------------|--------|---------------|-----------|
| **Nmap** | implemented | [nmap_nugget_graph_structure.md](nugget_structure/nmap_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/nmap` |
| **Netdiscover** | implemented | [netdiscover_nugget_graph_structure.md](nugget_structure/netdiscover_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/netdiscover` |
| **Nerva** | implemented | [nerva_nugget_graph_structure.md](nugget_structure/nerva_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/nerva` |
| **Pius** | implemented | [pius_nugget_graph_structure.md](nugget_structure/pius_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/pius` |
| **Subfinder** | implemented | [subfinder_nugget_graph_structure.md](nugget_structure/subfinder_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/subfinder` |
| **httpx** | implemented | [httpx_nugget_graph_structure.md](nugget_structure/httpx_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/httpx` |
| **Katana** | implemented | [katana_nugget_graph_structure.md](nugget_structure/katana_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/katana` |
| **Nuclei** | implemented | [nuclei_nugget_graph_structure.md](nugget_structure/nuclei_nugget_graph_structure.md) | `.seed/scripts/cli_corpus/adapters/nuclei` |

Canonical seed: `.seed/05_Onotology_for_Nuggets.md` · Vocabulary: `.docs/analysis/nuggets.json` + `.docs/analysis/nuggets_extension.json` · Correlation: `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`

---

## Unified model (full extent)

Every profiled CLI app emits a graph that **plugs into** the same top-level shape:

```mermaid
flowchart TD
  scan["SCAN_RECORD"]
  endpoint["Endpoint entity"]
  cat["Category nuggets"]
  desc["Descriptor nuggets"]
  scan -->|contains| endpoint
  scan -->|had| desc
  endpoint -->|contains| cat
  endpoint -->|had| desc
  cat -->|contains| desc
```

| Layer | Role | Shared across tools |
|-------|------|---------------------|
| **Scan head** | One `SCAN_RECORD` per examination run; tool-specific metadata as `had` descriptors | Always |
| **Endpoint** | `SYSTEM`, `HOST`, `DEVICE`, `MOBILE`, `SERVER`, `CDN`, `DOMAIN_NAME`, `COMPANY_NAME`, … | Variant per evidence |
| **Categories** | `NETWORKS`, `APPLICATIONS`, `ENVIRONMENT`, `VULNERABILITIES`, `SECURITY`, … | As evidence allows |
| **Facts** | Descriptor nuggets linked via `had` or nested `contains` | As evidence allows |

**Composition rule:** later scans **add** nodes and edges to the same investigation; they do not define a parallel ontology.

---

## Relations (global)

| Relation | Direction | Meaning |
|----------|-----------|---------|
| `contains` | parent → child | Structural ownership |
| `had` | entity → descriptor | Attribute fact on a node |
| `listens-to` | service → port | Application service associated with a transport port |

Instance ids use `nugget_id--uuid5(ontology_seed, nugget_data)` — see `core/graph_builder.py`.

---

## System qualification hierarchy

Endpoint subclass is a qualification decision within the unified model. ARP-level scans emit **`SYSTEM`**; port/service scans justify **`HOST`** or **`CDN`**; org tools emit **`COMPANY_NAME`** and **`DOMAIN_NAME`** trees.

```mermaid
flowchart TB
  system["SYSTEM"]
  host["HOST"]
  cdn["CDN"]
  company["COMPANY_NAME"]
  domain["DOMAIN_NAME"]
  system --> host
  system --> cdn
```

| Depth | Typical tools | Endpoint | Categories typically present |
|-------|---------------|----------|------------------------------|
| L2 / ARP | Netdiscover | `SYSTEM` | `NETWORKS` → IP/MAC |
| L3 + ports | Nmap, Nerva | `HOST` / `CDN` | `NETWORKS`, `APPLICATIONS` |
| DNS / org | Subfinder, Pius | `DOMAIN_NAME`, `COMPANY_NAME` | domain descriptors, netblocks |
| Web probe | httpx, Katana | `HOST` / `CDN` | `APPLICATIONS`, URL entities |
| Vuln scan | Nuclei | `HOST` | `SECURITY` → `FINDINGS` |

---


## Sub-graph: Nmap

*Nmap contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/nmap`. See the per-tool Structure doc for field tables and scenario coverage.*

### Host reachability

HOST_STATUS and HOST_STATUS_REASON attach to HOST via had when reachability is reported.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  host_2["HOST"]
  host_status_3["HOST_STATUS"]
  host_status_reason_4["HOST_STATUS_REASON"]
  networks_5["NETWORKS"]
  ip_address_6["IP_ADDRESS"]
  scan_record_1 -->|contains| host_2
  host_2 -->|had| host_status_3
  host_2 -->|had| host_status_reason_4
  host_2 -->|contains| networks_5
  networks_5 -->|contains| ip_address_6
```

### Host port and service tree

Qualified HOST scans extend NETWORKS with TRANSPORT and PORT; APPLICATIONS contains SERVICE entities that listens-to their PORT. Port protocol and state are descriptors.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  host_2["HOST"]
  networks_3["NETWORKS"]
  ip_address_4["IP_ADDRESS"]
  transport_5["TRANSPORT"]
  port_6["PORT"]
  port_state_7["PORT_STATE"]
  applications_8["APPLICATIONS"]
  service_9["SERVICE"]
  service_version_10["SERVICE_VERSION"]
  scan_record_1 -->|contains| host_2
  host_2 -->|contains| networks_3
  networks_3 -->|contains| ip_address_4
  networks_3 -->|contains| transport_5
  transport_5 -->|contains| port_6
  port_6 -->|had| port_state_7
  host_2 -->|contains| applications_8
  applications_8 -->|contains| service_9
  service_9 -->|listens-to| port_6
  service_9 -->|had| service_version_10
```

### SSH service and host keys

When SSH host-key scripts fire, APPLICATIONS contains an SSH SERVICE that listens-to the open PORT and contains key SUBENTITY nodes (RSA, ECDSA, EDDSA, DSA) with SSH_KEY_* descriptors.

```mermaid
flowchart TD
  host_1["HOST"]
  applications_2["APPLICATIONS"]
  service_3["SERVICE ssh"]
  service_4["SERVICE"]
  port_5["PORT tcp/22"]
  port_6["PORT"]
  port_state_7["PORT_STATE"]
  rsa_8["RSA"]
  ecdsa_9["ECDSA"]
  ssh_key_bits_10["SSH_KEY_BITS"]
  ssh_key_type_11["SSH_KEY_TYPE"]
  ssh_key_key_12["SSH_KEY_KEY"]
  host_1 -->|contains| applications_2
  applications_2 -->|contains| service_3
  service_4 -->|listens-to| port_5
  port_6 -->|had| port_state_7
  service_4 -->|contains| rsa_8
  service_4 -->|contains| ecdsa_9
  rsa_8 -->|had| ssh_key_bits_10
  rsa_8 -->|had| ssh_key_type_11
  rsa_8 -->|had| ssh_key_key_12
```

Full Structure doc: [nmap_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Netdiscover

*Netdiscover contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/netdiscover`. See the per-tool Structure doc for field tables and scenario coverage.*

### System tree (L2 provisional)

When only L2/L3 identity is known, emit SYSTEM (not HOST). Each system owns a NETWORKS category containing IPv4 and L2 facts; MAC_VENDOR attaches via had on MAC_ADDRESS.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  system_2["SYSTEM"]
  networks_3["NETWORKS"]
  ip_address_4["IP_ADDRESS"]
  mac_address_5["MAC_ADDRESS"]
  mac_vendor_6["MAC_VENDOR"]
  scan_record_1 -->|contains| system_2
  system_2 -->|contains| networks_3
  networks_3 -->|contains| ip_address_4
  networks_3 -->|contains| mac_address_5
  mac_address_5 -->|had| mac_vendor_6
```

Full Structure doc: [netdiscover_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Nerva

*Nerva contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/nerva`. See the per-tool Structure doc for field tables and scenario coverage.*

### Host port and service tree

Qualified HOST scans extend NETWORKS with TRANSPORT and PORT; APPLICATIONS contains SERVICE entities that listens-to their PORT. Port protocol and state are descriptors.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  host_2["HOST"]
  networks_3["NETWORKS"]
  ip_address_4["IP_ADDRESS"]
  transport_5["TRANSPORT"]
  port_6["PORT"]
  port_state_7["PORT_STATE"]
  applications_8["APPLICATIONS"]
  service_9["SERVICE"]
  service_version_10["SERVICE_VERSION"]
  scan_record_1 -->|contains| host_2
  host_2 -->|contains| networks_3
  networks_3 -->|contains| ip_address_4
  networks_3 -->|contains| transport_5
  transport_5 -->|contains| port_6
  port_6 -->|had| port_state_7
  host_2 -->|contains| applications_8
  applications_8 -->|contains| service_9
  service_9 -->|listens-to| port_6
  service_9 -->|had| service_version_10
```

Full Structure doc: [nerva_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Pius

*Pius contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/pius`. See the per-tool Structure doc for field tables and scenario coverage.*

### Organisation company tree

Pius scans contain a COMPANY_NAME root with category buckets (DOMAINS, NETBLOCKS, …) holding INTERNET_NAME and NETBLOCK_OWNER findings plus PIUS_SOURCE descriptors.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  company_name_2["COMPANY_NAME"]
  domains_3["DOMAINS category"]
  netblocks_4["NETBLOCKS category"]
  domains_5["DOMAINS"]
  internet_name_6["INTERNET_NAME"]
  netblocks_7["NETBLOCKS"]
  netblock_owner_8["NETBLOCK_OWNER"]
  pius_source_9["PIUS_SOURCE"]
  scan_record_1 -->|contains| company_name_2
  company_name_2 -->|contains| domains_3
  company_name_2 -->|contains| netblocks_4
  domains_5 -->|contains| internet_name_6
  netblocks_7 -->|contains| netblock_owner_8
  internet_name_6 -->|had| pius_source_9
  netblock_owner_8 -->|had| pius_source_9
```

Full Structure doc: [pius_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Subfinder

*Subfinder contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/subfinder`. See the per-tool Structure doc for field tables and scenario coverage.*

### Domain apex tree

Org-intelligence and DNS tools root at DOMAIN_NAME entities under SCAN_RECORD. Subdomains are sibling DOMAIN_NAME nodes; descriptors capture discovery mode, sources, and liveness.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  domain_name_2["DOMAIN_NAME apex"]
  domain_name_3["DOMAIN_NAME"]
  domain_name_4["DOMAIN_NAME subdomain"]
  discovery_mode_5["DISCOVERY_MODE"]
  discovery_source_6["DISCOVERY_SOURCE"]
  liveness_status_7["LIVENESS_STATUS"]
  ip_address_8["IP_ADDRESS"]
  scan_record_1 -->|contains| domain_name_2
  domain_name_3 -->|contains| domain_name_4
  domain_name_3 -->|had| discovery_mode_5
  domain_name_3 -->|had| discovery_source_6
  domain_name_3 -->|had| liveness_status_7
  domain_name_3 -->|had| ip_address_8
```

Full Structure doc: [subfinder_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: httpx

*httpx contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/httpx`. See the per-tool Structure doc for field tables and scenario coverage.*

### Web URL probe tree

httpx attaches LINKED_URL_INTERNAL per live probe under SCAN_RECORD and DOMAIN_NAME apex. HOST or CDN endpoints own NETWORKS port chains and APPLICATIONS SERVICE facts.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  domain_name_2["DOMAIN_NAME apex"]
  linked_url_internal_3["LINKED_URL_INTERNAL"]
  domain_name_4["DOMAIN_NAME"]
  host_5["HOST"]
  networks_6["NETWORKS"]
  ip_address_7["IP_ADDRESS"]
  transport_8["TRANSPORT"]
  port_9["PORT"]
  applications_10["APPLICATIONS"]
  service_11["SERVICE"]
  http_status_code_12["HTTP_STATUS_CODE"]
  webserver_technology_13["WEBSERVER_TECHNOLOGY"]
  scan_record_1 -->|contains| domain_name_2
  scan_record_1 -->|contains| linked_url_internal_3
  domain_name_4 -->|contains| host_5
  host_5 -->|contains| networks_6
  networks_6 -->|contains| ip_address_7
  networks_6 -->|contains| transport_8
  transport_8 -->|contains| port_9
  host_5 -->|contains| applications_10
  applications_10 -->|contains| service_11
  service_11 -->|listens-to| port_9
  service_11 -->|had| http_status_code_12
  service_11 -->|had| webserver_technology_13
```

Full Structure doc: [httpx_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Katana

*Katana contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/katana`. See the per-tool Structure doc for field tables and scenario coverage.*

### Crawl URL tree

Katana extends the web surface with LINKED_URL_INTERNAL nodes under SCAN_RECORD and nests URLs under discovered DOMAIN_NAME hosts within the crawl scope.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  domain_name_2["DOMAIN_NAME apex"]
  linked_url_internal_3["LINKED_URL_INTERNAL"]
  domain_name_4["DOMAIN_NAME"]
  domain_name_5["DOMAIN_NAME host"]
  linked_url_internal_6["LINKED_URL_INTERNAL path"]
  http_method_7["HTTP_METHOD"]
  http_status_code_8["HTTP_STATUS_CODE"]
  scan_record_1 -->|contains| domain_name_2
  scan_record_1 -->|contains| linked_url_internal_3
  domain_name_4 -->|contains| domain_name_5
  domain_name_4 -->|contains| linked_url_internal_6
  linked_url_internal_3 -->|had| http_method_7
  linked_url_internal_3 -->|had| http_status_code_8
```

Full Structure doc: [katana_nugget_graph_structure.md](_Current_Ontology.md).

## Sub-graph: Nuclei

*Nuclei contributes validated nodes and edges via `.seed/scripts/cli_corpus/adapters/nuclei`. See the per-tool Structure doc for field tables and scenario coverage.*

### Vulnerability findings tree

Nuclei attaches SECURITY under HOST with FINDINGS severity buckets, NUCLEI_FINDING rows, NUCLEI_VULNERABILITY observations, and optional CVE tier descriptors.

```mermaid
flowchart TD
  scan_record_1["SCAN_RECORD"]
  host_2["HOST"]
  security_3["SECURITY"]
  findings_4["FINDINGS"]
  templates_used_5["TEMPLATES_USED"]
  nuclei_severity_high_6["NUCLEI_SEVERITY category"]
  nuclei_severity_high_7["NUCLEI_SEVERITY_HIGH"]
  nuclei_finding_8["NUCLEI_FINDING"]
  nuclei_vulnerability_9["NUCLEI_VULNERABILITY"]
  vulnerability_cve_high_10["VULNERABILITY_CVE_HIGH"]
  nuclei_template_11["NUCLEI_TEMPLATE"]
  scan_record_1 -->|contains| host_2
  host_2 -->|contains| security_3
  security_3 -->|contains| findings_4
  security_3 -->|contains| templates_used_5
  findings_4 -->|contains| nuclei_severity_high_6
  nuclei_severity_high_7 -->|contains| nuclei_finding_8
  nuclei_finding_8 -->|contains| nuclei_vulnerability_9
  nuclei_vulnerability_9 -->|had| vulnerability_cve_high_10
  templates_used_5 -->|contains| nuclei_template_11
```

Full Structure doc: [nuclei_nugget_graph_structure.md](_Current_Ontology.md).

## Composing sub-graphs

The **investigation graph** is the union of contributed sub-graphs, correlated by shared keys (`IP_ADDRESS`, `INTERNET_NAME` / `DOMAIN_NAME`, URLs, findings):

```mermaid
flowchart LR
  sf["Subfinder
DOMAIN_NAME"]
  hx["httpx
web probe"]
  ka["Katana
crawl URLs"]
  nm["Nmap
HOST + SERVICE"]
  nv["Nerva
fingerprint"]
  nu["Nuclei
FINDINGS"]
  sf --> hx --> ka
  nm --> nv --> nu
  sf -.->|"hostname correlates"| nm
```

Shallow discovery leaves provisional endpoints until deeper sub-graphs justify reclassification.

---

## Expansion policy

- Prefer **extending** the unified model over forking per-tool ontologies.
- Keep each Mermaid diagram focused (≤12 nodes where possible).
- Document parser mappings in per-tool `*_nugget_graph_structure.md`; keep this file as the composed view.
- Regenerate via `render_structure_docs.py --ontology` after structure pack changes.
