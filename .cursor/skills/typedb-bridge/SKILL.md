# TypeBridge Skill

Use this skill when implementing TypeDB-backed Python work with `type-bridge` (modeling, CRUD, query logic, schema sync, generation, DTOs, functions, validation, logging).

## Baseline

- Package: `type-bridge`
- Python: `>=3.13`
- TypeDB: `3.x`
- Prefer current docs + PyPI over marketplace metadata when details conflict.

## Skill Operating Rules

1. **Generator-first when schema exists**
   - If a `.tql` schema is present, generate models first, then refine manually only where needed.
2. **Manager-first data access**
   - Prefer `Entity.manager(...)` / `Relation.manager(...)` patterns before raw TypeQL.
3. **Schema safety**
   - Register all touched models and run schema sync/migration consciously after model edits.
4. **Concrete instances only**
   - Abstract types are for polymorphic modeling/querying, never direct instantiation.
5. **Do not assume ordering for multi-value attributes**
   - `list[T]` is syntactic convenience; TypeDB stores unordered sets.

## Default Implementation Flow

1. Verify versions and connection assumptions.
1. If schema exists, run:

```bash
python -m type_bridge.generator schema.tql -o ./models/
```

1. Validate model correctness (attributes/entities/relations/cardinality/flags/abstract inheritance).
1. Apply schema operations via `SchemaManager`.
1. Implement CRUD/query logic with managers and transaction context reuse.
1. Add validation/error-handling/logging hooks where useful.
1. If API layer is requested, generate DTOs (`--dto`) and configure with `DTOConfig`.
1. If schema functions are present, use generated wrappers / `FunctionQuery`.

## Canonical Modeling Requirements

### Attributes

- Treat attributes as independent reusable types.
- Use the correct primitive (`String`, `Integer`, `Double`, `Decimal`, `Boolean`, `Date`, `DateTime`, `DateTimeTZ`, `Duration`).
- Use `Decimal` for financial/exact values; `Double` for approximate/scientific.
- Use `AttributeFlags` (`name`, `case`) when schema naming must be stable.
- Use value constraints when needed:
  - `range_constraint` -> `@range`
  - `regex` -> `@regex`
  - `allowed_values` -> `@values`
  - `independent = True` -> `@independent`

### Entities

- Define with `TypeFlags` (`name`, `abstract`, `base`, `case`) where explicit control is needed.
- Optional single-value fields must be `Type | None = None`.
- Constructors are keyword-only.
- Use `Flag(Key)` for stable identity and update/delete matching.
- Use `to_dict()` / `from_dict()` for payload mapping, aliases, and relaxed parsing (`strict=False` only when appropriate).

### Relations and Roles

- Define roles with `Role("role-name", Type)`.
- Use `Role.multi(...)` for one role accepted by multiple entity types.
- Prefer role names that match field names.
- For abstract role player types, expect concrete instance resolution on fetch.
- Remember relation operations match role players by IID first, then key attributes fallback.

### Cardinality and Flags

- Required single: `field: T` -> `@card(1..1)`
- Optional single: `field: T | None = None` -> `@card(0..1)`
- Multi-value: `field: list[T] = Flag(Card(...))` (required for lists)
- Never use code that depends on multi-value order.
- Use `Flag(Key)` for primary identity; `Flag(Unique)` for secondary uniqueness.

### Abstract Types

- Mark abstract with `TypeFlags(abstract=True)`.
- Query abstract managers polymorphically (returns concrete subtypes).
- Instantiate only concrete subtypes.
- When dealing with inherited attributes in internals/custom logic, prefer `get_all_attributes()` semantics over owned-only assumptions.

## CRUD and Query Patterns

```python
mgr = Person.manager(db)
mgr.insert(person)
mgr.put(person)  # idempotent insert pattern
rows = mgr.filter(status__in=["active", "pending"], age__gte=21).order_by("-age").limit(50).execute()
mgr.update_many(updated_people)
mgr.delete_many(to_delete, strict=False)
```

- Use `first()` for single expected results.
- Use bulk methods (`insert_many`, `put_many`, `update_many`, `delete_many`) for throughput.
- For updates/deletes, ensure key strategy is valid.
- For relations, use role-player filters and role-player sort (`role__attr`) as needed.

## Transactions

Use shared transaction context for atomic multi-manager workflows:

```python
with db.transaction("write") as tx:
    Person.manager(tx).insert(alice)
    Company.manager(tx).insert(acme)
    Employment.manager(tx).insert(emp)
```

## DTO Generation (When API Needed)

- Generate with:

```bash
python -m type_bridge.generator schema.tql -o ./models/ --dto
```

- Use `DTOConfig` for:
  - excluded internal entities
  - custom union names
  - `iid` field rename
  - strict out models
  - base-class hierarchies
  - validators
  - composite DTOs / relation structure customization

## Functions (TypeDB `fun`)

- Prefer generated wrappers from schema.
- Use `FunctionQuery` for manual function-call query generation.
- For stream functions, include pagination (`limit`/`offset`) where appropriate.
- Remember `FunctionQuery` generates TypeQL; DB executes it.

## Validation and Logging

- Leverage Pydantic v2 validation on creation and assignment.
- Add `field_validator` for business rules.
- Handle `ValidationError` explicitly at boundaries.
- Configure logging by logger namespace (e.g., `type_bridge`, `type_bridge.crud`, `type_bridge.session`) when debugging.

## Common Failure Modes to Prevent

- Defining optional fields without explicit `= None`.
- Using positional constructor arguments.
- Treating list-valued attributes as ordered.
- Updating entities without usable key identity.
- Instantiating abstract types.
- Skipping schema sync after model evolution.
- Overusing raw TypeQL where manager/query APIs already cover the task.

## Companion References In This Skill Folder

- `references/implementation-checklist.md` - end-to-end execution checklist
- `references/patterns-and-pitfalls.md` - quick patterns, anti-patterns, and gotchas
- `references/sources.md` - canonical source URLs
