# SPEC-010 — Canonical semantic-edge naming (R10-06)

**Issue:** AI0 [#1071](https://github.com/brettforbes/spiderfeet/issues/1071)  
**Consumers:** AL2 dual-form subgraph serializer, AI2/`contains_recursive` extensions, TypeDB load/serialize layer  
**Schema:** `.seed/spiderfeet_v2_semantic.tql` (`semantic_link` + subtypes)  
**Ontology graph contract:** `.seed/05_Onotology_for_Nuggets.md` §3 (graph JSON relation vocabulary)

This note is the **one** canonical mapping between proposed-graph JSON edge `type` strings and TypeQL relation types / roles. Loaders and serializers must not invent alternate spellings.

---

## 1. Bidirectional mapping (relation type)

| Direction | Graph JSON `edges[].type` | TypeQL relation type | Notes |
|-----------|---------------------------|----------------------|-------|
| JSON → TypeDB | `had` | `has_this` | `has` is TypeQL-reserved; ontology uses `had` in JSON/docs |
| JSON → TypeDB | `contains` | `contains_this` | Structural / ownership containment |
| JSON → TypeDB | `listens-to` | `listens_to_this` | Hyphen in JSON; underscore in TypeQL type name |
| TypeDB → JSON | `has_this` | `had` | Inverse of row 1 |
| TypeDB → JSON | `contains_this` | `contains` | Inverse of row 2 |
| TypeDB → JSON | `listens_to_this` | `listens-to` | Inverse of row 3 |

No other relation names are allowed in proposed graphs (`rule_engine.DEFAULT_ALLOWED_RELATIONS = {contains, had, listens-to}`). Do not invent `relates`, `detects`, `uses`, `produces`, `had-this`, `contains-this`, or `listens_on` as edge types in graph JSON.

---

## 2. Role mapping (seed §3.2 reconciliation)

Schema defines abstract `semantic_link` with roles **`source`** and **`target`** (not `container`/`contained`):

```typeql
relation semantic_link @abstract,
  relates source,
  relates target,
  plays subgraph:edges;

relation has_this, sub semantic_link;
relation contains_this, sub semantic_link;
relation listens_to_this, sub semantic_link;
```

Seed prompt `.seed/17_…` §3.2 shows an illustrative `contains_recursive` using roles `container` / `contained`. That example is **non-canonical** relative to the checked-in schema. Canonical role semantics:

| Graph JSON edge | JSON `from` / `source` id | JSON `to` / `target` id | TypeQL `links` |
|-----------------|---------------------------|-------------------------|----------------|
| `had` | entity / category owning the descriptor | descriptor nugget | `(source: <owner>, target: <descriptor>)` |
| `contains` | parent entity / category / scan | child entity / category | `(source: <parent>, target: <child>)` |
| `listens-to` | service / application / host | open port | `(source: <listener>, target: <port>)` |

**Rule of thumb:** graph-JSON edge direction is always `source → target` in the same sense as TypeQL `semantic_link` roles. The obsolete seed names map as:

| Seed §3.2 example role | Canonical schema role |
|------------------------|------------------------|
| `container` | `source` |
| `contained` | `target` |

Implementations of `contains_recursive` (and any walk that follows `had` / `listens-to`) must use `source` / `target` on `*_this` relations. See existing schema comment at `.seed/spiderfeet_v2_semantic.tql` (~lines 827–830) and the live `contains_recursive` body (uses `contains_this` + `source`/`target`).

---

## 3. Serialization contract (for AL2)

When persisting a proposed graph into TypeDB entity/relation form:

1. Map each edge `type` via the table in §1 (fail closed on unknown types).
2. Insert `$_ isa <typeql_relation>, links (source: $from, target: $to);` where `$from`/`$to` are the nugget entities for the edge endpoints.
3. When projecting TypeDB edges back to graph JSON, emit `type` from the inverse column and preserve endpoint order as `from=source`, `to=target`.

Dual-form storage (`json-string` attribute + entity/relation form) must keep both forms consistent with this mapping; the JSON form remains the UI/corpus vocabulary (`had` / `contains` / `listens-to`).

---

## 4. Doc / prose aliases (do not emit)

These appear in narrative prose or older seed wording and are **not** graph-JSON edge types:

| Prose / legacy wording | Canonical graph JSON | Canonical TypeQL |
|------------------------|----------------------|------------------|
| `has`, `had-this` | `had` | `has_this` |
| `contains-this` | `contains` | `contains_this` |
| `listens on`, `listens_to` | `listens-to` | `listens_to_this` |
| seed roles `container`/`contained` | n/a (use endpoints) | roles `source`/`target` |

---

## 5. Verification checklist

- [x] All three relations mapped both directions (§1).
- [x] Seed §3.2 `container`/`contained` reconciled to `source`/`target` (§2).
- [x] AL2 / load-serialize consumers pointed at this note (§3).
- Schema already documents the same TypeQL side: `.seed/spiderfeet_v2_semantic.tql` functions section comment.
