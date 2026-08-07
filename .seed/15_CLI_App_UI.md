# Simple UI for Every CLI App, and every API

Our experimental **"CLI Profiling"** exploration and examinations of the capabilities of the CLI tools has been a great success, and is going to form the basis of a complete reengineering of SpiderFeet into a more powerful and user-friendly tool, where each the output of each OSINT Service, either API or CLI app, can be converted into a semantic subgraphs rather than just atomic niggets of data, based on an overall ontology, so that the semantic meanings can be converted into narrative reports and the subgraphs added together to form a complete picture of the target.

Thus, each CLI APP can only see part of the picture, and the aim is  to convert them into a common ontology, so that the data can be converted into narrative reports and the subgraphs added together to form a complete picture of the target. 

Importantly the user interface that we use for exploring the examination outputs for each tool, has turned out to be very useful, and the intent of this propmpt is to extend it and turn it into a generic, simple UI useful for every CLI App, to setup and run any single scan. The aim will be to abstract this functionality out as a module that we can reuse in the Composer page of the UI.

## 1. Current UI Capabilities for the CLI App Tool Examinations

Let us consider the capabilities of the 3 existing pages:

1. **CLI APP PROFILING All Tools PAGE**: Review formal CLI examination captures and nugget graph proposals. Edit artifacts in the repo; use Approve/Reject to update review status files. Table includes one row per CLI App, with the following columns:


