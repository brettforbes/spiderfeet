# TypeDB Studio queries — `spiderfeet-map`

Validated against the [TypeDB skill](../.cursor/skills/typedb/SKILL.md) (TypeDB 3.x: `match`, `links`, `or`, `reduce`, `sort` / `offset` / `limit`).

**Database:** `spiderfeet-map`  
**Transaction:** read  
**Naming:** entity/relation labels are kebab-case (`internet-name`, `sfp-virustotal`); `module_id` values stay snake_case (`sfp_virustotal`).  
**Lists in JSON:** `flags`, `consumed_nuggets`, `produced_nuggets`, etc. are stored as **JSON strings** (one attribute each). Graph edges use **`links (consumed: …)` / `links (produced: …)`**.

**Instance typing:** use **`isa`** with `has` / `links` on the same constraint line. Do **not** use `$x sub type, has …` on instances (parse error). Do **not** use `$x sub osint-service` for instances (`sub` binds a type, not a service relation).

Run each query as a single script. **Every query must end with `;`** — including the final `reduce`, `limit`, or `fetch` line. Without it, Studio reports `expected GROUPBY` at `count` (misleading parse error).

Example (note the semicolon on the last line):

```typeql
match
  $n isa nugget;
reduce $nugget_count = count;
```

TypeDB Studio graphs only **`match`** without **`fetch`** (or **`insert`**). Use the match-only blocks below and open the **Graph** tab.

---

## 0. Prerequisites — run this first

If link queries return **0 rows** while nugget counts work, the map database has no persisted OSINT services or edges. Re-seed:

```powershell
cd c:\projects\spiderfeet
poetry run python -m spiderfeet.map --reset
poetry run python -m spiderfeet.map
```

Confirm in Studio (table view is fine):

```typeql
match
  $n isa nugget;
reduce $nugget_count = count;
```

```typeql
match
  $osint isa osint-service;
reduce $service_count = count;
```

```typeql
match
  $osint isa osint-service,
    links (consumed: $nug);
  $nug isa nugget;
reduce $probe_consumed = count;
```

Expected after a good bootstrap: **172** nuggets, **177** services, **probe_consumed > 0**. If services are **0**, stop — fix bootstrap before using §4–§6.

---

## 1. Quick inventory (counts — not graphable)

```typeql
match
  $n isa nugget;
reduce $nugget_count = count;
```

```typeql
match
  $osint isa osint-service;
reduce $service_count = count;
```

```typeql
match
  $osint isa osint-service;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
  $nug isa nugget;
reduce $link_count = count;
```

Expected: **172** nuggets, **177** services, **~1445** links.

---

## 2. All archetype nuggets (nodes)

```typeql
match
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_instance_id $iid,
    has nugget_description $desc,
    has nugget_type $ntype,
    has nugget_colour $colour;
```

Paged:

```typeql
match
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_description $desc;
sort $nid asc;
offset 0;
limit 50;
```

---

## 3. All OSINT service relations (nodes)

```typeql
match
  $osint isa osint-service,
    has module_id $mid,
    has name $name,
    has summary $summary,
    has service_state $state;
```

Paged:

```typeql
match
  $osint isa osint-service,
    has module_id $mid,
    has name $name;
sort $mid asc;
offset 0;
limit 25;
```

---

## 4. Map subgraphs (graph view)

**4a — sample edges (consumed + produced, whole map)**

```typeql
match
  $osint isa osint-service,
    has module_id $mid;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
  $nug isa nugget,
    has nugget_id $nid;
offset 0;
limit 100;
```

**4b — one service hub (replace `sfp_abstractapi`)**

```typeql
match
  $osint isa osint-service,
    has module_id "sfp_abstractapi",
    has name $sname;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_description $desc;
```

---

## 5. One service drill-down

Replace `sfp_abstractapi` with any `module_id` from §3.

**5a — service node + attributes**

```typeql
match
  $osint isa osint-service,
    has module_id "sfp_abstractapi",
    has name $name,
    has summary $summary,
    has service_state $state,
    has consumed_nuggets $consumed_json,
    has produced_nuggets $produced_json;
```

**5b — all linked nuggets (consumed + produced)**

```typeql
match
  $osint isa osint-service,
    has module_id "sfp_abstractapi",
    has name $sname;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_description $desc;
```

**5c — data-source** (if seeded)

```typeql
match
  $osint isa osint-service,
    has module_id "sfp_abstractapi";
  data-source (service: $osint, source: $src);
  $src isa osint-source,
    has website $web,
    has model $model;
```

**5d — module options** (if present)

```typeql
match
  $osint isa osint-service,
    has module_id "sfp_abstractapi";
  opts (service: $osint, opt: $opt);
  $opt isa module-opt,
    has opt_name $oname;
```

---

## 6. One nugget and its services

Example: `INTERNET_NAME` / `internet-name`.

**6a — nugget node**

```typeql
match
  $nug isa internet-name,
    has nugget_id "INTERNET_NAME",
    has nugget_instance_id $iid,
    has nugget_description $desc,
    has nugget_type $ntype,
    has nugget_colour $colour;
```

**6b — all services that consume or produce this nugget**

```typeql
match
  $nug isa internet-name,
    has nugget_id "INTERNET_NAME";
  $osint isa osint-service,
    has module_id $mid,
    has name $sname;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
```

---

## 7. Schema sanity

```typeql
match
  $t type nugget;
```

```typeql
match
  $t type osint-service;
```

---

## Troubleshooting

| Symptom | Cause / fix |
|--------|-------------|
| Parse error `expected GROUPBY` at `count` | Missing trailing **`;`** on the `reduce` line. Use `reduce $nugget_count = count;` not `… = count`. |
| **0 rows** on §4–§6, nuggets OK | Services/links never persisted. Run §0 bootstrap; expect 177 services. |
| Bootstrap `services_inserted: 177` but Studio shows 0 services | Old schema/bootstrap bug: relations without role players are deleted on commit. Use current `.seed/spiderfeet_map.tql` (`relates consumed/produced @card(0..)`) and `--reset`. |
| “Cannot be displayed as a graph” | Query uses `fetch` or `reduce`. Use match-only blocks above. |
| Parse error after `sub nugget` | Use `isa nugget` for instances. |
| Parse error reusing `$mod` after `$mod sub …` | Never use `sub` on instance variables; use `isa osint-service`. |

## Re-seed from CLI

```powershell
cd c:\projects\spiderfeet
poetry run python -m spiderfeet.map --reset
poetry run python -m spiderfeet.map
```

---

## Appendix: tabular `fetch` queries

Not graphable. Same `or` pattern for consumed + produced.

```typeql
match
  $osint isa osint-service,
    has module_id $mid;
  {
    $osint links (consumed: $nug);
  } or {
    $osint links (produced: $nug);
  };
  $nug isa nugget,
    has nugget_id $nid;
fetch {
  "module_id": $mid,
  "nugget_id": $nid
};
```
