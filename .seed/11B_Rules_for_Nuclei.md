# Nuclei JSON → SpiderFeet Graph Transformation Rules
**Version:** 1.0  
**Status:** Draft  
**Purpose:** Deterministically transform a Nuclei JSON document into a SpiderFeet graph consisting of a `nodes[]` array and an `edges[]` array.

---

# 1. Objectives

The transformation engine shall:

1. Convert every Nuclei finding into graph entities.
2. Preserve every security observation.
3. Never create duplicate category entities.
4. Never create duplicate template entities.
5. Reuse existing Host, Service and Port entities from the existing graph whenever possible.
6. Produce deterministic output regardless of JSON ordering.
7. Ignore execution metadata that has no long-term graph value.

---

# 2. Input

The parser accepts a single Nuclei JSON document.

Expected schema:

```text
{
    records[]
}
```

Each record is transformed independently.

---

# 3. Output

The parser produces two arrays.

```text
nodes[]

edges[]
```

## Node Structure

```text
{
    id
    type
    label
    descriptors{}
}
```

## Edge Structure

```text
{
    source
    relationship
    target
}
```

---

# 4. Processing Order

Every document shall be processed in the following order.

```text
Validate JSON

↓

Resolve Host

↓

Resolve Service

↓

Resolve SECURITY

↓

Resolve TEMPLATES_USED

↓

Resolve FINDINGS

↓

Resolve Severity Category

↓

Resolve Template

↓

Create Vulnerability

↓

Create Finding

↓

Create Relationships

↓

Validate Graph

↓

Return Graph
```

---

# 5. Global Rules

## G1

The parser shall process every element of

```text
records[]
```

independently.

---

## G2

Processing order shall not affect graph structure.

---

## G3

Entity lookup shall always occur before entity creation.

---

## G4

Descriptors shall never become entities.

---

## G5

Null values shall not generate descriptors.

---

## G6

Empty arrays shall be ignored.

---

## G7

Missing optional fields shall not generate errors.

---

## G8

Missing mandatory fields shall generate a parser error.

Mandatory fields:

- template-id
- info
- host

---

# 6. Host Resolution

## Rule H1

Read

```text
record.host
```

IF Host exists

THEN

Reuse Host

ELSE

Create Host

---

## Rule H2

Host Identity

Primary

```text
hostname
```

Fallback

```text
ip
```

---

# 7. Service Resolution

## Rule S1

Read

```text
host

port
```

IF Service exists

Reuse

ELSE

Create

---

## Rule S2

Service Identity

```text
host + port
```

---

## Rule S3

IF no Service exists

AND no Port exists

THEN

Skip Service relationships.

---

# 8. SECURITY Resolution

## Rule SEC1

IF SECURITY exists beneath Host

Reuse

ELSE

Create SECURITY

---

## Rule SEC2

Always create

```text
HOST

contains

SECURITY
```

if missing.

---

# 9. TEMPLATES_USED Resolution

## Rule TMP1

IF TEMPLATES_USED exists

Reuse

ELSE

Create

---

## Rule TMP2

Always ensure

```text
SECURITY

contains

TEMPLATES_USED
```

---

# 10. FINDINGS Resolution

## Rule FIND1

IF FINDINGS exists

Reuse

ELSE

Create

---

## Rule FIND2

Always ensure

```text
SECURITY

contains

FINDINGS
```

---

# 11. Severity Resolution

## Rule SEV1

Read

```text
info.severity
```

---

## Rule SEV2

Valid values

```text
info

low

medium

high

critical
```

---

## Rule SEV3

Map

| JSON | Entity |
|-------|--------|
| info | INFO |
| low | LOW |
| medium | MEDIUM |
| high | HIGH |
| critical | CRITICAL |

---

## Rule SEV4

IF Severity Category exists

Reuse

ELSE

Create

---

## Rule SEV5

Always ensure

```text
FINDINGS

contains

Severity Category
```

---

# 12. Template Resolution

## Rule T1

Read

```text
template-id
```

---

## Rule T2

Template Identity

```text
template-id
```

---

## Rule T3

IF Template exists

Reuse

ELSE

Create

---

## Rule T4

Populate Template descriptors.

| Descriptor | Source |
|------------|--------|
| template_id | template-id |
| template_name | info.name |
| path | template-path |
| author | info.author |
| tags | info.tags |
| protocol | type |

---

## Rule T5

Always ensure

```text
TEMPLATES_USED

contains

TEMPLATE
```

---

# 13. Vulnerability Creation

Unlike Templates, Vulnerabilities represent individual security observations.

Every Nuclei record shall produce one Vulnerability.

No Vulnerability deduplication shall occur.

