"""Generate .docs/non_osint_modules.md from module metadata."""

from __future__ import annotations

import ast
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyse_modules import (  # noqa: E402
    MODULES_DIR,
    class_assignment,
    find_plugin_class,
    literal_value,
    method_return_list,
)

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "non_osint_modules.md"
QUARANTINE_OUTPUT_PATH = Path(__file__).resolve().parents[1] / "quarantine_modules.md"

CORE_NON_OSINT_MODULES = {"sfp__stor_db", "sfp__stor_stdout"}

CATEGORY_ORDER = [
    "Storage & Output",
    "DNS & Domain Intelligence",
    "Web Crawling & Scanning",
    "Content Analysis & Extraction",
    "Social & Identity",
    "Reputation",
    "Public Registries",
    "External Tool Wrappers",
]

MODULE_CATEGORY = {
    "sfp__stor_db": "Storage & Output",
    "sfp__stor_stdout": "Storage & Output",
    "sfp_dnsbrute": "DNS & Domain Intelligence",
    "sfp_dnscommonsrv": "DNS & Domain Intelligence",
    "sfp_dnsneighbor": "DNS & Domain Intelligence",
    "sfp_dnsraw": "DNS & Domain Intelligence",
    "sfp_dnsresolve": "DNS & Domain Intelligence",
    "sfp_dnszonexfer": "DNS & Domain Intelligence",
    "sfp_similar": "DNS & Domain Intelligence",
    "sfp_tldsearch": "DNS & Domain Intelligence",
    "sfp_subdomain_takeover": "DNS & Domain Intelligence",
    "sfp_whois": "DNS & Domain Intelligence",
    "sfp_spider": "Web Crawling & Scanning",
    "sfp_portscan_tcp": "Web Crawling & Scanning",
    "sfp_sslcert": "Web Crawling & Scanning",
    "sfp_intfiles": "Web Crawling & Scanning",
    "sfp_junkfiles": "Web Crawling & Scanning",
    "sfp_crossref": "Web Crawling & Scanning",
    "sfp_accounts": "Social & Identity",
    "sfp_social": "Social & Identity",
    "sfp_customfeed": "Reputation",
    "sfp_pgp": "Public Registries",
}

TOOL_MODULES = {m for m in MODULE_CATEGORY if m.startswith("sfp_tool_")}


def safe_events(class_node: ast.ClassDef, method_name: str) -> list[str]:
    try:
        return method_return_list(class_node, method_name) or []
    except ValueError:
        return []


def load_non_osint_modules() -> list[dict]:
    modules: list[dict] = []

    for path in sorted(MODULES_DIR.glob("sfp_*.py")):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            continue

        plugin_class = find_plugin_class(tree)
        if plugin_class is None:
            continue

        meta_node = class_assignment(plugin_class, "meta")
        if meta_node is None:
            continue

        try:
            meta = literal_value(meta_node)
        except ValueError:
            continue

        if not isinstance(meta, dict) or "dataSource" in meta:
            continue

        modules.append(
            {
                "module_id": path.stem,
                "name": meta.get("name", ""),
                "summary": meta.get("summary", ""),
                "flags": meta.get("flags", []),
                "use_cases": meta.get("useCases", []),
                "categories": meta.get("categories", []),
                "tool_details": meta.get("toolDetails"),
                "watched_events": safe_events(plugin_class, "watchedEvents"),
                "produced_events": safe_events(plugin_class, "producedEvents"),
            }
        )

    return modules


def category_for(module: dict) -> str:
    mid = module["module_id"]
    if mid in MODULE_CATEGORY:
        return MODULE_CATEGORY[mid]
    if mid.startswith("sfp_tool_"):
        return "External Tool Wrappers"
    cats = module.get("categories") or []
    if cats and cats[0] in ("DNS", "Public Registries"):
        if mid == "sfp_pgp":
            return "Public Registries"
        return "DNS & Domain Intelligence"
    if cats and cats[0] == "Crawling and Scanning":
        return "Web Crawling & Scanning"
    if cats and cats[0] == "Social Media":
        return "Social & Identity"
    if cats and cats[0] == "Reputation Systems":
        return "Reputation"
    return "Content Analysis & Extraction"


