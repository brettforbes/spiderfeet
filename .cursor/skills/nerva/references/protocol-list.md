# Nerva Protocol List

Nerva ships **54 service detection plugins** across TCP, UDP, and SCTP (per official wiki). Some plugins probe multiple protocol variants; the blog cites 120+ protocol checks via depth inside plugins.

Use the `protocol` field in `--json` output as the canonical service identifier.

**Transport summary:** TCP 44 · UDP 10 · SCTP 1 · Total 54 (some protocols support multiple transports).

---

## Databases (18)

### Relational

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| PostgreSQL | TCP | 5432 | Auth detection, version |
| MySQL | TCP | 3306 | Version, error codes |
| MSSQL | TCP | 1433 | Instance detection |
| OracleDB | TCP | 1521 | TNS protocol |
| DB2 | TCP | 50000 | DRDA protocol |
| Sybase | TCP | 5000 | TDS protocol |
| Firebird | TCP | 3050 | Wire protocol |

### NoSQL

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| MongoDB | TCP | 27017 | Wire protocol version |
| Redis | TCP | 6379 | Auth detection |
| Cassandra | TCP | 9042 | CQL protocol |
| CouchDB | TCP | 5984 | HTTP-based |
| Elasticsearch | TCP | 9200 | Cluster info |
| InfluxDB | TCP | 8086 | HTTP API |
| Neo4j | TCP | 7687 | Bolt protocol |
| Memcached | TCP | 11211 | Text/binary protocol |

### Vector

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| ChromaDB | TCP | 8000 | Vector database |
| Milvus | TCP | 19530 | Vector database |
| Pinecone | TCP | 443 | HTTPS vector API |

---

## Remote access (4)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| SSH | TCP | 22 | Banner, algorithms, host key |
| RDP | TCP | 3389 | OS fingerprint, NetBIOS |
| Telnet | TCP | 23 | Banner detection |
| VNC | TCP | 5900 | Version detection |

---

## Web and API (2)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| HTTP/HTTPS | TCP | 80, 443 | HTTP/2, Wappalyzer tech detection |
| Kubernetes | TCP | 6443 | API server detection |

---

## Messaging (5)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| Kafka | TCP | 9092 | Old and new protocol versions |
| MQTT | TCP | 1883 | MQTT 3 and MQTT 5 |
| SMTP/SMTPS | TCP | 25, 465, 587 | Banner detection |
| POP3/POP3S | TCP | 110, 995 | Banner detection |
| IMAP/IMAPS | TCP | 143, 993 | Banner detection |

---

## File transfer (3)

| Protocol | Transport | Default port |
|----------|-----------|--------------|
| FTP | TCP | 21 |
| SMB | TCP | 445 |
| Rsync | TCP | 873 |

---

## Directory services (2)

| Protocol | Transport | Default port |
|----------|-----------|--------------|
| LDAP | TCP | 389 |
| LDAPS | TCP | 636 |

---

## Network services (10)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| DNS | TCP/UDP | 53 | Dual transport |
| DHCP | UDP | 67 | Server detection |
| NTP | UDP | 123 | Version info |
| SNMP | UDP | 161 | Community detection |
| NetBIOS-NS | UDP | 137 | Name service |
| STUN | UDP | 3478 | NAT traversal |
| OpenVPN | UDP | 1194 | VPN detection |
| IPsec | UDP | 500 | IKE detection |
| IPMI | UDP | 623 | Server management |
| Echo | TCP/UDP | 7 | Dual transport |

---

## Industrial and telecom (5)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| Modbus | TCP | 502 | Industrial control |
| IPMI | UDP | 623 | Server management |
| Diameter | TCP | 3868 | 3GPP/LTE/5G AAA |
| Diameter-SCTP | SCTP | 3868 | Telecom (Linux only) |
| SMPP | TCP | 2775 | SMS gateway |

---

## Developer tools (4)

| Protocol | Transport | Default port | Notes |
|----------|-----------|--------------|-------|
| JDWP | TCP | 5005 | Java Debug Wire Protocol |
| Java RMI | TCP | 1099 | Remote Method Invocation |
| RTSP | TCP | 554 | Streaming media |
| Linux RPC | TCP | 111 | Portmapper |

---

## Port-aware prioritization

Nerva tries the **most likely protocol for the port first** (e.g. 22 → SSH), then falls back to broader probes unless `--fast` limits checks to default-port plugins only.

| Port | First probe (typical) |
|------|------------------------|
| 22 | ssh |
| 80 | http |
| 443 | https |
| 3306 | mysql |
| 5432 | postgresql |
| 3389 | rdp |
| 53 | dns (use `-U`) |
| 3868 | diameter (`-S` for SCTP) |

---

## Selecting plugins via CLI

| Need | Flag |
|------|------|
| TCP services | *(default)* |
| UDP services | `-U` |
| SCTP / Diameter | `-S` (Linux) |
| Speed over depth | `--fast` |

---

## Source

Canonical list: https://github.com/praetorian-inc/nerva/wiki/Protocol-List

Plugin count may grow between releases — run against live `--json` output for ground truth.
