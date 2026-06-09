"""
Parse SpiderFeet modules and extract OSINT Service metadata.

Modules whose meta dict includes a dataSource field are external OSINT services.
Results are written to osint_services.json.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "modules"
OUTPUT_FILE = Path(__file__).resolve().parent / "osint_services.json"

# SpiderFeet dataSource.model → canonical access tier (see test_modules.py valid_models)
ACCESS_TIER_BY_MODEL: dict[str, str] = {
    "FREE_NOAUTH_UNLIMITED": "free_no_auth",
    "FREE_NOAUTH_LIMITED": "free_no_auth",
    "FREE_AUTH_LIMITED": "free_auth",
    "FREE_AUTH_UNLIMITED": "free_auth",
    "COMMERCIAL_ONLY": "paid",
    "PRIVATE_ONLY": "paid",
    "LOCAL_NOAUTH": "free_no_auth",
}

QUARANTINE_OVERRIDES_FILE = Path(__file__).resolve().parent / "quarantine_catalogue_overrides.json"
CORE_NON_OSINT_MODULE_IDS = frozenset({"sfp__stor_db", "sfp__stor_stdout"})

CONSUMPTION_GROUPS = frozenset({
    "domain",
    "hostname",
    "domain_and_hostname",
    "ip_netblock",
    "ip_only",
    "email",
    "email_identity_bundle",
    "phone",
    "crypto",
    "web_url_content",
    "org_entity",
    "other",
})

DOMAIN_NUGGETS = frozenset({
    "DOMAIN_NAME",
    "AFFILIATE_DOMAIN_NAME",
    "DOMAIN_WHOIS",
    "SIMILARDOMAIN",
    "SIMILARDOMAIN_WHOIS",
    "DOMAIN_NAME_PARENT",
    "AFFILIATE_DOMAIN_UNREGISTERED",
})

HOSTNAME_NUGGETS = frozenset({
    "INTERNET_NAME",
    "AFFILIATE_INTERNET_NAME",
    "CO_HOSTED_SITE",
    "CO_HOSTED_SITE_DOMAIN",
    "CO_HOSTED_SITE_DOMAIN_WHOIS",
    "INTERNET_NAME_UNRESOLVED",
    "AFFILIATE_INTERNET_NAME_UNRESOLVED",
    "AFFILIATE_INTERNET_NAME_HIJACKABLE",
})

IP_NUGGETS = frozenset({
    "IP_ADDRESS",
    "IPV6_ADDRESS",
    "AFFILIATE_IPADDR",
    "AFFILIATE_IPV6_ADDRESS",
    "INTERNAL_IP_ADDRESS",
})

NETBLOCK_NUGGETS = frozenset({
    "NETBLOCK_MEMBER",
    "NETBLOCK_OWNER",
    "NETBLOCKV6_MEMBER",
    "NETBLOCKV6_OWNER",
    "NETBLOCK_WHOIS",
})

EMAIL_NUGGETS = frozenset({
    "EMAILADDR",
    "AFFILIATE_EMAILADDR",
})

WEB_NUGGETS = frozenset({
    "LINKED_URL_INTERNAL",
    "LINKED_URL_EXTERNAL",
    "TARGET_WEB_CONTENT",
    "TARGET_WEB_CONTENT_TYPE",
    "TARGET_WEB_COOKIE",
    "URL_FORM",
    "URL_JAVASCRIPT",
    "URL_STATIC",
    "URL_FLASH",
    "URL_JAVA_APPLET",
    "URL_UPLOAD",
    "URL_PASSWORD",
    "URL_WEB_FRAMEWORK",
    "URL_FORM_HISTORIC",
    "URL_JAVASCRIPT_HISTORIC",
    "URL_STATIC_HISTORIC",
    "URL_FLASH_HISTORIC",
    "URL_JAVA_APPLET_HISTORIC",
    "URL_UPLOAD_HISTORIC",
    "URL_PASSWORD_HISTORIC",
    "URL_WEB_FRAMEWORK_HISTORIC",
    "SEARCH_ENGINE_WEB_CONTENT",
    "AFFILIATE_WEB_CONTENT",
    "PROVIDER_JAVASCRIPT",
})

ORG_NUGGETS = frozenset({
    "COMPANY_NAME",
    "AFFILIATE_COMPANY_NAME",
    "LEI",
})

CRYPTO_NUGGETS = frozenset({
    "BITCOIN_ADDRESS",
    "ETHEREUM_ADDRESS",
})

ROUTE_SEED_PRIORITY = [
    "ROOT",
    "INTERNET_NAME",
    "DOMAIN_NAME",
    "IP_ADDRESS",
    "IPV6_ADDRESS",
    "EMAILADDR",
    "PHONE_NUMBER",
    "BITCOIN_ADDRESS",
    "ETHEREUM_ADDRESS",
    "HUMAN_NAME",
    "USERNAME",
    "COMPANY_NAME",
    "LEI",
    "LINKED_URL_EXTERNAL",
    "LINKED_URL_INTERNAL",
    "WEB_ANALYTICS_ID",
    "SOCIAL_MEDIA",
    "INTERESTING_FILE",
    "PHYSICAL_ADDRESS",
    "PHYSICAL_COORDINATES",
]


def access_tier(model: str | None) -> str:
    if not model:
        return "free_no_auth"
    tier = ACCESS_TIER_BY_MODEL.get(model)
    if tier is None:
        raise ValueError(f"Unknown data_source.model: {model!r}")
    return tier


def route_seed_nugget(consumed: list[str]) -> str:
    consumed_set = set(consumed)
    if not consumed_set:
        return "OTHER"
    for nugget in ROUTE_SEED_PRIORITY:
        if nugget in consumed_set:
            return nugget
    return sorted(consumed_set)[0]


def consumption_group(consumed: list[str]) -> str:
    """Assign one of 12 consumption groups using priority rules (most specific first)."""
    s = set(consumed)
    if not s:
        return "other"

    has_domain = bool(s & DOMAIN_NUGGETS)
    has_hostname = bool(s & HOSTNAME_NUGGETS)
    has_ip = bool(s & IP_NUGGETS)
    has_netblock = bool(s & NETBLOCK_NUGGETS)
    has_email = bool(s & EMAIL_NUGGETS)
    has_phone = "PHONE_NUMBER" in s
    has_crypto = bool(s & CRYPTO_NUGGETS)
    has_web = bool(s & WEB_NUGGETS)
    has_org = bool(s & ORG_NUGGETS)

    if has_crypto and not has_email and not has_netblock:
        return "crypto"

    if has_phone and not has_email and not has_ip and not has_netblock and not has_hostname:
        return "phone"

    if has_email and len(s) == 1:
        return "email"

    if has_email and len(s) > 1:
        return "email_identity_bundle"

    if has_ip and has_netblock:
        return "ip_netblock"

    if has_ip and not has_netblock and not has_domain and not has_hostname and not has_email:
        return "ip_only"

    if has_domain and has_hostname:
        return "domain_and_hostname"

    if has_domain and not has_hostname and not has_ip and not has_netblock:
        return "domain"

    if has_hostname and not has_domain and not has_ip and not has_netblock:
        return "hostname"

    if has_web and not has_ip and not has_netblock and not has_email:
        return "web_url_content"

    if has_org and not has_ip and not has_email and not has_hostname:
        return "org_entity"

    return "other"


def to_snake_case(name: str) -> str:
    """Convert a camelCase or PascalCase identifier to snake_case."""
    name = name.replace("-", "_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def snake_case_keys(value: Any) -> Any:
    """Recursively convert dict keys to snake_case."""
    if isinstance(value, dict):
        return {to_snake_case(key): snake_case_keys(item) for key, item in value.items()}
    if isinstance(value, list):
        return [snake_case_keys(item) for item in value]
    return value


def normalize_opt_value(value: Any) -> tuple[str, Any]:
    """Return (value_type, json_safe_value) for one module option default."""
    if isinstance(value, bool):
        return "boolean", value
    if isinstance(value, int):
        return "integer", value
    if isinstance(value, float):
        return "double", value
    if isinstance(value, str):
        return "string", value
    if isinstance(value, (list, tuple, set)):
        return "string", json.dumps(list(value), ensure_ascii=False)
    return "string", json.dumps(value, ensure_ascii=False)


def merge_module_opts(
    opts: dict[str, Any] | None,
    optdescs: dict[str, str] | None,
) -> list[dict[str, Any]]:
    """Merge opts defaults and optdescs into a normalized list for JSON and TypeDB."""
    opts = opts or {}
    optdescs = optdescs or {}
    keys = sorted(set(opts) | set(optdescs))

    merged: list[dict[str, Any]] = []
    for key in keys:
        if key in opts:
            value_type, value = normalize_opt_value(opts[key])
        else:
            value_type, value = "string", None
        merged.append({
            "name": key,
            "value_type": value_type,
            "value": value,
            "description": optdescs.get(key, ""),
        })
    return merged


def service_icon_path(module_id: str) -> str:
    slug = module_id.replace("sfp_", "", 1) if module_id.startswith("sfp_") else module_id
    return f"icons/icon_service_{slug}.svg"


def local_data_source(module_id: str, meta: dict) -> dict[str, Any]:
    """Synthetic data_source for quarantine / local SpiderFeet modules (SPEC-003)."""
    summary = str(meta.get("summary") or meta.get("name") or module_id)
    website = f"spiderfeet://local/{module_id}"
    return {
        "website": website,
        "model": "LOCAL_NOAUTH",
        "references": [website],
        "fav_icon": service_icon_path(module_id),
        "description": summary,
    }


def build_service_record(
    module_id: str,
    meta: dict,
    watched_events: list[str],
    produced_events: list[str],
    module_opts: list[dict[str, Any]],
    *,
    data_source: dict[str, Any] | None = None,
    service_origin: str = "external",
) -> dict:
    """Flatten meta onto the service root and snake_case all field names."""
    raw = snake_case_keys({
        "module_id": module_id,
        **meta,
    })
    ds = data_source if data_source is not None else (raw.get("data_source") or {})
    model = ds.get("model")
    consumed = list(watched_events)
    produced = list(produced_events)

    return {
        "module_id": raw.get("module_id", module_id),
        "service_origin": service_origin,
        "name": raw.get("name"),
        "summary": raw.get("summary"),
        "flags": raw.get("flags", []),
        "use_cases": raw.get("use_cases", []),
        "categories": raw.get("categories", []),
        "data_source": ds,
        "access_tier": access_tier(model),
        "consumed_nuggets": consumed,
        "produced_nuggets": produced,
        "consumption_group": consumption_group(consumed),
        "route_seed_nugget": route_seed_nugget(consumed),
        "module_opts": module_opts,
        "fixture_category": "positive",
        "service_state": "in-test",
        **({"tool_details": raw["tool_details"]} if "tool_details" in raw else {}),
    }


def build_service(
    module_id: str,
    meta: dict,
    watched_events: list[str],
    produced_events: list[str],
    module_opts: list[dict[str, Any]],
) -> dict:
    rec = build_service_record(
        module_id,
        meta,
        watched_events,
        produced_events,
        module_opts,
        service_origin="external",
    )
    rec.pop("fixture_category", None)
    rec.pop("service_state", None)
    return rec


def literal_value(node: ast.AST | None):
    """Evaluate an AST node that contains only literals."""
    if node is None:
        return None
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [literal_value(item) for item in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(literal_value(item) for item in node.elts)
    if isinstance(node, ast.Dict):
        result = {}
        for key, value in zip(node.keys, node.values):
            if key is None:
                continue
            result[literal_value(key)] = literal_value(value)
        return result
    if isinstance(node, ast.Set):
        return {literal_value(item) for item in node.elts}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = literal_value(node.operand)
        if isinstance(value, (int, float)):
            return -value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = literal_value(node.left)
        right = literal_value(node.right)
        if isinstance(left, str) and isinstance(right, str):
            return left + right
    raise ValueError(f"Unsupported literal node: {ast.dump(node)}")


def find_plugin_class(tree: ast.Module) -> ast.ClassDef | None:
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            name = None
            if isinstance(base, ast.Name):
                name = base.id
            elif isinstance(base, ast.Attribute):
                name = base.attr
            if name == "SpiderFeetPlugin":
                return node
    return None


def class_assignment(class_node: ast.ClassDef, name: str) -> ast.AST | None:
    for node in class_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == name and node.value is not None:
                return node.value
    return None


def parse_class_dict(class_node: ast.ClassDef, name: str) -> dict | None:
    node = class_assignment(class_node, name)
    if node is None:
        return None
    try:
        value = literal_value(node)
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def method_return_list(class_node: ast.ClassDef, method_name: str) -> list[str] | None:
    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef) or node.name != method_name:
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.Return) and stmt.value is not None:
                if isinstance(stmt.value, ast.Name):
                    return _resolve_list_var(node, stmt.value.id)
                try:
                    value = literal_value(stmt.value)
                except ValueError:
                    return None
                if isinstance(value, list):
                    return [str(item) for item in value]
                return None
    return None


def _resolve_list_var(func_node: ast.FunctionDef, var_name: str) -> list[str] | None:
    """Best-effort: ret = [...]; ret.append('X'); return ret."""
    lists: dict[str, list[str]] = {}
    for stmt in func_node.body:
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and isinstance(stmt.value, ast.List):
                    try:
                        raw = literal_value(stmt.value)
                        if isinstance(raw, list):
                            lists[target.id] = [str(x) for x in raw]
                    except ValueError:
                        pass
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            call = stmt.value
            if (
                isinstance(call.func, ast.Attribute)
                and call.func.attr == "append"
                and isinstance(call.func.value, ast.Name)
                and call.args
            ):
                var = call.func.value.id
                if var in lists:
                    try:
                        item = literal_value(call.args[0])
                        if isinstance(item, str):
                            lists[var].append(item)
                    except ValueError:
                        pass
    return lists.get(var_name)


def load_quarantine_overrides() -> dict[str, dict[str, Any]]:
    if not QUARANTINE_OVERRIDES_FILE.is_file():
        return {}
    with QUARANTINE_OVERRIDES_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_module(path: Path) -> dict | None:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    plugin_class = find_plugin_class(tree)
    if plugin_class is None:
        return None

    meta_node = class_assignment(plugin_class, "meta")
    if meta_node is None:
        return None

    try:
        meta = literal_value(meta_node)
    except ValueError:
        return None

    if not isinstance(meta, dict) or "dataSource" not in meta:
        return None

    watched_events = method_return_list(plugin_class, "watchedEvents") or []
    produced_events = method_return_list(plugin_class, "producedEvents") or []
    opts = parse_class_dict(plugin_class, "opts") or {}
    optdescs = parse_class_dict(plugin_class, "optdescs") or {}
    module_opts = merge_module_opts(opts, optdescs)

    return build_service(path.stem, meta, watched_events, produced_events, module_opts)


def parse_quarantine_module(path: Path) -> dict | None:
    if path.stem in CORE_NON_OSINT_MODULE_IDS:
        return None

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    plugin_class = find_plugin_class(tree)
    if plugin_class is None:
        return None

    meta_node = class_assignment(plugin_class, "meta")
    if meta_node is None:
        return None

    try:
        meta = literal_value(meta_node)
    except ValueError:
        return None

    if not isinstance(meta, dict) or "dataSource" in meta:
        return None

    watched_events = method_return_list(plugin_class, "watchedEvents") or []
    produced_events = method_return_list(plugin_class, "producedEvents") or []
    overrides = load_quarantine_overrides().get(path.stem, {})
    if overrides.get("consumed_nuggets"):
        watched_events = list(overrides["consumed_nuggets"])
    if overrides.get("produced_nuggets"):
        produced_events = list(overrides["produced_nuggets"])

    opts = parse_class_dict(plugin_class, "opts") or {}
    optdescs = parse_class_dict(plugin_class, "optdescs") or {}
    module_opts = merge_module_opts(opts, optdescs)

    return build_service_record(
        path.stem,
        meta,
        watched_events,
        produced_events,
        module_opts,
        data_source=local_data_source(path.stem, meta),
        service_origin="quarantine",
    )


def analyse_quarantine_modules() -> list[dict]:
    services: list[dict] = []
    for path in sorted(MODULES_DIR.glob("sfp_*.py")):
        try:
            service = parse_quarantine_module(path)
        except SyntaxError:
            continue
        if service is None:
            continue
        services.append(service)
    services.sort(key=lambda item: item["module_id"])
    return services


def analyse_modules() -> list[dict]:
    services: list[dict] = []
    skipped: list[str] = []

    for path in sorted(MODULES_DIR.glob("sfp_*.py")):
        try:
            service = parse_module(path)
        except SyntaxError as exc:
            skipped.append(f"{path.name}: syntax error ({exc})")
            continue

        if service is None:
            continue
        services.append(service)

    services.sort(key=lambda item: item["module_id"])
    return services


def _print_summary(label: str, services: list[dict]) -> None:
    tiers: dict[str, int] = {}
    origins: dict[str, int] = {}
    for service in services:
        tiers[service["access_tier"]] = tiers.get(service["access_tier"], 0) + 1
        origin = str(service.get("service_origin") or "external")
        origins[origin] = origins.get(origin, 0) + 1
    print(f"{label}: {len(services)} services")
    print(f"  access_tier: {dict(sorted(tiers.items()))}")
    print(f"  service_origin: {dict(sorted(origins.items()))}")


def main() -> None:
    import sys

    if "--quarantine-only" in sys.argv:
        services = analyse_quarantine_modules()
        out = Path(__file__).resolve().parent / "quarantine_services.json"
        out.write_text(json.dumps(services, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _print_summary(f"Wrote quarantine catalogue to {out}", services)
        return

    services = analyse_modules()
    OUTPUT_FILE.write_text(
        json.dumps(services, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _print_summary(f"Wrote external OSINT services to {OUTPUT_FILE}", services)


if __name__ == "__main__":
    main()
