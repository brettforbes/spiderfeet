# Rethinking Nuclei Scanning


## Scanning Strategy

Don’t run everything, Start looking for:

    Misconfiguration templates
    Exposure templates
    Authentication & access-control related checks
    Technology-specific templates (only when relevant)

Avoid:

    Broad “informational” sets
    Low-confidence generic checks

Ask:

    “If this template hits, can I chain it?”

If the answer is no, skip it.

Think in batches:

    One target group
    One risk category
    One goal

For example:

    “This scan is only looking for exposed admin panels”
    “This run is only about auth misconfigurations”
    “This scan is just tech fingerprinting for chaining”

## Scanning using Tags - Standard Tags

The most common, valid standard tags used inside the official ProjectDiscovery Nuclei Templates repository are classified below by category:

### Vulnerability Types (Bug Bounty / Pentesting):

- `rce` — Remote Code Executions
- `qli` — SQL Injectionxss — Cross-Site Scripting
- `lfi` / `rfi` — Local/Remote File Inclusion
- `ssrf` — Server-Side Request Forgery
- `ssti` — Server-Side Template Injection
- `deserialization` — Insecure Deserialization vulnerabilities
- `idor` — Insecure Direct Object References
- `misconfiguration` — Security misconfigurations
- `exposure` — Exposed sensitive files, tokens, or credentials

## Technologies & Software Stacks
- `cve` / `cve2024` / `cve2025` — Specific Common Vulnerabilities and Exposures
- `wp` / wordpress — WordPress core, plugins, and themes
- `jira` / atlassian — Atlassian Jira and ecosystem products
- `aws` / `s3` / `cloud` — Cloud platforms and storage misconfigurations
- `apache` / `nginx` / `tomcat` — Specific web servers
- `generic` / `default-login` — Generic checks and panels with factory credentials
- `panel` / `admin` — Control panels and administrative interfaces

### Protocol & Infrastructure Types:

- `http` — Web application targets
- `dns` — Domain Name System routing and records
- `tcp` / `udp` — Network level port scanning and raw sockets
- `ssl` / `tls` — Certificate issues and weak configurations
- `fuzz` — Fuzzing templates (Note: disabled by default, requires the -itags fuzz flag)
- `osint` — Open-source intelligence and profile gathering


## Nuceli selective Scanning

Selective scanning techniques
- only scan for CVEs `nuclei -u <https://target.com> -tags cve`, make sure you include these additional templates
- Only scan for exposed panels `nuclei -u <https://target.com> -tags panel,exposure`
- Only scan for critical issues `nuclei -u <https://target.com> -severity critical,high`
- Only scan WordPress sites `nuclei -u <https://target.com> -tags wordpress`
- Only scan Apache servers `nuclei -u <https://target.com> -tags apache`
- Only scan Joomla `nuclei -u <https://target.com> -tags joomla`
-  Exposures Sensitive Files `nuclei -l targets.txt \
  -t ~/nuclei-templates/exposures/ \
  -o exposures_found.txt`

 Yeh dhundta hai:
 → .env files
 → .git directory
 → config files
 → API keys in pages
 → AWS credentials
 → Private keys
 → Backup files

- Default Logins Instant Access - nuclei -l targets.txt \
  -t ~/nuclei-templates/default-logins/ \
  -o default_login_found.txt

 Yeh check karta hai:
 → admin:admin
 → admin:password
 → root:root
 → test:test
 → Jenkins default credentials
 → Grafana default credentials
 → Kibana default credentials
 → Router default passwords

### Targets we want to use nuclei templates to scan for

Targets we want to use nuclei templates to scan for:

- Template #1: “Is admin panel accessible without login?”
- Template #2: “Can I read sensitive files?”
- Template #3: “Is there SQL injection in login form?”
- wordpress, then run templates from here https://github.com/topscoder/nuclei-wordfence-cve in addition to the nuclei wordpress ones
- Postman collections: Public links or exported files
- GitHub leaks: .env, .http, API keys in public repos
- Swagger/OpenAPI: /swagger.json, /openapi.json
- Exposed admin panels
- Open metrics endpoints
- Debug endpoints
- Unauthenticated APIs
- Forgotten staging environments
- Misconfigured CORS
- Auth bypass patterns


## Some Additional Techniques for API Pentesting

1. Detecting Swagger with Nuclei

Swagger (OpenAPI) files are often exposed under predictable paths like /swagger.json or /v2/api-docs. If left unprotected, they give attackers a full map of the API.

Basic template (swagger-detect.yaml):

id: swagger-detect
info:
  name: Swagger Documentation Exposed
  author: security.warrior
  severity: medium
requests:
  - method: GET
    path:
      - "{{BaseURL}}/swagger.json"
      - "{{BaseURL}}/v2/api-docs"
    matchers:
      - type: word
        words:
          - '"swagger"'
          - '"openapi"'

2. Testing for Broken Object Level Authorization (BOLA)

One of the most common API flaws is IDOR/BOLA, where attackers access resources of other users by simply changing IDs.

Template (api-bola.yaml):

id: api-bola
info:
  name: Broken Object Level Authorization
  severity: high
requests:
  - method: GET
    path:
      - "{{BaseURL}}/users/2"
    matchers:
      - type: word
        words:
          - '"username"'
          - '"password"'

Legitimate request:

GET /users/1 HTTP/1.1
Host: api.vulnerable-app.com

Malicious request:

GET /users/2 HTTP/1.1
Host: api.vulnerable-app.com

Vulnerable response:

{
  "id": 2,
  "username": "admin",
  "password": "hashed_password"
}
This confirms a BOLA vulnerability, exposing sensitive user data.

3. Detecting Mass Assignment

Some APIs accept extra parameters not defined in the schema, leading to privilege escalation.

Template (api-mass-assignment.yaml):

id: api-mass-assignment
info:
  name: Mass Assignment in API
  severity: critical
requests:
  - method: POST
    path:
      - "{{BaseURL}}/users"
    body: |
      {
        "username": "newuser",
        "password": "123456",
        "role": "admin"
      }
    headers:
      Content-Type: application/json
    matchers:
      - type: word
        words:
          - '"role": "admin"'

Vulnerable response:

{
  "id": 45,
  "username": "newuser",
  "role": "admin"
}

The application assigns an admin role simply because it was provided in the request body.
4. SQL Injection in APIs

Poorly validated inputs in APIs can still be vulnerable to SQL injection.

Malicious request:

GET /products?id=1' OR '1'='1 HTTP/1.1
Host: api.vulnerable-app.com

Response Example:

[
  { "id": 1, "name": "Laptop", "price": "1000" },
  { "id": 2, "name": "Mobile", "price": "500" },
  { "id": 3, "name": "Tablet", "price": "700" }
]

Instead of returning one product, the API dumps the entire database table — confirming SQL injection.
5. Building an Automated Workflow

This is where Nuclei really shines: chaining all templates together into a single workflow.

Workflow (api-pentest-workflow.yaml):

id: api-pentest-workflow
info:
  name: API Pentesting Workflow
  author: security.warrior
  severity: high

workflows:
  - template: swagger-detect.yaml
    subtemplates:
      - api-bola.yaml
      - api-mass-assignment.yaml
      - nuclei-templates/http/vulnerabilities/common/sql-injection.yaml
      - nuclei-templates/http/vulnerabilities/common/xss.yaml

Run it with a single command:

nuclei -w api-pentest-workflow.yaml -u https://api.vulnerable-app.com

This pipeline automatically detects Swagger exposure, enumerates endpoints, and tests for BOLA, Mass Assignment, SQLi, and XSS

