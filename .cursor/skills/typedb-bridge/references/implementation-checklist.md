# TypeBridge Implementation Checklist

Use this checklist while implementing TypeBridge tasks.

## 1) Environment and Scope

- Confirm `type-bridge`, Python, and TypeDB versions.
- Confirm whether a `.tql` schema already exists.
- Confirm whether the task includes API/DTO, functions, or only data modeling/CRUD.

## 2) Model Strategy

- If schema exists: generate models first.
- If no schema exists: model attributes/entities/relations directly.
- Define clear identity fields with `Flag(Key)` for entities used in updates/deletes.
- Keep optional single values as `Type | None = None`.
- Keep multi-values as `list[Type] = Flag(Card(...))`.
- Avoid relying on order of multi-value attributes.

## 3) Abstract and Inheritance Rules

- Use `TypeFlags(abstract=True)` for abstract bases.
- Do not instantiate abstract types directly.
- Expect polymorphic query behavior from abstract managers.
- For inherited-attribute logic, account for inherited + owned fields.

## 4) Schema Operations

- Register all touched models in `SchemaManager`.
- Run sync/migration intentionally after model changes.
- Review potential breaking changes before forcing schema updates.

## 5) CRUD and Query Implementation

- Use manager methods (`insert`, `put`, `filter`, `update`, `delete`) before raw TypeQL.
- Prefer bulk variants (`insert_many`, `put_many`, `update_many`, `delete_many`) for batches.
- Use chainable queries with explicit filters and `order_by`.
- For relations, verify role-player matching inputs (IID preferred, key fallback).

## 6) Transactions

- Group related writes in a shared write transaction.
- Reuse `tx` across managers for atomic workflows.

## 7) Optional API / DTO Layer

- If requested, generate DTOs with `--dto`.
- Configure `DTOConfig` for:
  - excluded entities
  - strict output
  - field/union naming
  - custom validators and composite DTO behavior

## 8) Optional Function Layer

- If schema functions exist, use generated function wrappers or `FunctionQuery`.
- Apply pagination for stream-returning functions.

## 9) Validation, Errors, and Logging

- Add `field_validator` for business constraints.
- Handle `ValidationError` at boundaries.
- Handle key CRUD exceptions (`KeyAttributeError`, not-found/not-unique cases).
- Turn on focused logging namespaces only as needed (`type_bridge.crud`, `type_bridge.session`, etc.).

## 10) Final Verification

- Validate representative create/read/update/delete flows.
- Verify relation queries and role-player behavior.
- Verify schema remains in sync with model definitions.
- Confirm no code assumes ordered list semantics for TypeDB multi-values.
