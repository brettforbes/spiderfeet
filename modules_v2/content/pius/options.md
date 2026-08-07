# PIUS CLI Arguments

```


Pius discovers CIDR blocks and domains associated with an organization using multiple OSINT data sources.

Usage:
  pius run [flags]

Flags:
      --asn string            Known ASN hint, e.g. AS12345 (optional)
      --cidr string           Known CIDR range, e.g. 192.0.2.0/24 (optional)
      --concurrency int       Max concurrent plugins (default 5)
      --disable string        Comma-separated plugin blacklist
      --doh-deploy-gateways   Auto-deploy AWS API Gateways pointing to DoH servers
      --doh-gateways string   Comma-separated AWS API Gateway URLs for DoH
      --doh-servers string    Comma-separated DoH server URLs
      --doh-wordlist string   Path to subdomain wordlist for DoH enumeration (default: embedded)
  -d, --domain string         Known domain hint (optional)
  -h, --help                  help for run
      --mode string           Plugin mode filter: passive|active|all (default "passive")
      --org string            Organization name to search (required)
  -o, --output string         Output format: terminal|json|ndjson (default "terminal")
      --plugins string        Comma-separated plugin whitelist (default: all)
```
