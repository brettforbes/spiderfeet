# Conversion pattern index

| Pattern | Count | Description |
|---------|-------|-------------|
| `api_json_map` | 112 | HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types. |
| `api_text_or_html` | 56 | HTTP fetch → text/HTML parsing without structured JSON schema. |
| `dns_network_local` | 19 | DNS, sockets, or validation helpers; no third-party OSINT API. |
| `custom_logic` | 17 | Mixed or module-specific logic not captured by heuristics. |
| `cli_subprocess_parse` | 13 | Runs external CLI; parses stdout/stderr (often line-oriented or JSON-lines) into typed events. |
| `regex_local` | 11 | Primarily regex over event.data or fetched reference files. |
| `content_extract` | 3 | Parses page/content events with helpers/regex; emits derived identifiers. |