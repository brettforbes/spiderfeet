# httpx Config, Ports, and Paths

## Configuration file

Default path:

| OS | Path |
|----|------|
| Linux/macOS | `~/.config/httpx/config.yaml` |
| Windows | `%USERPROFILE%\.config\httpx\config.yaml` |

Override with `-config /path/to/config.yaml`.

Store recurring defaults (threads, timeout, resolvers, headers) in config for repeatable corpus runs — document effective config in examination manifests.

## Port probing (`-p` / `-ports`)

nmap-style port syntax:

```bash
httpx -l hosts.txt -p 80,443,8080,8443 -json
httpx -l hosts.txt -p http:8080,https:8443 -json
httpx -l hosts.txt -p http:443,http:80,https:8443 -json
```

Custom schemes per port when services use non-standard TLS/HTTP bindings.

**After naabu:**

```bash
naabu -host target.com -json -silent | jq -r '"http://" + .host + ":" + (.port|tostring)' | httpx -json -silent
```

Or probe standard web ports on discovered IPs.

## Path probing (`-path`)

Comma-separated or file list:

```bash
httpx -l urls.txt -path /v1/api,/admin,/login -status-code -json
httpx -l urls.txt -path paths.txt -sc -json -o path_scan.jsonl
```

Each base URL × path = separate request. Use for **path discovery scenarios**, not default host-only corpus.

## TLS and CSP probes

```bash
httpx -u https://example.com -tls-probe -json
httpx -u https://example.com -csp-probe -json
```

Extracts additional hostnames from certificates and Content-Security-Policy — feed back to **dnsx** / second **subfinder** pass.

## HTTP/HTTPS behaviour

| Flag | Behaviour |
|------|-----------|
| default | HTTPS first, fallback to HTTP if HTTPS fails |
| `-no-fallback` | Probe and show both schemes |
| `-no-fallback-scheme` | Honor scheme in input only |

## CDN optimization

```bash
httpx -l hosts.txt -exclude-cdn -json
httpx -l hosts.txt -cdn -json
```

`-exclude-cdn` limits probing on known CDN hosts (80/443 only).

## Multi-IP hosts

```bash
httpx -l hosts.txt -probe-all-ips -json
```

Probes every A/AAAA returned for a hostname.

## VHOST mode

```bash
httpx -l vhosts.txt -vhost -status-code -json
```

Input is vhost names; use dedicated scenario.

## Resolvers

```bash
httpx -l hosts.txt -r 8.8.8.8,1.1.1.1 -json
httpx -l hosts.txt -rL resolvers.txt -json
```

## Allow / deny lists

```bash
httpx -l all.txt -allow 10.0.0.0/8 -json
httpx -l all.txt -deny 192.168.0.0/16 -json
```

## Screenshot output

```bash
httpx -u https://example.com -screenshot -srd ./shots/
httpx -screenshot -system-chrome -u https://example.com
```

Screenshots default under `output/screenshot/`; JSON may reference paths when `-json` combined.

## Docker

```bash
cat hosts.txt | docker run -i projectdiscovery/httpx -json -silent
```

Mount config volume when needed for persistent settings.