| Tool | Phase | Exams | Runtime | Notes | Actions |
|------|-------|------:|---------|-------|---------|
| nmap | complete | 15 | windows | Pilot complete 2026-06-26 — 15 scenarios operator-approved; narrative reports; graph structure + 15 JSON/MD artifacts; template for next CLI tools | [Structure](.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md) |
| netdiscover | complete | 5 | windows-lan | Complete 2026-06-29 — 5 scenarios operator-approved; graph_builder + MAC_VENDOR; narrative reports with Mermaid; windows-lan harvest | [Structure](.docs/docs-for-cli-tools/nugget_structure/netdiscover_nugget_graph_structure.md) |
| nerva | formal_examination | 6 | windows | Formal examination 2026-06-30 (#881) — 7 scenarios; JSONL + human text; graph structure in nugget_structure/ | [Structure](.docs/docs-for-cli-tools/nugget_structure/nerva_nugget_graph_structure.md) |
| nuclei | formal_examination | 5 | windows | 2026-07-05 pentest-ground matrix harvest — scanme severity baseline; ShadowLogic WebLogic CVEs; CipherHeart Redis CVE-2022-0543; GraphQL misconfig; DVWA tech fingerprint | [Structure](.docs/docs-for-cli-tools/nugget_structure/nuclei_nugget_graph_structure.md) |
| pius | formal_examination | 6 | wsl | 2026-07-05 manifest v4 — replaced obscure/scanme/rir with Square Peg + Upside gleif stacks; K2 deferred (offline) | [Structure](.docs/docs-for-cli-tools/nugget_structure/pius_nugget_graph_structure.md) |
| subfinder | formal_examination | 8 | windows | 2026-07-06 org-size matrix — upside/squarepeg/vcof/k2am/sbs + active IP + invalid clean miss; JSONL→records[] bundle | [Structure](.docs/docs-for-cli-tools/nugget_structure/subfinder_nugget_graph_structure.md) |
| httpx | formal_examination | 8 | windows | 2026-07-06 subfinder-fed web probes — host lists from subfinder exams; JSONL→httpx_probe_v1 bundle | [Structure](.docs/docs-for-cli-tools/nugget_structure/httpx_nugget_graph_structure.md) |
| katana | formal_examination | 2 | windows | 2026-07-06 httpx-fed crawls — seed URL lists from httpx exams; JSONL→katana_crawl_v1 bundle | [Structure](.docs/docs-for-cli-tools/nugget_structure/katana_nugget_graph_structure.md) |


2. **CLI APP PROFILING Single Tool Scan Scenarios PAGE**: for example `nmap/scenarios` which shows a table of the scan scenarios for the nmap tool, with the following columns:

| Scenario | Target | Artifacts | Review | Format |
|----------|--------|-----------|--------|--------|
| **K — capstone permissive (XML)**<br/>`capstone_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **A — host discovery corporate (XML)**<br/>`host_discovery_corporate` | bbc.co.uk | txt · data · graph · md | approved | xml |
| **B — host discovery local subnet (XML)**<br/>`host_discovery_local_subnet` | 192.168.1.0/24 | txt · data · graph · md | approved | xml |
| **A — host discovery permissive (XML)**<br/>`host_discovery_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **G — NSE default permissive (XML)**<br/>`nse_default_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **F — OS aggressive permissive (XML)**<br/>`os_aggressive_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **E — service version corporate (XML)**<br/>`service_version_corporate` | bbc.co.uk | txt · data · graph · md | approved | xml |
| **E — service version permissive (XML)**<br/>`service_version_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **J — skip ping permissive (XML)**<br/>`skip_ping_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **D — TCP top ports corporate (XML)**<br/>`tcp_top_ports_corporate` | bbc.co.uk | txt · data · graph · md | approved | xml |
| **C — TCP top ports local subnet (XML)**<br/>`tcp_top_ports_local` | 192.168.1.0/24 | txt · data · graph · md | approved | xml |
| **C — TCP top ports permissive (XML)**<br/>`tcp_top_ports_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **I — traceroute permissive (XML)**<br/>`traceroute_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **H — UDP top ports permissive (XML)**<br/>`udp_top_permissive` | scanme.nmap.org | txt · data · graph · md | approved | xml |
| **L — Windows enrich local host (XML)**<br/>`windows_enrich_local` | 192.168.1.12 | txt · data · graph · md | approved | xml |


3. **CLI APP Profiling Single Scan Page**: for example `nmap/scenarios/capstone_permissive` which shows the details of the capstone_permissive scan scenario for the nmap tool, and is entitled `nmap — K — capstone permissive (XML)`

The page for every specific scane scenario is identical, and contains four tabs:

1. **Text** Tab: Shows the raw text output of the scan scenario, or that produced by the scan module (i.e. if the output is structured).
2. **Structured Data** Tab: Shows the structured data output of the scan scenario, using the specialised Data Viewer UI component.
3. **Graph** Tab: Shows the graph output of the scan scenario, using our standard Graph Viewer UI component.
4. **Report** Tab: Shows the narrative report output of the scan scenario, using our standard markdown Report Viewer UI component.


## 2. Building on What Exists, Based on the Existing Scan Examination Data

The four tabs of the single scan page are built on the existing examination data, and they perfectly map the ways we want a user to be able to viewa CLI App Scan. These four different views: text, structured, graph and narrative report, are the four views we want to be able to use for every CLI App Scan. Since CLI Apps are the superset semantically of API services, we can also apply the same four components to see the output of any API service.

The one thing that is missing is a tab for the CLI App Command prompt that was used to produce the scan, and the output of the scan. This is a very important tab, as it allows the user to see the exact command that was used to produce the scan, and the output of the scan. So its useful as a record. But if we make it a real-live user interface, then one can use it to select the scan options you want before running the scan.

The UI for the CLI App and API scans thus has five tabs:

1. **Scan** Tab: Shows the user interface for the scan, with any UI controls required to enable the user to select any valid set of options and flags for the scan, and the buttons to execute the scan and access content
2. **Text** Tab: Shows the raw text output of the scan scenario, or that produced by the scan module (i.e. if the output is structured).
3. **Structured Data** Tab: Shows the structured data output of the scan scenario, using the specialised Data Viewer UI component.
4. **Graph** Tab: Shows the graph output of the scan scenario, using our standard Graph Viewer UI component.
5. **Report** Tab: Shows the narrative report output of the scan scenario, using our standard markdown Report Viewer UI component.

four of these tabs already exist, and the first is the main focus of this document. That and extracting the entire five tabs into a single module that can be reused for every CLI App and API Service.

### 2.1 Aim of the CLI App User Interface

In short, if we have a user interface that exactly models all of the CLI App options and flags, then we can use it for two jobs:

1. **To Specify and Run a CLI App Scan**: In this the user interface components are all in edit mode where the user can select the scan CLI options and flags, and then click the "Run Scan" button to run the scan.
2. **To View the Settings for a CLI App Scan**: In this the user interface components are all in read-only mode where where the user can use the user interface to see the scan options that were used to produce the scan, and the output of the scan.

To do this its convenient to realise that the entire user interface is clearly defined with data and hence can be setup dynamically from the data, rather than hard coded into the code base. This is called `content-driven` UI design, getting content and data from the FastAPI server, and it is a key feature of the system.

### 2.2  Fast API Structure for 3 Types of Content for every Tool or API Service

Importantly, every CLI App tool has a single file that defines all of the options and flags for the tool, and this file in its original form is the source of truth for the user interface for that specific tool. Further, we plan to ship with more than 20 tools built in, and the ability to make it easy to add new user interfaces for new tools is a key feature of the system.

Ideally, we setup a specific directory in the SpiderFeet code base to store an identical set of key content pieces for each CLI App or API Service, that act as a reference for the user interface for that specific tool. We need three key content pieces for each tool, using NMAP as an example below:

1. **Nmap — proposed nugget graph structure** `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`
2. **Nmap — raw cli options and flags --help raw text output** (the source of truth for the user interface for the tool) `.docs\docs-for-cli-tools\NMAP-CLI-Options.md` which is a markdown document that lists all of the CLI options and flags for the tool.
3. **Nmap — Zero to Hero Guide** `.docs\docs-for-cli-tools\NMAP-Zero-to-Hero.md`

And what we need is to copy these same 3 content pieces for each of the currently supported CLI Apps into the new `modules_v2\content` directory as official references. In a future stage we will import those 3 strings into the SpiderFeet database, but as an interim measure we want to setup API's as needed so Fast API will retrieve the 3 strings for any tool or api service directly from the `modules_v2\content` directory. 

Every time we complete onboarding of a new API Service, or CLI App, we will need to generate and store a copy of the 3 content pieces into the `modules_v2\content` directory. These will be the official references for the user interface for that specific tool. Initially, the content for the API will be file-based, but later on this will be changed to originate as a query from the `spiderfeet-db` TypeDB database, even if later on they are saved and then served from TypeDB to the API. This is because this specific UI is still a part of the whole, so we can easily use the synthetic, file-based API's as a testing ground for the API's that will be used to serve the content from TypeDB to the API, and in a later project we make this more robust.

Design the API's assuming they need to service those 3 content pieces for at last 200 API services and 30 CLI Apps, possibly more in the future. So design the API's to support this number, each with the same signature of `3 * Types of Content` pieces, and to be able to scale to more in the future.

Make sure you update the rules for onboarding new cli apps and api services to include the need to generate and store the 3 content pieces into the `modules_v2\content` directory, and update the API platform to accomodate the new content pieces.

### 2.3 CLI App "Scan" User Interface Design

Now we want to create the 5 tab mini app as a component in the Spiderfeet widget code base, so we can use it in many situations, not just for the  Cli App Profiling, but also in the Composer User Interface. So the component has 5 tabs:

1. Scan
2. Text
3. Structured Data
4. Graph
5. Report

And this subsection is a sketch of the details for the "scan" tab only. We note that description belowneeds to be expanded to suit all of the details contained in the first set of 8 CLI Appoptions:

- `.docs\docs-for-cli-tools\NMAP-CLI-Options.md`
- `.docs\docs-for-cli-tools\Httpx-CLI-Options.md`
- `.docs\docs-for-cli-tools\Nerva-CLI-Options.md`
- `.docs\docs-for-cli-tools\Subfinder-CLI-Options.md`
- `.docs\docs-for-cli-tools\Katana-CLI-Options.md`
- `.docs\docs-for-cli-tools\Nuclei-CLI-Options.md`
- `.docs\docs-for-cli-tools\Pius-CLI-Options.md`
- `.docs\docs-for-cli-tools\Netdiscover-CLI-Options.md`

GENERATION_PROMPT = """You are a UI generator. Given a CLI tool's --help output, generate a COMPLETE,
self-contained HTML file with embedded CSS and JavaScript that provides a web interface for the scan using that CLI. Put it in the first tab, marked `Scan`, of the 5 tab mini app. Make it based on bootstrap and HTML, and dynamic, so it can be configured almost instantly by receiving the 3 content files. Further, the content in the other tabs should also be provided from the FastAPI server, so the UI is fully dynamic and can be configured almost instantly by receiving the 3 content files, plus the 4 output files if the scan is complete. This UI is used in two scenarios, 

1. **User interface for the existing examination tables**, where the content is provided by API, but retrieved from their current hard coded disk locations
2. **User interface for the new Composer page**, where the content is provided by API, and retrieved from the TypeDB database.

Rules:

1. Every flag/option becomes a form field:
   - String flags → text input
   - Boolean flags → checkbox
   - Integer/float flags → number input
   - Flags with a fixed set of choices → select dropdown
   - File path flags → text input with a "browse" label hint
2. Every description becomes a label/help text
3. Every default value becomes a placeholder or pre-filled value
4. Required flags get a red asterisk
5. Group related flags into collapsible sections if there are more than 10 flags. Keep the command line options in the first 9 columns and make it scrollable if needed. 
6. In the right hand three columns keep the buttons to execute the scan, as well as 3 different buttons (`Options`, `Graph Structure`, `User Guide`) to bring up a modal showing a markdown document, the CLI App Proposed Graph Structure `Nmap — proposed nugget graph structure`, the CLI App Options Text `Nmap — raw cli options and flags --help raw text output` and the CLI App Zero to Hero Guide `Nmap — Zero to Hero Guide`, Make sure there is a time the scan was created a progeress bar id it is still running and a time finished once it is complete at the bottom of the right three columns.
6. Include a LIVE "Command Preview" panel at the bottom right  that shows the exact CLI command
   being constructed as the user fills in fields
7. Include an "Execute" button (wired to a POST /execute endpoint placeholder) that will run the scan and show the output in the `Results` tab.
8. Include a dark/light mode toggle
9. Make it look clean and modern — use CSS grid, subtle shadows, good typography
10. The HTML must be compatible with the existing widget code, using HTML and Bootstrap 5.3.0.

### 2.4 The Component in the Widget

So the idea is to extract out the above capability into a indepednent component in the widget code base, so it can be used in many situations, not just for the  Cli App Profiling, but also in the Composer User Interface. Initially as an outcome, make sure this new component can be shown cleanly as **CLI APP Profiling Single Scan Page**, so that each time the user clicks on a row in the examination tables, the component is shown and the content is provided by the API, and retrieved from the TypeDB database. Achieveing this will be a key milestone for this step of the project.