def fmt_list(items: list[str], limit: int = 6) -> str:
    if not items:
        return "—"
    if len(items) <= limit:
        return ", ".join(f"`{item}`" for item in items)
    shown = ", ".join(f"`{item}`" for item in items[:limit])
    return f"{shown}, … (+{len(items) - limit} more)"


def fmt_flags(flags: list[str]) -> str:
    if not flags:
        return "—"
    return ", ".join(f"`{flag}`" for flag in flags)


def fmt_use_cases(use_cases: list[str]) -> str:
    if not use_cases:
        return "—"
    return ", ".join(use_cases)


def how_it_works(module: dict) -> str:
    mid = module["module_id"]
    watched = module["watched_events"]
    produced = module["produced_events"]
    flags = module.get("flags") or []
    tool = module.get("tool_details")

    details = {
        "sfp__stor_db": (
            "Subscribes to every event type (`*`) emitted during a scan and persists them to the "
            "Spiderfeet SQLite database via `scanEventStore()`. Optional `maxstorage` truncates "
            "oversized event payloads before storage."
        ),
        "sfp__stor_stdout": (
            "Subscribes to all events and prints them to standard output. Intended for CLI-driven "
            "scans where results are consumed in the terminal rather than the web UI database."
        ),
        "sfp_accounts": (
            "Downloads the WhatsMyName site list (WebBreacher) and, for each username derived from "
            "emails, domains, or human names, probes hundreds of social and web platforms for "
            "matching profile URLs. Threaded HTTP checks with optional permutation and name filtering "
            "reduce false positives."
        ),
        "sfp_base64": (
            "Scans internal linked URLs for Base64-encoded path segments or parameters, decodes them, "
            "and emits the decoded content as `BASE64_DATA` for downstream extractors."
        ),
        "sfp_binstring": (
            "When binary file types are fetched via internal links, extracts printable ASCII strings "
            "and stores them as `RAW_FILE_META_DATA` for further pattern matching."
        ),
        "sfp_bitcoin": (
            "Regex-matches Bitcoin address patterns in scraped web page content and emits "
            "`BITCOIN_ADDRESS` entities."
        ),
        "sfp_company": (
            "Uses heuristics and pattern matching across web content, WHOIS records, and SSL "
            "certificate fields to identify organisation/company names tied to the target or affiliates."
        ),
        "sfp_cookie": (
            "Parses `Set-Cookie` and related headers from `WEBSERVER_HTTPHEADERS` events and emits "
            "individual `TARGET_WEB_COOKIE` records."
        ),
        "sfp_countryname": (
            "Normalises geographic hints from IBANs, phone numbers, WHOIS, geo data, and addresses "
            "into canonical `COUNTRY_NAME` entities."
        ),
        "sfp_creditcard": (
            "Searches darknet and leak-site content for credit-card-like number sequences (with Luhn "
            "validation where applicable). Marked `errorprone` because numeric false positives are common."
        ),
        "sfp_crossref": (
            "Fetches external URLs, similar domains, co-hosted sites, and darknet mentions, then "
            "checks whether page content links back to the target domain. Reciprocal links indicate "
            "an affiliate relationship and produce `AFFILIATE_INTERNET_NAME` / `AFFILIATE_WEB_CONTENT`."
        ),
        "sfp_customfeed": (
            "Downloads a user-supplied plain-text feed (one indicator per line: IP, netblock, ASN, or "
            "hostname) and matches discovered target entities against it, emitting malicious descriptor "
            "events when hits are found."
        ),
        "sfp_dnsbrute": (
            "Generates candidate hostnames from built-in and configured wordlists against the scan "
            "target domain, performs DNS lookups, and emits resolved names as `INTERNET_NAME`. Runs "
            "against the target directly rather than waiting for upstream events."
        ),
        "sfp_dnscommonsrv": (
            "Brute-forces common DNS SRV record names (e.g. `_sip._tcp`, `_xmpp-server._tcp`) under "
            "known domains and hostnames to discover service endpoints."
        ),
        "sfp_dnsneighbor": (
            "For each target IP, reverse-resolves adjacent addresses in the same /24 (or configured "
            "range) to find co-located hosts that may belong to the same organisation."
        ),
        "sfp_dnsraw": (
            "Issues direct DNS queries for MX, NS, TXT, SPF, and related record types against known "
            "hostnames and domains, producing structured `DNS_*` events plus raw record blobs."
        ),
        "sfp_dnsresolve": (
            "Central DNS resolution hub: forward- and reverse-resolves hostnames and IPs found across "
            "virtually all upstream content (web pages, WHOIS, certificates, banners, leak data). "
            "Enriches the graph with `IP_ADDRESS`, `INTERNET_NAME`, `DOMAIN_NAME`, and affiliate variants."
        ),
        "sfp_dnszonexfer": (
            "Attempts AXFR zone transfers against nameservers identified as `PROVIDER_DNS`. Successful "
            "transfers dump the full zone as `RAW_DNS_RECORDS` and individual hostnames."
        ),
        "sfp_email": (
            "Regex-extracts email addresses from web content, WHOIS, DNS TXT, certificates, banners, "
            "leak dumps, and other text-bearing events. Classifies generic vs. personal mailboxes."
        ),
        "sfp_errors": (
            "Pattern-matches common application and database error strings (SQL syntax errors, stack "
            "traces, etc.) in fetched web content to flag misconfiguration or information disclosure."
        ),
        "sfp_ethereum": (
            "Regex-matches Ethereum `0x` address patterns in scraped web pages and emits "
            "`ETHEREUM_ADDRESS` entities."
        ),
        "sfp_filemeta": (
            "Downloads interesting linked files and uses metadata libraries to extract author, software, "
            "EXIF, and other embedded properties into `RAW_FILE_META_DATA` and `SOFTWARE_USED`."
        ),
        "sfp_hashes": (
            "Identifies MD5, SHA-1, SHA-256, and other hash formats in text content from web pages, "
            "leaks, DNS records, and file metadata."
        ),
        "sfp_hosting": (
            "Compares resolved IP addresses against known cloud and hosting provider netblock lists "
            "(AWS, Azure, GCP, etc.) to tag `PROVIDER_HOSTING`."
        ),
        "sfp_iban": (
            "Extracts International Bank Account Numbers from web and leak content with format validation."
        ),
        "sfp_intfiles": (
            "Flags internal linked URLs whose extensions or paths suggest downloadable documents "
            "(PDF, Office, archives) as `INTERESTING_FILE` for metadata or content analysis."
        ),
        "sfp_junkfiles": (
            "Probes common backup, temporary, and editor-artifact paths (`index.bak`, `.git`, `~`, etc.) "
            "on internal URLs. Invasive and slow; may generate false positives on hardened sites."
        ),
        "sfp_names": (
            "Uses name wordlists and NLP-style heuristics to pull probable human names from web content, "
            "WHOIS, and document metadata. Marked `errorprone` due to ambiguous capitalised tokens."
        ),
        "sfp_pageinfo": (
            "Analyses HTML structure of target pages to detect forms, password fields, file uploads, "
            "JavaScript usage, Flash, Java applets, and static vs. dynamic content—emitting URL descriptor "
            "events used heavily by reporting and risk scoring."
        ),
        "sfp_pgp": (
            "Queries public PGP keyserver pools (SKS/HKP) for keys matching target domains and email "
            "addresses, returning key material and any additional email identities found."
        ),
        "sfp_phone": (
            "Extracts phone numbers from web content and WHOIS using international format heuristics; "
            "may infer telecom provider metadata."
        ),
        "sfp_portscan_tcp": (
            "Connects to a configurable list of common TCP ports on target IPs and netblocks, recording "
            "open ports and banner text. Directly contacts the target (`invasive`)."
        ),
        "sfp_similar": (
            "Generates typo, homoglyph, and permutation variants of the target domain locally, resolves "
            "them via DNS, and emits registered lookalikes as `SIMILARDOMAIN` for squatting analysis."
        ),
        "sfp_social": (
            "Parses external linked URLs for known social-network URL patterns (LinkedIn, Twitter/X, "
            "Facebook, etc.) and emits `SOCIAL_MEDIA` plus extracted usernames."
        ),
        "sfp_spider": (
            "Breadth-first crawler starting from target hostnames and internal links. Fetches pages "
            "(respecting optional robots.txt), extracts links, HTTP headers, status codes, and page "
            "bodies—feeding the entire content-analysis pipeline."
        ),
        "sfp_sslcert": (
            "Opens TLS connections to target hosts, retrieves certificate chains, checks expiry and "
            "hostname mismatch, and identifies co-hosted sites via certificate SAN entries."
        ),
        "sfp_strangeheaders": (
            "Compares HTTP response headers against a catalogue of standard headers; non-standard or "
            "unusual names/values are emitted as `WEBSERVER_STRANGEHEADER`."
        ),
        "sfp_subdomain_takeover": (
            "Tests unresolved affiliate hostnames for dangling CNAME records pointing to deprovisioned "
            "third-party services (GitHub Pages, S3, Heroku, etc.) that could be claimed by an attacker."
        ),
        "sfp_tldsearch": (
            "Strips the TLD from a hostname and attempts DNS resolution of the same label under every "
            "ICANN TLD. Extremely thorough but very slow; surfaces international domain variants."
        ),
        "sfp_webanalytics": (
            "Regex-extracts Google Analytics, Matomo, and similar tracking IDs from page HTML and "
            "DNS TXT records."
        ),
        "sfp_webframework": (
            "Detects references to known JavaScript/CSS web frameworks (jQuery, YUI, Bootstrap, etc.) "
            "in page source."
        ),
        "sfp_webserver": (
            "Parses the `Server` header and related fields from HTTP responses to identify web server "
            "software and version banners."
        ),
        "sfp_whois": (
            "Performs WHOIS/RDAP lookups on target domains, parent domains, netblocks, co-hosted domains, "
            "affiliate domains, and similar domains—emitting raw WHOIS text for downstream extractors."
        ),
    }

    if mid in details:
        return details[mid]

    if tool:
        tool_name = tool.get("name", mid)
        return (
            f"Wraps the external **{tool_name}** CLI tool. When triggered by "
            f"{fmt_list(watched, 4)} events, executes the tool against the target, parses stdout/stderr, "
            f"and maps findings to {fmt_list(produced, 4)} events. Requires the tool binary to be "
            f"installed and available on the host running Spiderfeet."
        )

    return (
        f"Internal Spiderfeet module in the **{(module.get('categories') or ['General'])[0]}** category. "
        f"Listens for {fmt_list(watched, 4)} and produces {fmt_list(produced, 4)}."
    )


