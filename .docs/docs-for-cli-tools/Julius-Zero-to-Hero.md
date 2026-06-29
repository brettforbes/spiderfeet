# Julius Zero to Hero — LLM Fingerprinting, JSONL, and Nuggets

From install to shadow-AI discovery with **`julius probe -o jsonl`**, nugget mapping, and **Naabu → Julius** chaining.

Skill reference: `.cursor/skills/julius/SKILL.md`

## What Julius does

Julius answers: **what LLM / AI inference service is exposed on this HTTP(S) endpoint?**

It sends HTTP probes (32+ embedded YAML signatures) to detect Ollama, vLLM, LiteLLM, Open WebUI, Dify, and related platforms. It extracts **model names** when probes support JQ-based model listing.

Julius does **not**:

- Discover open ports (use **Naabu** or **Nmap**)
- Brute-force credentials or bypass authentication
- Replace full web app testing (use Augustus for LLM security after fingerprinting)

---

## Level 0 — Install

Download from https://github.com/praetorian-inc/julius/releases or build from source:

```bash
go install github.com/praetorian-inc/julius/cmd/julius@latest
julius --help
```

---

## Level 1 — First probe

```bash
julius probe https://target.example.com
```

Human table output shows SERVICE, SPECIFICITY, CATEGORY, MODELS.

For SpiderFeet, always use structured output:

```bash
julius probe -o json https://target.example.com
julius probe -o jsonl https://target.example.com:11434
```

Example JSONL line:

```json
{"target":"https://10.0.0.5:11434/api/tags","service":"ollama","matched_request":"/api/tags","category":"self-hosted","specificity":100,"models":["llama3.2"]}
```

---

## Level 2 — Target lists

### File

```bash
cat > ai_targets.txt <<EOF
https://lab.internal:11434
https://lab.internal:8000
https://gateway.corp:443
EOF

julius probe -f ai_targets.txt -o jsonl -o julius_out.jsonl
```

### Stdin

```bash
cat ai_targets.txt | julius probe - -o jsonl
```

### Target normalization

| Input | Normalized |
|-------|------------|
| `192.168.1.10:11434` | `https://192.168.1.10:11434` |
| `https://host/` | `https://host` |

---

## Level 3 — Output formats

| `-o` value | Format | Use |
|------------|--------|-----|
| `table` | ASCII table | Manual review (default) |
| `json` | JSON array | Small batches |
| `jsonl` | JSON Lines | **Automation / SpiderFeet** |

### Parse JSONL in Python

```python
import json
from urllib.parse import urlparse

nodes, edges = [], []

with open("julius_out.jsonl", encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        host = urlparse(row["target"]).hostname
        nodes.append({
            "type": "SOFTWARE_USED",
            "data": row["service"],
            "metadata": {"specificity": row["specificity"], "category": row["category"]},
        })
        for model in row.get("models") or []:
            nodes.append({"type": "SOFTWARE_USED", "data": model, "parent": row["service"]})
```

Full mapping: `.cursor/skills/julius/references/nugget-mapping.md`

---

## Level 4 — Adaptive probing

| Symptom | Fix |
|---------|-----|
| Empty results on known Ollama | `-v` for debug; check HTTPS vs HTTP |
| `error` timeouts | `-t 15` or `-t 30` |
| Slow on many hosts | `-c 50` (careful on corp nets) |
| Only generic OpenAI match | Low specificity — corroborate manually |
| Need custom signature | Copy probe YAML → `julius validate` → `-p ./probes` |

```bash
julius probe -t 20 -c 25 -f targets.txt -o jsonl
julius probe -v https://host:8000
```

---

## Level 5 — Naabu → Julius pipeline

```bash
# 1. Find AI-related ports
naabu -host corp.example.com -p 11434,8000,8080,7860,4000,3000 -json -silent -o naabu.jsonl

# 2. Build URLs (jq)
jq -r '"https://" + (if .host then .host else .ip end) + ":" + (.port|tostring)' naabu.jsonl > urls.txt

# 3. Fingerprint
julius probe -f urls.txt -o jsonl -o julius.jsonl
```

---

## Level 6 — Probe catalog and custom probes

```bash
julius list
julius list -o json | jq '.[].name'

julius validate ./my-probes
julius probe -p ./my-probes -o jsonl https://custom:9000
```

Match rules: `.cursor/skills/julius/references/match-rules-and-probes.md`

---

## Level 7 — Augustus handoff (authorized only)

```bash
julius probe --augustus -o json https://llm.internal:8000
```

Use generator configs with the Augustus skill for LLM vulnerability scanning — only on approved targets.

---

## Level 8 — SpiderFeet formal examination

Per `.cursor/skills/cli_app_profiling/SKILL.md`:

| Scenario class | Example |
|----------------|---------|
| Positive | Lab Ollama on 11434, `-o jsonl` |
| Rich | Row with `models[]` populated |
| Multi-target | `-f targets.txt` |
| Clean miss | `https://example.com` |
| Catalog | `julius list -o json` |

Store under `.docs/docs-for-cli-tools/app_examination_docs/julius/scenarios/<key>/`.

---

## Supported services (summary)

32 probes across self-hosted LLM servers, gateways, RAG platforms, and one generic OpenAI-compatible fallback. See `.cursor/skills/julius/references/probes-and-services.md` or the [Supported Services wiki](https://github.com/praetorian-inc/julius/wiki/Supported-Services).

---

## Quick reference

```bash
julius probe -o jsonl -f targets.txt          # baseline automation
julius probe -t 15 -c 50 -f big.txt -o jsonl  # scale tuning
julius list -o json                             # probe inventory
julius validate ./probes                        # custom YAML QA
naabu ... -json | jq ... | julius probe - -o jsonl  # chain
```

CLI details: `Julius-CLI-Options.md`
