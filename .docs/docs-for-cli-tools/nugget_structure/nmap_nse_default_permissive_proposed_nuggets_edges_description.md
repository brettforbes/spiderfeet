# Nmap OSINT Scan Report — nse_default_permissive

## Introduction

This report narrates the findings of a **Nmap** scan against **scanme.nmap.org**. The story follows the scan itself, each discovered host, and any traceroute path recorded during the run. Every observed nugget and value from the semantic graph appears in the narrative below or in the appendix.

## Scan

The scan was executed with **nmap** version **7.80**, targeting **scanme.nmap.org** from **Tue Jun 23 19:02:05 2026**. The operator invoked: `nmap -sT -sC -T3 -p 22,80,443 -oX - scanme.nmap.org`.
 The run completed in **9.83** seconds.

Nmap done at Tue Jun 23 19:02:15 2026; 1 IP address (1 host up) scanned in 9.83 seconds

During this scan, **1** host was placed under investigation.

## Host 45.33.32.156

The host was observed as **up** (reason: **echo-reply**).
It answers to the internet name **scanme.nmap.org**.

### Networks

Network address **45.33.32.156**:
- Port **22** on **tcp** is **open** (syn-ack), associated with **ssh**.
- Port **443** on **tcp** is **filtered** (no-response), associated with **https**.
- Port **80** on **tcp** is **open** (syn-ack), associated with **http**.

### Applications

Application service **http** listening on port **80**.
Application service **https** listening on port **443**.
Application service **ssh** listening on port **22**.
The **ssh** service exposes an **DSA** SSH host key (fingerprint `ac00a01a82ffcc5599dc672b34976b75`). Algorithm: **ssh-dss**. Key size: **1024** bits. Public key material: `AAAAB3NzaC1kc3MAAACBAOe8o59vFWZGaBmGPVeJBObEfi1AR8yEUYC/Ufkku3sKhGF7wM2m2ujIeZDK5vqeC0S5EN2xYo6FshCP4FQRYeTxD17nNO4PhwW65qAjDRRU0uHFfSAh5wk+vt4yQztOE++sTd1G9OBLzA8HO99qDmCAxb3zw+GQDEgPjzgyzGZ3AAAAFQCBmE1vROP8IaPkUmhM5xLFta/xHwAAAIEA3EwRfaeOPLL7TKDgGX67Lbkf9UtdlpCdC4doMjGgsznYMwWH6a7Lj3vi4/KmeZZdix6FMdFqq+2vrfT1DRqx0RS0XYdGxnkgS+2g333WYCrUkDCn6RPUWR/1TgGMPHCj7LWCa1ZwJwLWS2KX288Pa2gLOWuhZm2VYKSQx6NEDOIAAACBANxIfprSdBdbo4Ezrh6/X6HSvrhjtZ7MouStWaE714ByO5bS2coM9CyaCwYyrE5qzYiyIfb+1BG3O5nVdDuN95sQ/0bAdBKlkqLFvFqFjVbETF0ri3v97w6MpUawfF75ouDrQ4xdaUOLLEWTso6VFJcM6Jg9bDl0FA0uLZUSDEHL`
The **ssh** service exposes an **ECDSA** SSH host key (fingerprint `9602bb5e57541c4e452f564c4a24b257`). Algorithm: **ecdsa-sha2-nistp256**. Key size: **256** bits. Public key material: `AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMD46g67x6yWNjjQJnXhiz/TskHrqQ0uPcOspFrIYW382uOGzmWDZCFV8FbFwQyH90u+j0Qr1SGNAxBZMhOQ8pc=`
The **ssh** service exposes an **EDDSA** SSH host key (fingerprint `33fa910fe0e17b1f6d05a2b0f1544156`). Algorithm: **ssh-ed25519**. Key size: **256** bits. Public key material: `AAAAC3NzaC1lZDI1NTE5AAAAILzVjfIyIHfXyRd8jVBaVT8Yvk/UvHh5Afvho8sGciG7`
The **ssh** service exposes an **RSA** SSH host key (fingerprint `203d2d44622ab05a9db5b30514c2a6b2`). Algorithm: **ssh-rsa**. Key size: **2048** bits. Public key material: `AAAAB3NzaC1yc2EAAAADAQABAAABAQC6afooTZ9mVUGFNEhkMoRR1Btzu64XXwElhCsHw/zVlIx/HXylNbb9+11dm2VgJQ21pxkWDs+L6+EbYyDnvRURTrMTgHL0xseB0EkNqexs9hYZSiqtMx4jtGNtHvsMxZnbxvVUk2dasWvtBkn8J5JagSbzWTQo4hjKMOI1SUlXtiKxAs2F8wiq2EdSuKw/KNk8GfIp1TA+8ccGeAtnsVptTJ4D/8MhAWsROkQzOowQvnBBz2/8ecEvoMScaf+kDfNQowK3gENtSSOqYw9JLOza6YJBPL/aYuQQ0nJ74Rr5vL44aNIlrGI9jJc2x0bV7BeNA5kVuXsmhyfWbbkB8yGd`