def when_used(module: dict) -> str:
    mid = module["module_id"]
    use_cases = module.get("use_cases") or []
    flags = module.get("flags") or []

    specifics = {
        "sfp__stor_db": (
            "Enable on **every scan** that uses the web UI or needs persistent results. Without it, "
            "events are lost after the scan completes."
        ),
        "sfp__stor_stdout": (
            "Use for **CLI-only** workflows (`sf.py -o tab`) where you want live event streaming without "
            "database storage."
        ),
        "sfp_dnsresolve": (
            "Enable whenever the scan needs hostname/IP enrichment—almost always required alongside "
            "spidering, WHOIS, or OSINT modules that emit unresolved names."
        ),
        "sfp_spider": (
            "Core module for **Footprint** and **Investigate** scans targeting websites. Required for "
            "most content extractors (email, pageinfo, bitcoin, etc.) to receive page bodies."
        ),
        "sfp_portscan_tcp": (
            "Use in **Investigate** or authorised penetration-test style scans. Avoid on passive-only "
            "assessments—it actively connects to target ports."
        ),
        "sfp_customfeed": (
            "Use when you have an internal threat-intel or blocklist feed to correlate against scan "
            "findings. Configure the feed URL in module options."
        ),
        "sfp_tldsearch": (
            "Optional deep **Footprint** module for brand-protection; expect long runtimes. Disable unless "
            "international lookalike domains are in scope."
        ),
        "sfp_junkfiles": (
            "Enable for security assessments hunting exposed backups and dev artifacts. Can be noisy; "
            "pair with conservative scope."
        ),
        "sfp_creditcard": (
            "Primarily for **Investigate** scans involving breach or leak data. High false-positive rate "
            "on unstructured text."
        ),
        "sfp_tool_nmap": (
            "Use when OS fingerprinting is needed beyond banner grabbing. Requires Nmap installed; "
            "generates invasive traffic."
        ),
        "sfp_tool_nuclei": (
            "Use for vulnerability validation passes after base footprinting. Requires Nuclei templates "
            "installed locally."
        ),
        "sfp_accounts": (
            "Enable for **Footprint** scans when you want to discover usernames and registered accounts "
            "from emails, domains, or names already found. Probes hundreds of third-party sites via the "
            "WhatsMyName list—network-active, though not a catalogued OSINT data source."
        ),
    }

    if mid in specifics:
        return specifics[mid]

    if "Passive" in use_cases and "Investigate" not in use_cases and "invasive" not in flags:
        return (
            f"Suitable for **passive** scans: processes data already collected by other modules without "
            f"contacting new external APIs (beyond normal DNS/WHOIS where applicable)."
        )
    if "Footprint" in use_cases and "Investigate" in use_cases:
        return (
            "Use in both **Footprint** (mapping attack surface) and **Investigate** (deeper validation) "
            "scan profiles when the relevant upstream events are in scope."
        )
    if "Footprint" in use_cases:
        return "Typically enabled in **Footprint** scans to map the target's external presence."
    if "Investigate" in use_cases:
        return "Enable for **Investigate** scans where deeper validation or active probing is authorised."
    return "Enable when the listed input events are produced by other modules in your scan configuration."


