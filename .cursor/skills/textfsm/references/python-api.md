# TextFSM Python API

## Installation

```bash
pip install textfsm
```

Verify: `pip show textfsm`

## Core usage

```python
import textfsm

with open("template.textfsm") as f:
    fsm = textfsm.TextFSM(f)

rows = fsm.ParseText(raw_text)           # list[list]
dicts = fsm.ParseTextToDicts(raw_text)   # list[dict]
header = fsm.header                      # list[str]
```

## Class members

| Member | Purpose |
|--------|---------|
| `TextFSM(template)` | Parse template file-like object; calls `Reset()` |
| `.header` | Column names from `Value` definitions |
| `.ParseText(text, eof=True)` | Returns `list[list]` — one inner list per row |
| `.ParseTextToDicts(text, eof=True)` | Returns `list[dict]` |
| `.Reset()` | Clear results; return to `Start` |
| `str(fsm)` | Round-trip template representation |

**Note:** `ParseText()` returns rows only. Headers are in `fsm.header`, not the first row.

**`eof=False`:** Suppresses implicit EOF `Record` for partial/streamed input.

## Exceptions

| Exception | When |
|-----------|------|
| `TextFSMTemplateError` | Invalid template syntax |
| `TextFSMError` | Runtime FSM error (including `-> Error` rule) |
| `SkipRecord` | Internal; `Required` values missing at record time |

## Validation CLI

```bash
python -m textfsm.parser template.textfsm input.txt [expected_output.txt]
```

Prints parsed template then table with `fsm.header` as columns.

## Manual dict conversion

```python
rows = fsm.ParseText(raw_text)
records = [dict(zip(fsm.header, row)) for row in rows]
```

## Export helpers

```python
import csv, json

rows = fsm.ParseText(raw_text)
with open("out.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(fsm.header)
    w.writerows(rows)

json.dumps([dict(zip(fsm.header, r)) for r in rows])
```

`List` option columns are Python `list` objects inside each row.
