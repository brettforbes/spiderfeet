# Development Metadata and Stability

Before running modules (especially anything beyond passive-ish scanners), review:

1. **`info`** — description, options, references  
2. **`info -d`** — module documentation when present  
3. **Reliability / side effects / stability** metadata — official definitions:  
   https://docs.metasploit.com/docs/development/developing-modules/module-metadata/definition-of-module-reliability-side-effects-and-stability.html  
4. **Datastore guidance** —  
   https://docs.metasploit.com/docs/development/developing-modules/module-metadata/how-to-use-datastore-options.html  
5. **In-repo module docs** — `documentation/modules/**`

## SpiderFeet defaults

- Prefer modules with clear scanner/gather semantics and DB host/service writes.
- Avoid modules whose side effects imply crash, reboot, or data loss unless the lab explicitly allows them.
- Do not treat “module exists in `search`” as “safe to run.”

## Contributing / module quality (upstream)

- https://github.com/rapid7/metasploit-framework/blob/master/CONTRIBUTING.md  
- https://docs.metasploit.com/docs/development/maintainers/process/guidelines-for-accepting-modules-and-enhancements.html  
- https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-get-started-writing-an-auxiliary-module.html  
- https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-write-a-check-method.html  