def section_for(module: dict, *, quarantined: bool = False) -> str:
    mid = module["module_id"]
    name = module["name"]
    summary = module["summary"]
    cat = category_for(module)
    flags = module.get("flags") or []
    use_cases = module.get("use_cases") or []
    meta_cats = module.get("categories") or []
    tool = module.get("tool_details")

    lines = [
        f"#### `{mid}` — {name}",
        "",
        f"**Category:** {cat}  ",
        f"**Spiderfeet categories:** {', '.join(meta_cats) if meta_cats else '—'}  ",
        f"**Use cases:** {fmt_use_cases(use_cases)}  ",
        f"**Flags:** {fmt_flags(flags)}",
        "",
        f"**Summary:** {summary}",
        "",
        "**Listens for:** " + fmt_list(module["watched_events"], 8),
        "",
        "**Produces:** " + fmt_list(module["produced_events"], 8),
        "",
    ]

    if tool:
        lines.extend([
            f"**Tool:** [{tool.get('name', '')}]({tool.get('website', '')})",
            "",
        ])

    lines.extend([
        "**How it works:** " + how_it_works(module),
        "",
    ])

    if quarantined:
        lines.extend([
            "**Status:** Quarantined — module behaviour and reliability still to be verified.",
            "",
            "**When to use:** Do not enable by default. Review and test before adding to a scan profile.",
            "",
        ])
    else:
        lines.extend([
            "**When to use:** " + when_used(module),
            "",
        ])

    return "\n".join(lines)


