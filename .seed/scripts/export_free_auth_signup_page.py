#!/usr/bin/env python3
"""Export free-tier API key signup reference from osint_services.json."""

from __future__ import annotations

import json
from pathlib import Path

from spiderfeet.map.service_states import include_in_operator_ui
from spiderfeet.map.signup_links import signup_metadata
from spiderfeet.map.subscriptions import subscription_tier_for_service

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / ".docs" / "analysis" / "osint_services.json"
OUT_MD = ROOT / ".docs" / "analysis" / "free_auth_api_key_signup.md"
OUT_HTML = ROOT / ".docs" / "analysis" / "free_auth_api_key_signup.html"
WIDGET_HTML = ROOT.parent / "spiderfeet-widget" / "src" / "assets" / "free_auth_api_key_signup.html"


def main() -> None:
    services = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = []
    for svc in services:
        if not include_in_operator_ui(svc):
            continue
        if subscription_tier_for_service(svc) != "free_auth":
            continue
        signup = signup_metadata(svc)
        ds = svc.get("data_source") or {}
        instructions = [str(x) for x in (ds.get("api_key_instructions") or [])]
        rows.append(
            {
                "module_id": svc["module_id"],
                "name": svc.get("name") or svc["module_id"],
                "model": str(ds.get("model") or ""),
                "signup": signup.get("signup_url") or "",
                "website": str(ds.get("website") or ""),
                "bucket": signup.get("signup_bucket") or "review",
                "note": signup.get("signup_note") or "",
                "instructions": instructions,
            }
        )
    rows.sort(key=lambda r: (r["bucket"], r["name"].lower()))

    self_serve = [r for r in rows if r["bucket"] == "self-serve"]
    review = [r for r in rows if r["bucket"] == "review"]
    manual = [r for r in rows if r["bucket"] == "manual"]
    paid_risk = [r for r in rows if r["bucket"] == "paid-risk"]

    md = [
        "# Free API key signup guide (SpiderFeet Stage 4)",
        "",
        "Modules that need a **free-tier API key** before tests can run (`free_auth` in the catalogue).",
        "Paid-tier modules (`paid_auth`, 10 modules) are listed in the Subscriptions tab with bucket `paid-risk`.",
        "",
        f"**Total free_auth modules:** {len(rows)}",
        f"- **Self-serve signup (start here):** {len(self_serve)}",
        f"- **Review on site:** {len(review)}",
        f"- **Manual / slow approval:** {len(manual)}",
        "",
        "Open the same table in the widget: **Subscriptions** tab → signup checklist.",
        "Static copy when the dev server is running: `http://localhost:4001/free_auth_api_key_signup.html`",
        "",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    html_rows = []
    for r in rows:
        link = r["signup"] or r["website"]
        badge = {
            "self-serve": "success",
            "review": "warning",
            "manual": "secondary",
            "paid-risk": "danger",
        }[r["bucket"]]
        html_rows.append(
            f"<tr data-bucket='{r['bucket']}'><td><span class='badge bg-{badge}'>{r['bucket']}</span></td>"
            f"<td><code>{r['module_id']}</code></td><td>{r['name']}</td>"
            f"<td><a href='{link}' target='_blank' rel='noopener'>Open signup</a></td>"
            f"<td class='small'>{r['note']}</td></tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SpiderFeet free API key signups</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="p-4">
  <h1 class="h3">Free API key signups ({len(rows)} modules)</h1>
  <p class="text-secondary">Self-serve: {len(self_serve)} · Review: {len(review)} · Manual: {len(manual)}</p>
  <p>Prefer the live checklist in the widget <strong>Subscriptions</strong> tab (keys + status).</p>
  <table class="table table-sm table-striped" id="signup-table">
    <thead><tr><th>Bucket</th><th>Module</th><th>Name</th><th>Link</th><th>Note</th></tr></thead>
    <tbody>
      {''.join(html_rows)}
    </tbody>
  </table>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    if WIDGET_HTML.parent.is_dir():
        WIDGET_HTML.write_text(html, encoding="utf-8")
        print(f"Wrote {WIDGET_HTML}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_HTML}")


if __name__ == "__main__":
    main()
