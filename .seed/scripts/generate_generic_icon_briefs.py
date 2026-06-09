#!/usr/bin/env python3
"""Build icon design briefs for services using placeholder/generic map icons."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
QUARANTINE_MD = REPO_ROOT / ".docs" / "quarantine_modules.md"
OUTPUT = REPO_ROOT / ".docs" / "analysis" / "generic_icon_design_briefs.md"
WIDGET_ICONS = REPO_ROOT / ".." / "spiderfeet-widget" / "src" / "assets" / "icons"
TEMPLATE_HASH_MARKER = 'fill="#F97316"'  # icon_software_used.svg accent

ICON_SPEC = """
## Technical specification (all icons)

| Property | Value |
|----------|-------|
| Format | SVG 1.1, standalone file |
| Canvas | `viewBox="0 0 50 50"` (square) |
| Display size | 40×40 px in map icon mode (scale cleanly) |
| Background | Rounded rect `rx="5"`; use service brand colour or category hue |
| Foreground | White or near-white (`#FFFFFF`) strokes/fills for contrast |
| Style | Flat vector, 2–2.5 px stroke at 50×50 scale; no raster embeds |
| File name | As listed per service (`icons/...`) |
| Export path | `spiderfeet-widget/src/assets/icons/<filename>` |
| Accessibility | Recognisable at 24×24; avoid text smaller than 4 px cap height |
"""


def is_generic_fav_icon(fav: str, widget_icons: Path) -> bool:
    if not fav:
        return True
    if "icon_software_used" in fav:
        return True
    if "icon_service_" in fav:
        name = fav.replace("icons/", "").split("/")[-1]
        path = widget_icons / name
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if TEMPLATE_HASH_MARKER in text and "node-icon" not in text:
                return True
        return True  # quarantine placeholder path
    return False


def category_for(module_id: str, row: dict) -> str:
    cats = row.get("categories") or []
    if cats:
        return str(cats[0])
    if module_id.startswith("sfp_tool_"):
        return "External Tool Wrapper"
    return "OSINT Service"


def story_for(row: dict) -> str:
    name = row.get("name") or row["module_id"]
    summary = row.get("summary") or ""
    origin = row.get("service_origin") or "external"
    ds = row.get("data_source") or {}
    model = ds.get("model") or ""
    if origin == "quarantine":
        if module_id := row.get("module_id"):
            if module_id.startswith("sfp_tool_"):
                tool = module_id.replace("sfp_tool_", "").replace("_", " ")
                return (
                    f"{name} wraps the `{tool}` CLI installed on the operator host. "
                    f"The icon should evoke a terminal/command badge plus the tool's security function. "
                    f"{summary}"
                )
            if model == "LOCAL_NOAUTH":
                return (
                    f"{name} runs entirely inside SpiderFeet (no external API). "
                    f"Icon should communicate local processing / parsing, not a cloud vendor logo. "
                    f"{summary}"
                )
    website = ds.get("website") or ""
    return (
        f"{name} is an external OSINT integration"
        f"{f' ({website})' if website.startswith('http') else ''}. "
        f"Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. "
        f"{summary}"
    )


def visual_metaphor(module_id: str, category: str) -> str:
    metaphors = {
        "DNS": "globe + magnifier on hostname letters, or stylised DNS record stack",
        "Search Engines": "magnifying glass over data grid",
        "Social Media": "connected nodes / profile silhouette",
        "Crawling and Scanning": "spider web or radar sweep",
        "External Tool Wrapper": "terminal window with wrench or shield overlay",
        "Reputation Systems": "shield with feed/list motif",
        "Passive DNS": "clock + DNS glyph",
        "Real World": "map pin or building",
    }
    for key, val in metaphors.items():
        if key.lower() in category.lower():
            return val
    if module_id.startswith("sfp_tool_"):
        return metaphors["External Tool Wrapper"]
    if "dns" in module_id:
        return metaphors["DNS"]
    return "abstract OSINT glyph distinct from the generic orange terminal placeholder"


def colour_hint(category: str, origin: str) -> str:
    if origin == "quarantine":
        return "#7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph"
    hints = {
        "DNS": "#0EA5E9 sky blue",
        "Social Media": "#EC4899 pink",
        "Search Engines": "#3B82F6 blue",
        "Real World": "#10B981 emerald",
    }
    for k, v in hints.items():
        if k.lower() in category.lower():
            return v
    return "#57534E stone (positive fixture) or provider brand primary"


def main() -> int:
    widget_icons = WIDGET_ICONS.resolve()
    rows = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    generic_rows = [
        r for r in rows
        if is_generic_fav_icon(str((r.get("data_source") or {}).get("fav_icon") or ""), widget_icons)
    ]
    generic_rows.sort(key=lambda r: r["module_id"])

    lines = [
        "# Generic / placeholder OSINT service icon briefs",
        "",
        f"Generated for **{len(generic_rows)}** services whose Maps icon is the shared "
        "`icon_software_used.svg` placeholder or a copied quarantine stub.",
        "",
        "Hand each section to a design agent to produce a unique SVG per service.",
        ICON_SPEC.strip(),
        "",
        "---",
        "",
    ]

    for row in generic_rows:
        mid = row["module_id"]
        ds = row.get("data_source") or {}
        fav = ds.get("fav_icon") or f"icons/icon_service_{mid.replace('sfp_','')}.svg"
        if not fav.startswith("icons/"):
            fav = f"icons/{Path(fav).name}"
        cat = category_for(mid, row)
        slug = fav.replace("icons/icon_service_", "").replace(".svg", "")
        lines.extend(
            [
                f"## {mid} — {row.get('name', mid)}",
                "",
                f"- **Output file:** `{fav}`",
                f"- **Category:** {cat}",
                f"- **Service origin:** {row.get('service_origin', 'external')}",
                f"- **Access tier:** {row.get('access_tier', 'unknown')}",
                "",
                "### Narrative / brand story",
                "",
                story_for(row),
                "",
                "### Visual direction",
                "",
                f"- **Metaphor:** {visual_metaphor(mid, cat)}",
                f"- **Primary colour:** {colour_hint(cat, row.get('service_origin', 'external'))}",
                "- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`",
                "- **Must:** read clearly at 40 px inside a white circular ring on the force graph",
                "",
                "### Consumes / produces (context)",
                "",
                f"- Consumed: {', '.join((row.get('consumed_nuggets') or [])[:6])}"
                f"{'…' if len(row.get('consumed_nuggets') or []) > 6 else ''}",
                f"- Produced: {', '.join((row.get('produced_nuggets') or [])[:6])}"
                f"{'…' if len(row.get('produced_nuggets') or []) > 6 else ''}",
                "",
                "---",
                "",
            ]
        )

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(generic_rows)} briefs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
