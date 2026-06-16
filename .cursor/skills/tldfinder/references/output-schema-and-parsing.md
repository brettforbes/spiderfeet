# tldfinder Output Schema and Parsing

tldfinder output represents candidate private/non-standard TLD signals derived from supplied seeds.

## Expected parsed fields

| Field class | Meaning |
|---|---|
| Seed context | source domain/org/input that led to detection |
| Candidate suffix | candidate TLD/private namespace |
| Confidence/score | ranking or confidence estimate |
| Evidence count | number/type of supporting observations |
| Validation hints | resolver or source notes that aid verification |

## Parsing workflow

1. Parse JSON line/object output when available.
2. Normalize candidate suffixes (`lowercase`, punycode-safe).
3. Attach source seed and evidence metadata.
4. Assign confidence tier (`high`, `medium`, `low`) from score fields.
5. Emit normalized records for nugget conversion and follow-up validation.

## Example normalized record

```json
{
  "seed": "corp.example.com",
  "candidate_tld": ".corp",
  "confidence": 0.82,
  "evidence_count": 14,
  "validation_state": "candidate"
}
```

## Edge handling

- Keep unknown/partial records in a quarantine list instead of discarding.
- Distinguish parse failures from empty findings.
- Preserve raw suffix strings before normalization for forensic traceability.
