# Selective Scan Techniques

Concrete Nuclei command patterns for **one goal per run**. Adapt paths (`-t`, `-l`) to repo layout (e.g. `.tools/nuclei-templates`).

Source: `.seed/03EB_Rethinking_Nuclei_Strategy.md`

## Tag and severity filters

```bash
# CVE-only pass
nuclei -u https://target.com -tags cve -silent -jsonl -no-interactsh

# Exposed panels
nuclei -u https://target.com -tags panel,exposure -silent -jsonl -no-interactsh

# Critical and high only (repeat -severity per shell; on Windows cmd use separate flags)
nuclei -u https://target.com -severity critical -severity high -silent -jsonl -no-interactsh

# Stack-specific (run only after fingerprint confirms stack)
nuclei -u https://target.com -tags wordpress -silent -jsonl -no-interactsh
nuclei -u https://target.com -tags apache -silent -jsonl -no-interactsh
nuclei -u https://target.com -tags joomla -silent -jsonl -no-interactsh
```

## Template path slices

### Exposures — sensitive files

```bash
nuclei -l targets.txt \
  -t ~/nuclei-templates/exposures/ \
  -o exposures_found.txt
```

Looks for:

- `.env` files
- `.git` directory exposure
- Config files
- API keys in pages
- AWS credentials
- Private keys
- Backup files

Prefer `-jsonl` / `-jle` for examination corpus instead of plain `-o` text when harvesting structured bundles.

### Default logins — instant access checks

```bash
nuclei -l targets.txt \
  -t ~/nuclei-templates/default-logins/ \
  -o default_login_found.txt
```

Checks include:

- `admin:admin`, `admin:password`, `root:root`, `test:test`
- Jenkins, Grafana, Kibana default credentials
- Router default passwords

## SpiderFeet-aligned baseline (from nuclei skill)

When comparing to module defaults, manual batches often still use:

```bash
nuclei -silent -jsonl -concurrency 100 -retries 1 \
  -t /path/to/nuclei-templates -no-interactsh -etags dos,fuzz,misc
```

For **strategy runs**, replace the implicit “full tree” with **tag**, **severity**, or **path** filters from this document instead of `-t` on the entire template root.

## Examination export pattern

```bash
nuclei -u https://target.com -tags cve -severity critical -severity high \
  -silent -jsonl -omit-raw -omit-template -no-interactsh -etags dos,fuzz,misc \
  -jle .docs/docs-for-cli-tools/exploration_scratch/nuclei/target_cve_crit_high.jsonl
```

Post-process JSONL → JSON bundle with `records[]` (list of dicts) for CLI Profiling structured pane.

## Related

- [tags-and-categories.md](tags-and-categories.md)
- [sequential-playbook.md](sequential-playbook.md)
- [../../nuclei/references/cli-options.md](../../nuclei/references/cli-options.md)
