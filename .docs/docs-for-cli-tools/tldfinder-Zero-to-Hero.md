# tldfinder Zero to Hero

Practical guide for using `tldfinder` to enumerate private and uncommon DNS namespaces.

## 1) What tldfinder is for

`tldfinder` helps identify candidate private/non-standard top-level namespaces from real-world domain evidence.

## 2) Install and verify

```bash
go install -v github.com/projectdiscovery/tldfinder/cmd/tldfinder@latest
tldfinder -h
```

## 3) First run

```bash
tldfinder -d example.com -json
```

Start with known organization seed domains.

## 4) Major option classes with examples

### A. Seed input

```bash
tldfinder -d example.com -json
tldfinder -l seeds.txt -json
```

### B. Confidence filtering

```bash
tldfinder -l seeds.txt -json -min-confidence 0.7
```

### C. Resolver-aware validation

```bash
tldfinder -l seeds.txt -json -r resolvers.txt
```

### D. Performance controls

Use concurrency/rate flags from your installed version for large input sets.

## 5) Practical workflows

### Workflow 1: Candidate private TLD discovery

1. Run on broad seed corpus.
2. Collect candidate suffixes and confidence scores.
3. Keep only medium/high confidence candidates.

### Workflow 2: Validation and expansion

1. Generate host candidates under discovered suffixes.
2. Resolve with `dnsx`.
3. Promote only resolvable/high-evidence namespaces.

### Workflow 3: Split-horizon analysis

1. Repeat discovery from alternate resolver/vantage sets.
2. Compare candidate recurrence.
3. Flag environment-specific private namespaces.

## 6) Output to SpiderFeet nuggets (`nodes[]` and `edges[]`)

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "corp.example.com" },
    { "type": "INTERNET_NAME", "data": ".corp", "meta": { "namespace_candidate": true } },
    { "type": "INTERNET_NAME", "data": "portal.auth.corp" }
  ],
  "edges": [
    { "source": "corp.example.com", "target": ".corp", "relationship": "suggests_private_tld" },
    { "source": ".corp", "target": "portal.auth.corp", "relationship": "expands_to_candidate_host" }
  ]
}
```

## 7) Tactics and strategy

- Blend diverse seeds (domains, certs, passive datasets).
- Score candidates by recurrence and evidence density.
- Validate before active expansion to avoid noisy pivots.
- Track namespace drift with recurring scans.

## 8) Common pitfalls

- Assuming every unusual suffix is private.
- Ignoring public suffix/root list context.
- Dropping low-confidence evidence without trace metadata.
- Skipping resolver differential checks in split-horizon environments.

## 9) Next references

- `.cursor/skills/tldfinder/SKILL.md`
- `.cursor/skills/tldfinder/references/SKILLS.md`
- [tldfinder repository](https://github.com/projectdiscovery/tldfinder)
