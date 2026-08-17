# 20. Refine Composer 2

## 1. Change nugget_instance_id to use UUID4 not UUID5 for entities and subentities

In the analysis above, you show that one of the issues for Nerva is that because the nugget_instance_id is a UUID5, then it generates overlaps, which then conflict with the ability to use a recursive transitive relation like `contains`.

Currently the nugget instance id is set as shown in the following section

### 1.1 Current Nugget instance IDs (uuid5)

Canonical implementation: `.seed/scripts/cli_corpus/core/graph_builder.py` → `nugget_instance_id()`

```python
ONTOLOGY_NAMESPACE = uuid5(NAMESPACE_DNS, "OS Threat, OS Intel Ontology")

def nugget_instance_id(nugget_id: str, data: str) -> str:
    return f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, data)}"
```

So for every CLI graph node:

| Piece | Value |
|-------|--------|
| Namespace | `uuid5(NAMESPACE_DNS, "OS Threat, OS Intel Ontology")` |
| Name / seed | canonical `nugget_data` string |
| Final id | `{nugget_id}--{uuid5(...)}` (double dash) |

`id` and `nugget_instance_id` are set to the same value. `GraphBuilder` dedupes on that id, so the same `(nugget_id, nugget_data)` only appears once.

Older seed text in `.seed/05_Onotology_for_Nuggets.md` still shows a single `-` and a different namespace string — CLI adapters follow `graph_builder.py`, not that older snippet.

The nuggets that have those id's are:

| `nugget_type` | Role in CLI graphs | How `nugget_data` is typically chosen |
|---------------|--------------------|--------------------------------------|
| **ENTITY** | `HOST`, `SERVICE`, `IPV4_ADDRESS`, `SCAN_RECORD`, … | Fact value (IP, hostname, service name, scan key) |
| **SUBENTITY** | `PORT`, `RSA`/`ECDSA`/…, `CPE_URL`, `TRACE_HOP`, … | Port number, fingerprint, CPE string, hop IP |
| **DESCRIPTOR** | `HOST_STATUS`, `HTTP_TITLE`, `SCAN_CLI`, … | Attribute value (status, title, CLI string) |
| **CATEGORY** | `NETWORKS`, `APPLICATIONS`, `ENVIRONMENT`, … | Often a scoped key like `networks:{host}` / `applications:{host}` (or a fixed label) so category instances stay per-host |

### 1.2 Proposed Change to Nugget instance IDs (uuid4)

As described, we need to change the nugget instance id to use UUID4 instead of UUID5 on some of the nuggets so that they don't overlap. We should definitely leave the descriptor nuggets alone, as they are not used for the recursive transitive relation `contains`.

We need to change the following nugget types to use UUID4 throughout all of our code in the CLI App Profiling and the new SpiderFeet v2 codebase:

- ENTITY
- SUBENTITY
- CATEGORY

## 2. Fixing the Nerva issue, where results from NMAP are never read

In the analysis above, you show that one of the issues for Nerva is that because the nugget_instance_id is a UUID5, then it generates overlaps, which then conflict with the ability to use a recursive transitive relation like `contains`. In the previous section we show that we need to change the nugget_instance_id to use UUID4 for the ENTITY, SUBENTITY, and CATEGORY nugget types. This takes care of the first problem you analysed.

The second problem you described about Nerva is that the results from NMAP are never read. Consider that with our workflow model, we need to make sure that Nerva can take in a list of ip address with colons and ports like this: `192.168.1.1:80,192.168.1.2:443,192.168.1.3:8080`, regardless of where it comes from. We should not try to make Nerva work with NMAP, instead we need to adjust the woprkflow model, so that Nerva expects a list with the correct format.

Thus the output variables from NMAP that are used by Nerva must be in the specified format, so that Nerva can read them and use them in the correct way. So this is a task for NMAP to make sure it produces the output variables in the correct format, assuming they are correctly specified by the Graph Selection Language.

On the Nerva side we need to make sure the module is updated to take the list of output variables from the workflow manager and use them in the correct way. The message you wrote was:

```
2. Results written to --output are never read

12A points Nerva at --output $step.files.output. Nerva writes JSONL to that file and leaves stdout empty. Nmap/Subfinder/Httpx hydrate from the -o file; Nerva does not. SpiderFeet then builds an empty success graph.

```

So we need to make sure that Nerva can read the output variables from the workflow manager and use them in the correct way.

## 3. Fix the Nuclei issu, where nothing ran

The error message you gave for Nuclei above is:

```
Nuclei — timeout; bundling did not run
Katana produced 225 URLs plus 23 hostnames (GSE also selects DOMAIN_NAME). Those were passed as one -l file. Nuclei then hit ERROR: timeout after 900.0s.

It is not bundling 10 URLs at a time on this path.

sfp_cli_nuclei can chunk targets (DEFAULT_BATCH_SIZE is 20, from SPEC-014), but only if the spec has urls / hosts / host_list and len(targets) > batch_size. The workflow engine only passes:

argv (including -l pointing at the full file)
target = first URL
timeout = 900
So _collect_urls sees one URL, batching never starts, and one Nuclei process runs the full template tree against all ~248 lines until the 900s wall clock kills it.

SPEC-018 also locked “one batched CLI per step / no per-value fan-out,” so Composer progress is 0/n then n/n for the whole list, not 10-at-a-time.

```

The module needs some major work, as it is clear that we need:

1. Take in the list of URLs to the Nuclei module that enables it to bundle and execute the bundles
2. Chunk the list of URLs into batches of 20
3. Execute the bundles in batches of 20
4. Return the results to the workflow manager
5. Set the timer to suit this bundling approach, regardless of how complex each scan is (i.e. how many templates are run)

## 4. Fix the YAML DSL Visualisation Rules

The YAML DSL Visualisation Rules are not working correctly. The message you gave for this is:

```
Those edges are a mapper bug, not something 12A asked for.

HTTPX and Katana both have context.export: none. They should not have a step→collector edge. The collector on that row is still correct, because Nmap (same row as HTTPX) and Nerva (same row as Katana) do export.

What went wrong: C3 only stopped tagging those links as semantic-export. The collector’s Nice-DAG dependencies are still every step on the rank, not only exporters:
const deps = atRank.map((s) => s.id);
if (prevCollectorId) deps.push(prevCollectorId);
const col = {
  id: cid,
  dependencies: deps,
  ...
};
...
for (const s of exporters) {
  edgeMeta.set(edgeKey(s.id, cid), EDGE_TYPE.SEMANTIC_EXPORT);
}

Nice-DAG draws an edge for each dependency. HTTPX/Katana are in deps, so you still get a line to the collector. Unlabeled edges default to followed-by (blue), which is why they look like sequence edges instead of purple semantic-export.

The smoke test missed this: it checks edgeMeta.has(httpx → collector) (false, because the label was never set) and never checks that Nice-DAG actually omitted the dependency.

Should be: collector dependencies = exporting steps only (nmap / nerva) plus the previous collector. HTTPX and Katana stay on the row with no collector edge.
```

Clearly this is incorrect. The `followed-by` and `used-by` edges can only connect veritcal input and output ports based on the existing rules, they can never connect the context ports which are horizontal. This rule can never be broken

Can you work out how to fix this so the redrawing of the viz is robust, but still obeys they flows in the YAML DSL?
