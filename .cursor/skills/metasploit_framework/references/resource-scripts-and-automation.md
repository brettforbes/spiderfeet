# Resource Scripts and Automation

Automation entrypoints:

- `msfconsole -r script.rc`
- `msfconsole -x "<commands>"`

Best practices:

- Set workspace explicitly in each script.
- Keep script steps deterministic (`use`, `set`, `run`, reporting commands).
- Capture output for structured parsing or DB export.