def write_module_table(lines: list[str], modules: list[dict]) -> None:
    lines.extend([
        "",
        "| Module | Name | Category | Use Cases | Flags |",
        "|--------|------|----------|-----------|-------|",
    ])
    for m in modules:
        lines.append(
            f"| `{m['module_id']}` | {m['name']} | {m['_category']} | "
            f"{fmt_use_cases(m.get('use_cases') or [])} | {fmt_flags(m.get('flags') or [])} |"
        )


def write_module_reference(
    lines: list[str],
    modules: list[dict],
    *,
    quarantined: bool = False,
) -> None:
    lines.extend([
        "",
        "---",
        "",
        "## Module Reference",
        "",
    ])
    if quarantined:
        lines.extend([
            "Detailed notes for each quarantined module, grouped by provisional role. "
            "Functionality has not yet been validated.",
            "",
        ])
    else:
        lines.extend(["Detailed notes for each module.", ""])

    current_cat = None
    for m in modules:
        if m["_category"] != current_cat:
            current_cat = m["_category"]
            lines.extend([f"### {current_cat}", ""])
        lines.append(section_for(m, quarantined=quarantined))


def write_non_osint_doc(modules: list[dict]) -> None:
    lines = [
        "# Non-OSINT Spiderfeet Modules",
        "",
        "A reference guide to Spiderfeet modules that are **generic infrastructure**—not tied to "
        "any external OSINT data source and not specialised scan logic.",
        "",
        "These modules do not declare a `dataSource` in their metadata because they provide core "
        "platform behaviour (persisting or printing scan events). They are distinct from:",
        "",
        "- [OSINT service modules](analysis/osint_services.json) — query third-party APIs and feeds",
        "- [Quarantined modules](quarantine_modules.md) — lack `dataSource` but implement specialised "
        "scan logic; pending verification",
        "",
        f"**Total: {len(modules)} modules.**",
        "",
        "---",
        "",
        "## All Non-OSINT Modules",
    ]
    write_module_table(lines, modules)
    write_module_reference(lines, modules)
    lines.extend([
        "---",
        "",
        f"*Generated from Spiderfeet module metadata. Total: {len(modules)} core non-OSINT modules.*",
        "",
    ])
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({len(modules)} modules)")


