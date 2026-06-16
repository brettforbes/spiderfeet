# Vespasian Zero to Hero

Vespasian discovers APIs by observing real traffic and generates OpenAPI, GraphQL SDL, or WSDL specs.

## 1) Install

```bash
go install github.com/praetorian-inc/vespasian/cmd/vespasian@latest
```

## 2) Quick scan

```bash
vespasian scan https://app.example.com -o api.yaml
```

This is the fastest way to get a first endpoint map.

## 3) Two-stage flow for repeatability

```bash
vespasian crawl https://app.example.com -o capture.json
vespasian generate rest capture.json -o openapi.yaml
```

Use this when you want stable artifacts and re-generation without re-crawling.

## 4) Import existing traffic

```bash
vespasian import burp traffic.xml -o capture.json
vespasian generate graphql capture.json -o schema.graphql
```

## 5) Expand coverage

- Add auth headers with `-H`.
- Increase `--depth` and `--max-pages`.
- Use `--scope same-domain` if cross-subdomain calls matter.

## 6) Private targets in lab

```bash
vespasian scan http://localhost:3000 --dangerous-allow-private -o api.yaml
```

## 7) Convert to SpiderFeet-style nuggets

Create graph arrays:
- nodes: host, endpoint, parameter, generated spec artifact
- edges: host exposes endpoint; endpoint uses parameter; endpoint documented in spec

## 8) Common pitfalls

- assuming one crawl covers all user journeys
- forgetting authenticated flows
- treating generated spec as full system contract rather than observed surface
