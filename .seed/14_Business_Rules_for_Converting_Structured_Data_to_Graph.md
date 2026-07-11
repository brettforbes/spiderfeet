# Business Rules for Converting Structured CLI App Output into a Common, Semantic Graph

## 1. Background

The output of a CLI App is seen as the semantic superset of the output of a Spiderfeet scan. Thus, by converting the output of a CLI App into a common, semantic graph, we will be able to use the same rules and processes to convert the output of a Spiderfeet scan into a common, semantic graph.

### 1.1 App-Specific Code

The exploration and examination of the CLI apps has demonstrated that app-specific code is required for:

1. Running the CLI app, including providing the command line arguments and preparing a temporary input list file for the app to process.
2. Parsing the app's output and extracting the output and providing both a structured and text form of the output

There are two different types of CLI Apps:

1. CLI Apps that can output data in a structured format. In this case, the app-specific code will be used to create the standard scan record, and the text to be output to the Text window
2. CLI Apps that can only output data in a text format. In this case, the app-specific code will be used to create the standard scan record, using TextFSM to parse the text output and convert it to a structured format, and then text to be output to the Text window will be the raw output of the CLI app.

### 1.2 Current Approach Used to Convert Structured Data into a Common, Semantic Graph

Converting the structured data (JSON, XML) into a common, semantic graph format requires a lot of decisions and rules in order to convert CLI app outputs into a semantic subgraph of a common ontology,  some of which will be app-specific (65-75%), and some of which are common across all CLI apps (25-35%).

Currently, we have explored and examined 8 CLI apps, but only two have been converted to a common, semantic graph so far, NMAP and NetDiscover. What we did in those two cases was to embed all of these rules and decisions in code inside the CLI app-specific code. So the code becomes very intricate and fragile to changes. Once we realised this, we focused on only completing the first part of the examination, and then developing rules and ontology extensions for the other 6 CLI apps.

But extracting out rules into a central system seems highly feasible in our current architecture, because we already have some early building blocks:

- Shared graph primitives already exist in `\.seed\scripts\cli_corpus\graph_builder.py` (`nugget_node`, dedupe by (`nugget_id`, `nugget_data`), edge uniqueness, connectivity validation).
- Ontology vocabulary is already externalized in `\.docs\analysis\nuggets.json` and `\.docs\analysis\nuggets_extension.json`.
- Cross-record correlation policy is documented in `\.seed\07_Scan_Record_Host_Correlation_Rulesets.md`.

But the implementation is currently mixed: some parts are centralized, many rules are still embedded in tool-specific Python

### 1.3 Decisions Rules Used to Convert Structured Data into a Common, Semantic Graph

We need to extract these rules using a hybrid approach:

- Declarative for 80% common mapping/merge behavior.
- Small Python hook functions for hard cases (e.g., Nerva A/B/C host-correlation, odd text parsing).
- **Pros**: Best scale/flexibility balance, keeps difficult logic explicit, avoids DSL overreach.
- **Cons**: Needs clear boundaries and governance to avoid sliding back into hardcoded sprawl.


### 1.4 What is hardcoded now and should be abstracted from the current Nmap/Netdiscover CLI-app-specific conversion modules?

There are several embedded rules worth abstracting:

1. Nugget mapping rules in code:

- `nmap_xml_to_graph.py` hardcodes many nugget IDs and mapping behavior (HOST_STATUS, SERVICE_VERSION, TRACE_HOP, SSH key mapping, etc.).
- `netdiscover_json_to_graph.py` hardcodes SYSTEM -> NETWORKS -> IP/MAC.
- `cli_tool_to_graph.py` hardcodes minimal Nerva/Pius mappings.

2. Topology/relationship rules hardcoded:

- `contains`, `had`, `listens-to` wiring is explicit in each converter, not centrally defined as reusable templates.

3. Tool-specific heuristics hardcoded:

- `graph_builder.py` uses `uuid5(ONTOLOGY_NAMESPACE, nugget_data)` with nugget prefix (aligned with ontology intent).
- `cli_tool_to_graph.py` uses a different namespace formula (`uuid.NAMESPACE_DNS + nugget_id:data`), which risks cross-tool identity inconsistency.

4. Ruleset A/B/C from your doc are not implemented yet

- Search in `\.seed\scripts\cli_corpus` shows no implementation of fields like `same_system_*`, `host_classification`, `cdn_vendor`, etc.
- So that policy currently lives in documentation, not executable rule packs.

### 1.5 How many rules are CLI-specific vs cross-module?

For current pipeline behavior, rough split is:

**CLI-app-specific rules**: ~65–75%

- Parse grammar/output normalization.
- Tool-specific field interpretation.
- Tool-specific evidence extraction (e.g., Nmap NSE scripts, Netdiscover TUI/parsable detection).

**Cross-module rules**: ~25–35%

- Ontology catalog lookup.
- Node identity/dedup.
- Edge relation semantics (`contains`, `had`, `listens-to`).
- Graph validation/connectivity.
- Correlation policy class (A/B/C should be here once implemented).

At 20+ apps, this naturally trends toward more shared policy needs, especially for correlation/merge and consistency checks. Without centralization, code duplication will grow nonlinearly.

### 1.6 What to centralize first (highest ROI)?

1. Correlation & consolidation policy

Your A/B/C rules from `\.seed\07_Scan_Record_Host_Correlation_Rulesets.md`.
Provider signatures/ASN allowlists externalized and versioned.
Confidence scoring + fired-rule trace kept as first-class outputs.

2. Ontology mapping templates

- Field-to-nugget mappings, relation templates, required/optional descriptors.
- Per-tool overrides in separate content files.

3. Identity and merge keys

- Canonical IDs, dedupe precedence, conflict handling.
- One shared identity policy used by all tool converters.

4. Validation policies

“No orphan nodes,” required scan descriptors, evidence completeness, scenario coverage checks.

### 1.7 Final recommendation

Use a hybrid rule-engine architecture:

- Keep parsing adapters per CLI app (tool-specific by nature).
- Move mapping/correlation/merge rules into centralized versioned content (rules/).
- Keep Python hooks only for exceptional logic.
- Enforce one canonical identity function across all converters (remove current UUID divergence).
- Treat A/B/C as executable policy next, not just documentation.

This gives us the scalability we want (20+ tools, 4x ontology growth) without sacrificing precision where complex logic is unavoidable.

## 2.0 Conversion of Semantic Graphs to a Markdown Narrative Report Document

One advantage of converting Cli-app-specific data to a common semantic ontology is that the meaning of the scan is encoded in the graph, and can be used to generate a narrative report document. The narraitve report document has access to the scan and all of its descriptors, as well as all the sub-graphs discovered by the scan. The narrative is something simple, facts with some small amount of context, plus explanatory mermaid graphs and tables. For example ...

"A scan was performed on a target (detailed descriptors) ..."

"The scan found, for example, 4 Hosts and 1 Trace, then make a separate section with detailed descriptions of each, with its categories and their contained nuggetsa narrative for each meta-concept found..."

"Appendix with detailed tables of every object and relation in the scan graph"

Clearly there are a lot of oppourtunities for using a centralised set of rules and policies to generate the narrative report document for each CLI app.