---

## Rule V1

Create

```text
VULNERABILITY
```

---

## Rule V2

Assign

```text
vulnerability--UUID4
```

---

## Rule V3

Populate descriptors.

| Descriptor | Source |
|------------|--------|
| name | info.name |
| description | info.description |
| impact | info.impact |
| remediation | info.remediation |
| severity | info.severity |
| vendor | info.metadata.vendor |
| product | info.metadata.product |
| tags | info.tags |
| cve | classification.cve-id |
| cwe | classification.cwe-id |
| cpe | classification.cpe |
| cvss_metrics | classification.cvss-metrics |
| cvss_score | classification.cvss-score |
| epss_score | classification.epss-score |
| epss_percentile | classification.epss-percentile |

---

## Rule V4

Ignore null descriptors.

---

# 14. Finding Creation

Every processed record shall generate exactly one Finding.

Findings are never merged.

---

## Rule F1

Create

```text
FINDING
```

---

## Rule F2

Assign

```text
finding--UUID4
```

---

## Rule F3

Populate descriptors.

| Descriptor | Source |
|------------|--------|
| timestamp | timestamp |
| matched_at | matched-at |
| host | host |
| ip | ip |
| port | port |
| url | url |
| protocol | type |
| matcher_status | matcher-status |

---

# 15. Relationship Creation

The parser shall create the following relationships.

---

## Rule E1

```text
HOST

contains

SECURITY
```

---

## Rule E2

```text
SECURITY

contains

TEMPLATES_USED
```

---

## Rule E3

```text
SECURITY

contains

FINDINGS
```

---

## Rule E4

```text
FINDINGS

contains

Severity Category
```

---

## Rule E5

```text
Severity Category

contains

FINDING
```

---

## Rule E6

```text
FINDING

contains

VULNERABILITY
```

---

## Rule E7

```text
FINDING

based-on

TEMPLATE
```

---

## Rule E8

IF Service exists

Create

```text
SERVICE

affected-by

VULNERABILITY
```

---

## Rule E9

IF Application exists for Service

Create

```text
APPLICATION

affected-by

VULNERABILITY
```

---

## Rule E10

Always create

```text
HOST

affected-by

VULNERABILITY
```

---

# 16. Descriptor Rules

Every descriptor follows identical logic.

```text
IF value exists

AND value != null

AND value != ""

THEN

Create Descriptor

ELSE

Ignore
```

---

# 17. Array Rules

Arrays shall become descriptor arrays.

Examples

```text
author[]

↓

author descriptor
```

```text
tags[]

↓

tags descriptor
```

Do not create child entities.

---

# 18. Ignore Rules

The following fields shall be ignored.

| JSON Field | Reason |
|------------|--------|
| schema | Parser metadata |
| tool | Parser metadata |
| scenario | Test metadata |
| scenario_id | Test metadata |
| command | Runtime only |
| runtime | Runtime only |
| started_at | Runtime only |
| duration_s | Runtime only |
| exit_code | Runtime only |
| finding_summary_lines | Derived |
| text_role | Documentation |
| structured_role | Documentation |
| max-request | Runtime tuning |
| shodan-query | Search metadata |

---

# 19. Validation Rules

## VLD1

Exactly one Finding shall be created for every record.

---

## VLD2

Exactly one Vulnerability shall be created for every Finding.

---

## VLD3

Exactly one Template relationship shall exist for every Finding.

---

## VLD4

Every Finding shall belong to exactly one Severity Category.

---

## VLD5

Every Severity Category shall belong to FINDINGS.

---

## VLD6

Every Template shall belong to TEMPLATES_USED.

---

## VLD7

Every SECURITY node shall belong to exactly one Host.

---

## VLD8

Every node referenced by an edge shall exist in `nodes[]`.

---

## VLD9

Duplicate edges shall not be emitted.

---

# 20. Graph Invariants

After transformation, the graph shall always satisfy the following structure.

```text
HOST
└── SECURITY
    ├── TEMPLATES_USED
    │   └── TEMPLATE
    └── FINDINGS
        ├── INFO
        ├── LOW
        ├── MEDIUM
        ├── HIGH
        └── CRITICAL
            └── FINDING
                ├── VULNERABILITY
                └── TEMPLATE (based-on)

HOST
    affected-by
        VULNERABILITY

SERVICE
    affected-by
        VULNERABILITY

APPLICATION
    affected-by
        VULNERABILITY
```

---

# 21. Determinism

Given identical input, the parser shall always produce:

- identical node types
- identical edge relationships
- identical hierarchy
- identical descriptor values

The only permitted non-deterministic values are generated UUIDs for FINDING and VULNERABILITY entities.