def write_quarantine_doc(modules: list[dict]) -> None:
    counts = Counter(m["_category"] for m in modules)
    lines = [
        "# Quarantined Spiderfeet Modules",
        "",
        "Modules listed here **do not** declare an external `dataSource` in their metadata, but they "
        "are **not** generic non-OSINT infrastructure. Each implements specialised scan behaviour "
        "(DNS, crawling, content extraction, local tools, etc.) that still needs to be checked: "
        "whether it works, and exactly how it works in this codebase.",
        "",
        "Do **not** treat these as validated non-OSINT modules. They were moved here from an earlier "
        "classification that incorrectly grouped all `dataSource`-less modules together. Only "
        "[`sfp__stor_db` and `sfp__stor_stdout`](non_osint_modules.md) are confirmed generic modules.",
        "",
        f"**Total: {len(modules)} modules** pending review.",
        "",
        "---",
        "",
        "## Module Categories (provisional)",
        "",
        "| Category | Count | Role |",
        "|----------|------:|------|",
    ]
    role_blurbs = {
        "Storage & Output": "Persist or print scan events",
        "DNS & Domain Intelligence": "Resolve, brute-force, and register domain data",
        "Web Crawling & Scanning": "Fetch targets, crawl sites, active probes",
        "Content Analysis & Extraction": "Parse text and headers for entities",
        "Social & Identity": "Find accounts and social profiles",
        "Reputation": "Match findings against user-supplied feeds",
        "Public Registries": "Query open registries (PGP keyservers)",
        "External Tool Wrappers": "Invoke installed CLI security tools",
    }
    for cat in CATEGORY_ORDER:
        if counts[cat]:
            lines.append(f"| {cat} | {counts[cat]} | {role_blurbs[cat]} |")

    lines.extend([
        "",
        "---",
        "",
        "## All Quarantined Modules",
    ])
    write_module_table(lines, modules)
    write_module_reference(lines, modules, quarantined=True)
    lines.extend([
        "---",
        "",
        "*Generated from Spiderfeet module metadata. Quarantined = no `dataSource` in module `meta`, "
        f"specialised behaviour pending verification. Total: {len(modules)} modules.*",
        "",
    ])
    QUARANTINE_OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {QUARANTINE_OUTPUT_PATH} ({len(modules)} modules)")


def main() -> None:
    all_modules = load_non_osint_modules()
    for module in all_modules:
        module["_category"] = category_for(module)

    core_modules = sorted(
        [m for m in all_modules if m["module_id"] in CORE_NON_OSINT_MODULES],
        key=lambda m: m["module_id"],
    )
    quarantine_modules = sorted(
        [m for m in all_modules if m["module_id"] not in CORE_NON_OSINT_MODULES],
        key=lambda m: (CATEGORY_ORDER.index(m["_category"]), m["module_id"]),
    )

    write_non_osint_doc(core_modules)
    write_quarantine_doc(quarantine_modules)


if __name__ == "__main__":
    main()
