# GitHub Project — First Four Stages

Issues are created on both repos. Linking them to a **single user-level Project** requires one-time OAuth scope refresh (cannot be done non-interactively from the agent).

## 1. Refresh GitHub CLI scopes

In a terminal (interactive):

```powershell
gh auth refresh -h github.com -s project,read:project
```

Complete the browser/device login when prompted.

## 2. Create project and add all issues

```powershell
cd C:\projects\spiderfeet
python .seed/planning/add_issues_to_github_project.py
```

This creates (if missing) a user project titled **Spiderfeet — First Four Stages** under `@brettforbes` and adds every open issue from:

- `brettforbes/spiderfeet`
- `brettforbes/spiderfeet-widget`

Output: `.seed/planning/github_project.json` with the project URL.

## 3. Manual alternative (simplest UI)

1. Open https://github.com/users/brettforbes/projects/new
2. Name: **Spiderfeet — First Four Stages**
3. Add issues from both repos via **Add item** (or wait for script after step 1–2)

## 4. Board columns (VibeGov)

Suggested Status field values: `Backlog`, `Ready`, `In progress`, `In review`, `Done`, `Blocked`.

Issue **X-00-03** tracks completion of project linkage.
