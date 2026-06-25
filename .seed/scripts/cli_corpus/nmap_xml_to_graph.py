#!/usr/bin/env python3
"""Derive V2 nugget graph proposals from Nmap -oX XML examination artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import NAMESPACE_DNS, uuid5

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAM_ROOT = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap"
NUGGET_ROOT = REPO_ROOT / ".docs/docs-for-cli-tools/nugget_structure"
NUGGETS_PATH = REPO_ROOT / ".docs/analysis/nuggets.json"
NUGGETS_EXTENSION_PATH = REPO_ROOT / ".docs/analysis/nuggets_extension.json"

ONTOLOGY_NAMESPACE = uuid5(NAMESPACE_DNS, "OS Threat, OS Intel Ontology")

DEFAULT_TYPE_COLOURS = {
    "ENTITY": "#3B82F6",
    "DESCRIPTOR": "#F59E0B",
    "DATA": "#14B8A6",
    "SUBENTITY": "#F97316",
    "INTERNAL": "#8B5CF6",
    "CATEGORY": "#14B8A6",
}

_SCENARIO_SUFFIXES = ("_xml", "_text", "_json", "_yaml", "_csv")


def scenario_key_from_id(scenario_id: str) -> str:
    for suffix in _SCENARIO_SUFFIXES:
        if scenario_id.endswith(suffix):
            return scenario_id[: -len(suffix)]
    return scenario_id


def _load_nugget_templates() -> Dict[str, Dict[str, Any]]:
    templates: Dict[str, Dict[str, Any]] = {}
    for path in (NUGGETS_PATH, NUGGETS_EXTENSION_PATH):
        if not path.is_file():
            continue
        for record in json.loads(path.read_text(encoding="utf-8")):
            nugget_id = record.get("nugget_id")
            if nugget_id:
                templates[nugget_id] = record
    return templates


NUGGET_TEMPLATES = _load_nugget_templates()


def instance_id(nugget_id: str, data: str) -> str:
    return f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, data)}"


def _fallback_template(nugget_id: str, nugget_type: str) -> Dict[str, Any]:
    return {
        "nugget_id": nugget_id,
        "nugget_description": nugget_id.replace("_", " ").title(),
        "nugget_type": nugget_type,
        "nugget_icon": "",
        "nugget_colour": DEFAULT_TYPE_COLOURS.get(nugget_type, DEFAULT_TYPE_COLOURS["ENTITY"]),
    }


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = []
        self._edge_set: set[Tuple[str, str, str]] = set()

    def add_node(
        self,
        nugget_id: str,
        data: str,
        nugget_type: str = "ENTITY",
    ) -> str:
        template = NUGGET_TEMPLATES.get(nugget_id) or _fallback_template(nugget_id, nugget_type)
        template_type = template.get("nugget_type") or nugget_type
        data_value = str(data)
        nid = instance_id(nugget_id, data_value)
        if nid not in self.nodes:
            self.nodes[nid] = {
                "id": nid,
                "nugget_instance_id": nid,
                "nugget_id": nugget_id,
                "nugget_description": template.get("nugget_description", nugget_id),
                "nugget_type": template_type,
                "nugget_event_type": nugget_id,
                "nugget_icon": template.get("nugget_icon", ""),
                "nugget_colour": template.get(
                    "nugget_colour",
                    DEFAULT_TYPE_COLOURS.get(template_type, DEFAULT_TYPE_COLOURS["ENTITY"]),
                ),
                "nugget_data": data_value,
                "nugget_source_data": data_value,
                "nugget_module": "nmap",
                "nugget_confidence": 100,
                # Backward-compatible display alias used by the current widget.
                "data": data_value,
            }
        return nid

    def add_edge(self, source: str, target: str, relation: str) -> None:
        key = (source, target, relation)
        if key in self._edge_set:
            return
        self._edge_set.add(key)
        self.edges.append({"source": source, "target": target, "relation": relation})

    def to_dict(self) -> Dict[str, Any]:
        return {"nodes": list(self.nodes.values()), "edges": self.edges}


def _host_key(addresses: List[Tuple[str, str]]) -> str:
    for addr, _ in addresses:
        if "." in addr:
            return addr
    return addresses[0][0] if addresses else "unknown-host"


def _parse_host_addresses(host_el: ET.Element) -> List[Tuple[str, str]]:
    return [
        (el.get("addr", ""), el.get("addrtype", ""))
        for el in host_el.findall("address")
        if el.get("addr")
    ]


def _add_descriptor(
    g: GraphBuilder,
    parent_id: str,
    nugget_id: str,
    data: str,
) -> None:
    desc_id = g.add_node(nugget_id, data, "DESCRIPTOR")
    g.add_edge(parent_id, desc_id, "had")


def _ensure_host(
    g: GraphBuilder,
    host_key: str,
    status_el: Optional[ET.Element] = None,
    hostnames: Optional[List[str]] = None,
) -> str:
    host_id = g.add_node("HOST", host_key, "ENTITY")

    if status_el is not None:
        state = status_el.get("state")
        if state:
            _add_descriptor(g, host_id, "HOST_STATUS", state)
        reason = status_el.get("reason")
        if reason:
            _add_descriptor(g, host_id, "HOST_STATUS_REASON", reason)

    networks_id = g.add_node("NETWORKS", f"networks:{host_key}", "CATEGORY")
    g.add_edge(host_id, networks_id, "contains")

    ip_id = g.add_node("IP_ADDRESS", host_key, "ENTITY")
    g.add_edge(networks_id, ip_id, "contains")

    for name in hostnames or []:
        if name:
            _add_descriptor(g, host_id, "INTERNET_NAME", name)

    return host_id


def _parse_ports(g: GraphBuilder, host_id: str, host_key: str, host_el: ET.Element) -> None:
    ports_el = host_el.find("ports")
    if ports_el is None:
        return

    apps_id = g.add_node("APPLICATIONS", f"applications:{host_key}", "CATEGORY")
    g.add_edge(host_id, apps_id, "contains")

    networks_id = instance_id("NETWORKS", f"networks:{host_key}")
    ip_id = instance_id("IP_ADDRESS", host_key)

    for port_el in ports_el.findall("port"):
        proto = port_el.get("protocol", "tcp")
        portid = port_el.get("portid", "")
        if not portid:
            continue

        transport_id = g.add_node("TRANSPORT", proto, "ENTITY")
        g.add_edge(ip_id, transport_id, "contains")

        port_data = f"{proto}/{portid}"
        port_node_id = g.add_node("PORT", port_data, "ENTITY")
        g.add_edge(transport_id, port_node_id, "contains")

        state_el = port_el.find("state")
        if state_el is not None:
            state = state_el.get("state")
            if state:
                _add_descriptor(g, port_node_id, "PORT_STATE", state)
            reason = state_el.get("reason")
            if reason:
                _add_descriptor(g, port_node_id, "PORT_STATE_REASON", reason)

        _add_descriptor(g, port_node_id, "PORT_PROTOCOL", proto)

        service_el = port_el.find("service")
        if service_el is None:
            continue

        svc_name = service_el.get("name") or "unknown"
        svc_data = f"{host_key}:{port_data}:{svc_name}"
        svc_id = g.add_node("SERVICE", svc_data, "ENTITY")
        g.add_edge(apps_id, svc_id, "contains")

        if state_el is not None and state_el.get("state") == "open":
            g.add_edge(svc_id, port_node_id, "listens-to")

        product = service_el.get("product")
        version = service_el.get("version")
        if product or version:
            version_str = " ".join(x for x in (product, version) if x)
            _add_descriptor(g, svc_id, "SOFTWARE_USED", version_str)

        extrainfo = service_el.get("extrainfo")
        if extrainfo:
            _add_descriptor(g, svc_id, "SERVICE_EXTRAINFO", extrainfo)

        for cpe_el in service_el.findall("cpe"):
            cpe_text = (cpe_el.text or "").strip()
            if cpe_text:
                cpe_id = g.add_node("CPE_URL", cpe_text, "ENTITY")
                g.add_edge(svc_id, cpe_id, "contains")


def _parse_os(g: GraphBuilder, host_id: str, host_key: str, host_el: ET.Element) -> None:
    os_el = host_el.find("os")
    if os_el is None:
        return

    env_id = g.add_node("ENVIRONMENT", f"environment:{host_key}", "CATEGORY")
    g.add_edge(host_id, env_id, "contains")

    best = None
    best_acc = -1
    for match in os_el.findall("osmatch"):
        try:
            acc = int(match.get("accuracy", "0"))
        except ValueError:
            acc = 0
        if acc > best_acc:
            best_acc = acc
            best = match

    if best is None:
        return

    os_name = best.get("name", "unknown")
    os_id = g.add_node("OPERATING_SYSTEM", os_name, "ENTITY")
    g.add_edge(env_id, os_id, "contains")
    if best_acc >= 0:
        _add_descriptor(g, os_id, "OS_MATCH_ACCURACY", str(best_acc))


def _parse_trace(
    g: GraphBuilder,
    scan_id: str,
    target_host_id: str,
    target_host_key: str,
    host_el: ET.Element,
) -> None:
    trace_el = host_el.find("trace")
    if trace_el is None:
        return

    proto = trace_el.get("proto", "unknown")
    trace_id = g.add_node("TRACE", f"{target_host_key}:{proto}", "ENTITY")
    g.add_edge(scan_id, trace_id, "contains")
    _add_descriptor(g, trace_id, "TRACE_PROTOCOL", proto)

    hops = trace_el.findall("hop")
    for order, hop in enumerate(hops, start=1):
        ipaddr = hop.get("ipaddr", "")
        if not ipaddr:
            continue

        hop_entity_id = g.add_node(
            "TRACE_HOP",
            f"{target_host_key}:{proto}:{order}:{ipaddr}",
            "ENTITY",
        )
        g.add_edge(trace_id, hop_entity_id, "contains")

        ttl = hop.get("ttl")
        if ttl:
            _add_descriptor(g, hop_entity_id, "HOP_TTL", ttl)
        rtt = hop.get("rtt")
        if rtt:
            _add_descriptor(g, hop_entity_id, "HOP_RTT", rtt)
        _add_descriptor(g, hop_entity_id, "HOP_ORDER", str(order))

        hop_hostnames: List[str] = []
        hop_host = hop.get("host")
        if hop_host:
            hop_hostnames.append(hop_host)

        if ipaddr == target_host_key:
            hop_host_id = target_host_id
        else:
            hop_host_id = _ensure_host(g, ipaddr, hostnames=hop_hostnames)

        g.add_edge(hop_entity_id, hop_host_id, "contains")


def nmap_xml_to_graph(xml_path: Path) -> Dict[str, Any]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    g = GraphBuilder()

    args = root.get("args", "")
    version = root.get("version", "")
    startstr = root.get("startstr", "")

    target_match = re.search(r"\s(?:-oX\s+-\s+)?(\S+)\s*$", args)
    scan_target = target_match.group(1) if target_match else "unknown"

    scan_data = f"nmap:{scan_target}:{startstr or args}"
    scan_id = g.add_node("SCAN_RECORD", scan_data, "ENTITY")

    _add_descriptor(g, scan_id, "SCAN_CLI", args)
    if version:
        _add_descriptor(g, scan_id, "SCAN_VERSION", version)
    if startstr:
        _add_descriptor(g, scan_id, "SCAN_START", startstr)
    _add_descriptor(g, scan_id, "SCAN_TARGET", scan_target)
    _add_descriptor(g, scan_id, "SCAN_TOOL", "nmap")

    finished = root.find("./runstats/finished")
    if finished is not None:
        summary = finished.get("summary")
        if summary:
            _add_descriptor(g, scan_id, "SCAN_SUMMARY", summary)
        elapsed = finished.get("elapsed")
        if elapsed:
            _add_descriptor(g, scan_id, "SCAN_ELAPSED", elapsed)

    for host_el in root.findall("host"):
        addresses = _parse_host_addresses(host_el)
        if not addresses:
            continue

        host_key = _host_key(addresses)
        status_el = host_el.find("status")

        hostnames = [
            hn.get("name", "")
            for hn in host_el.findall("./hostnames/hostname")
            if hn.get("name")
        ]

        host_id = _ensure_host(g, host_key, status_el, hostnames)
        g.add_edge(scan_id, host_id, "contains")

        _parse_ports(g, host_id, host_key, host_el)
        _parse_os(g, host_id, host_key, host_el)
        _parse_trace(g, scan_id, host_id, host_key, host_el)

    return g.to_dict()


def _legacy_xml_exams() -> List[Tuple[str, Path]]:
    rows: List[Tuple[str, Path]] = []
    for manifest_path in sorted(EXAM_ROOT.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("structured_kind") != "xml":
            continue
        scenario_id = manifest.get("scenario_id", "")
        key = scenario_key_from_id(scenario_id)
        exam_id = manifest_path.name.split("_", 1)[0]
        xml_path = EXAM_ROOT / f"{exam_id}_output_structured.xml"
        if xml_path.is_file():
            rows.append((key, xml_path))
    return rows


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml", type=Path, help="Single Nmap XML file")
    parser.add_argument(
        "--scenario-key",
        help="Scenario key for output filename (with --xml)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all legacy XML examination artifacts for nmap",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=NUGGET_ROOT,
        help="Output directory for proposed_nuggets_edges JSON",
    )
    args = parser.parse_args(argv)

    if args.all:
        pairs = _legacy_xml_exams()
    elif args.xml:
        if not args.scenario_key:
            print("--scenario-key required with --xml", file=sys.stderr)
            return 2
        pairs = [(args.scenario_key, args.xml)]
    else:
        parser.print_help()
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)

    for scenario_key, xml_path in pairs:
        graph = nmap_xml_to_graph(xml_path)
        out_path = args.out_dir / f"nmap_{scenario_key}_proposed_nuggets_edges.json"
        out_path.write_text(
            json.dumps(graph, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            f"{scenario_key}: {len(graph['nodes'])} nodes, "
            f"{len(graph['edges'])} edges -> {out_path.relative_to(REPO_ROOT)}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
