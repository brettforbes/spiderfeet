# TypeBridge Patterns and Pitfalls

## High-Value Patterns

- **Generator-first**
  - Generate from `.tql` to reduce schema drift and boilerplate.
- **Attribute-first modeling**
  - Treat attributes as reusable types; entities/relations own them.
- **Identity-first CRUD**
  - Use `Flag(Key)` for entities used in update/delete and relation role matching.
- **Transaction sharing**
  - Reuse a single write transaction across managers for atomic workflows.
- **Polymorphic relation handling**
  - Use abstract role types where needed; branch on concrete types after fetch.
- **Manager APIs over raw queries**
  - Use chainable `filter`, `order_by`, `limit`, `offset`, `count`, `first`.

## Pitfalls to Avoid

- **Optional without default**
  - Wrong: `age: Age | None`
  - Correct: `age: Age | None = None`
- **Positional construction**
  - Wrong: `Person(Name("Alice"))`
  - Correct: `Person(name=Name("Alice"))`
- **Ordered-list assumption**
  - `list[T]` maps to unordered set semantics in TypeDB.
- **Missing card on list**
  - `list[T]` should use `Flag(Card(...))`.
- **Abstract instantiation**
  - Abstract types are for hierarchy/querying, not direct instances.
- **Unsafe updates/deletes**
  - Ensure key strategy or unique matching path exists.
- **Skipping schema sync**
  - Model edits without schema updates cause runtime mismatch issues.

## Quick Decision Matrix

- **Need fastest delivery from existing schema?** -> Use generator.
- **Need custom API payloads?** -> Use DTO generation with `DTOConfig`.
- **Need database functions (`fun`)?** -> Use generated wrappers / `FunctionQuery`.
- **Need deep diagnostics?** -> Enable targeted logging namespaces.
- **Need custom business constraints?** -> Add Pydantic validators.