## Conclusion

The scan captured **42** semantic nuggets across **1** host.
 Nmap done at Tue Jun 23 19:02:15 2026; 1 IP address (1 host up) scanned in 9.83 seconds
 The appendix lists every nugget instance and value for audit and downstream review.


## Appendix — Complete Nugget Inventory

| Type | Nugget | Description | Value |
|------|--------|-------------|-------|
| CATEGORY | APPLICATIONS | Applications Category | `applications:45.33.32.156` |
| CATEGORY | NETWORKS | Networks Category | `networks:45.33.32.156` |
| DESCRIPTOR | HOST_STATUS | Host Status | `up` |
| DESCRIPTOR | HOST_STATUS_REASON | Host Status Reason | `echo-reply` |
| DESCRIPTOR | PORT_PROTOCOL | Port Protocol | `tcp` |
| DESCRIPTOR | PORT_STATE | Port State | `filtered` |
| DESCRIPTOR | PORT_STATE | Port State | `open` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `no-response` |
| DESCRIPTOR | PORT_STATE_REASON | Port State Reason | `syn-ack` |
| DESCRIPTOR | SCAN_CLI | Scan CLI | `nmap -sT -sC -T3 -p 22,80,443 -oX - scanme.nmap.org` |
| DESCRIPTOR | SCAN_ELAPSED | Scan Elapsed Time | `9.83` |
| DESCRIPTOR | SCAN_START | Scan Start | `Tue Jun 23 19:02:05 2026` |
| DESCRIPTOR | SCAN_SUMMARY | Scan Summary | `Nmap done at Tue Jun 23 19:02:15 2026; 1 IP address (1 host up) scanned in 9.83 seconds` |
| DESCRIPTOR | SCAN_TARGET | Scan Target | `scanme.nmap.org` |
| DESCRIPTOR | SCAN_TOOL | Scan Tool | `nmap` |
| DESCRIPTOR | SCAN_VERSION | Scan Version | `7.80` |
| DESCRIPTOR | SSH_KEY_BITS | SSH Key Bits | `1024` |
| DESCRIPTOR | SSH_KEY_BITS | SSH Key Bits | `2048` |
| DESCRIPTOR | SSH_KEY_BITS | SSH Key Bits | `256` |
| DESCRIPTOR | SSH_KEY_KEY | SSH Public Key | `AAAAB3NzaC1kc3MAAACBAOe8o59vFWZGaBmGPVeJBObEfi1AR8yEUYC/Ufkku3sKhGF7wM2m2ujIeZDK5vqeC0S5EN2xYo6FshCP4FQRYeTxD17nNO4PhwW65qAjDRRU0uHFfSAh5wk+vt4yQztOE++sTd1G9OBLzA8HO99qDmCAxb3zw+GQDEgPjzgyzGZ3AAAAFQCBmE1vROP8IaPkUmhM5xLFta/xHwAAAIEA3EwRfaeOPLL7TKDgGX67Lbkf9UtdlpCdC4doMjGgsznYMwWH6a7Lj3vi4/KmeZZdix6FMdFqq+2vrfT1DRqx0RS0XYdGxnkgS+2g333WYCrUkDCn6RPUWR/1TgGMPHCj7LWCa1ZwJwLWS2KX288Pa2gLOWuhZm2VYKSQx6NEDOIAAACBANxIfprSdBdbo4Ezrh6/X6HSvrhjtZ7MouStWaE714ByO5bS2coM9CyaCwYyrE5qzYiyIfb+1BG3O5nVdDuN95sQ/0bAdBKlkqLFvFqFjVbETF0ri3v97w6MpUawfF75ouDrQ4xdaUOLLEWTso6VFJcM6Jg9bDl0FA0uLZUSDEHL` |
| DESCRIPTOR | SSH_KEY_KEY | SSH Public Key | `AAAAB3NzaC1yc2EAAAADAQABAAABAQC6afooTZ9mVUGFNEhkMoRR1Btzu64XXwElhCsHw/zVlIx/HXylNbb9+11dm2VgJQ21pxkWDs+L6+EbYyDnvRURTrMTgHL0xseB0EkNqexs9hYZSiqtMx4jtGNtHvsMxZnbxvVUk2dasWvtBkn8J5JagSbzWTQo4hjKMOI1SUlXtiKxAs2F8wiq2EdSuKw/KNk8GfIp1TA+8ccGeAtnsVptTJ4D/8MhAWsROkQzOowQvnBBz2/8ecEvoMScaf+kDfNQowK3gENtSSOqYw9JLOza6YJBPL/aYuQQ0nJ74Rr5vL44aNIlrGI9jJc2x0bV7BeNA5kVuXsmhyfWbbkB8yGd` |
| DESCRIPTOR | SSH_KEY_KEY | SSH Public Key | `AAAAC3NzaC1lZDI1NTE5AAAAILzVjfIyIHfXyRd8jVBaVT8Yvk/UvHh5Afvho8sGciG7` |
| DESCRIPTOR | SSH_KEY_KEY | SSH Public Key | `AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMD46g67x6yWNjjQJnXhiz/TskHrqQ0uPcOspFrIYW382uOGzmWDZCFV8FbFwQyH90u+j0Qr1SGNAxBZMhOQ8pc=` |
| DESCRIPTOR | SSH_KEY_TYPE | SSH Key Type | `ecdsa-sha2-nistp256` |
| DESCRIPTOR | SSH_KEY_TYPE | SSH Key Type | `ssh-dss` |
| DESCRIPTOR | SSH_KEY_TYPE | SSH Key Type | `ssh-ed25519` |
| DESCRIPTOR | SSH_KEY_TYPE | SSH Key Type | `ssh-rsa` |
| ENTITY | HOST | Host | `45.33.32.156` |
| ENTITY | INTERNET_NAME | Internet Name | `scanme.nmap.org` |
| ENTITY | IP_ADDRESS | IP Address | `45.33.32.156` |
| ENTITY | SCAN_RECORD | Scan Record | `nmap:scanme.nmap.org:Tue Jun 23 19:02:05 2026` |
| ENTITY | SERVICE | Network Service | `http` |
| ENTITY | SERVICE | Network Service | `https` |
| ENTITY | SERVICE | Network Service | `ssh` |
| ENTITY | TRANSPORT | Transport Protocol | `tcp` |
| SUBENTITY | DSA | SSH Key - DSA | `ac00a01a82ffcc5599dc672b34976b75` |
| SUBENTITY | ECDSA | SSH Key - ECDSA | `9602bb5e57541c4e452f564c4a24b257` |
| SUBENTITY | EDDSA | SSH Key - EdDSA | `33fa910fe0e17b1f6d05a2b0f1544156` |
| SUBENTITY | PORT | Network Port | `22` |
| SUBENTITY | PORT | Network Port | `443` |
| SUBENTITY | PORT | Network Port | `80` |
| SUBENTITY | RSA | SSH Key - RSA | `203d2d44622ab05a9db5b30514c2a6b2` |

---

*OS-Intel Scan · Tue Jun 23 19:02:05 2026 · Page 1*
