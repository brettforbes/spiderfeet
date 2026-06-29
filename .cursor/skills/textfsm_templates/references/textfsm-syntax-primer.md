# TextFSM Syntax Primer (NTC Context)

NTC Templates are **TextFSM** files. This skill assumes templates exist; for grammar depth use the sibling **`textfsm`** skill.

## Minimal template anatomy

```
Value Required IP (\d+\.\d+\.\d+\.\d+)
Value MAC (\S+)

Start
  ^IP\s+MAC
  ^${IP}\s+${MAC} -> Record
  ^. -> Next
```

## Value options (common)

| Option | Effect |
|--------|--------|
| `Required` | Row dropped if column empty |
| `Filldown` | Value persists across rows (hostname context) |
| `List` | Accumulate multiple matches into Python list |
| `Key` | Deduplication key for record |

## State actions

| Action | Effect |
|--------|--------|
| `-> Record` | Emit row, clear non-Filldown values |
| `-> Continue.Record` | Emit partial row, continue current line |
| `-> Next` | Skip line, stay in state |
| `-> Error` | Fail parse (becomes `ParsingException` via NTC) |

## Rules

- Match **start of line** with `^`.
- Order rules **specific → general**.
- Blank line inside `Value` section breaks template.

## Where to learn more

| Topic | Location |
|-------|----------|
| Full syntax | [`../../textfsm/references/template-syntax.md`](../../textfsm/references/template-syntax.md) |
| Pitfalls | [`../../textfsm/references/pitfalls-and-examples.md`](../../textfsm/references/pitfalls-and-examples.md) |
| Raw API | [`../../textfsm/references/python-api.md`](../../textfsm/references/python-api.md) |
| Authoring skill | [`../../textfsm/SKILL.md`](../../textfsm/SKILL.md) |

## Validate without NTC wrapper

```bash
python -m textfsm.parser my.template.textfsm fixture.txt
```

Use this while iterating before wiring `parse_output`.
