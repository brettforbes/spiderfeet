# TextFSM Template Syntax

Canonical reference: [google/textfsm wiki](https://github.com/google/textfsm/wiki/TextFSM)

## Template anatomy

```
Value [option[,option...]] name (regex)
Value name (regex)

Start
  ^rule [-> action]
  ^rule

AnotherState
  ^rule
```

Two sections, in order:

1. **Value definitions** — contiguous; blank line ends section
2. **State definitions** — separated by at least one blank line

Comments: lines matching `^\s*#`.

## Value definitions

```
Value [option[,option...]] name (regex)
```

| Option | Behavior |
|--------|----------|
| `Filldown` | Retain last matched value across rows until cleared or re-matched |
| `Fillup` | Like Filldown but fills empty prior rows; incompatible with `Required` |
| `Key` | Field contributes to row uniqueness |
| `Required` | Row discarded if this value empty at `Record` time |
| `List` | Each match appends (default overwrites) |

- `name` becomes column header (max 48 chars)
- `regex` must contain at least one **parenthesized capture group**
- Reference in rules: `$Name` or `${Name}` (preferred)
- Use `$$` in rules for explicit end-of-line

## State definitions

- First line: state name (alphanumeric)
- Rules: **1–2 spaces + `^` + regex** `[-> action]`
- Matching is line-anchored at start
- Rules evaluated top to bottom; first match wins
- **`Start` is mandatory**

### Reserved states

| State | Role |
|-------|------|
| `Start` | Required entry point |
| `End` | Terminates; skips implicit `EOF` |
| `EOF` | Implicit unless overridden; default `^.* -> Record` |

Suppress final EOF record:

```
EOF
```

## Rule actions

Format: `^regex -> [LineAction].[RecordAction] [NewState]`

Default: `Next.NoRecord`

### Line actions

| Action | Effect |
|--------|--------|
| `Next` | Consume line; read next; restart rules (default) |
| `Continue` | Try next rule on same line (values still assigned). **Cannot change state** |

### Record actions

| Action | Effect |
|--------|--------|
| `NoRecord` | Accumulate only (default) |
| `Record` | Save row; clear non-`Filldown` values |
| `Clear` | Clear non-`Filldown` values |
| `Clearall` | Clear all including `Filldown` |

### State transition

Optional new state name after actions switches FSM before next line.

### Error action

```
^regex -> Error [message|"string"]
```

Discards collected rows; raises `TextFSMError`.

## Value substitution

Rule `^Interface ${Interface} is up` with `Value Interface (\S+)` expands to `^Interface (\S+) is up`. Entire expanded regex must match for assignment.
