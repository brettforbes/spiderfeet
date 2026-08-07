#!/usr/bin/env python3
"""Template-driven narrative Markdown reports from semantic nugget graphs (Ontology §4.3)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple


Relation = str
Node = Dict[str, Any]
Edge = Dict[str, str]
Graph = Dict[str, Any]

SSH_KEY_NUGGETS = frozenset({"DSA", "RSA", "ECDSA", "EDDSA"})


def node_label(node: Node) -> str:
    return str(node.get("nugget_description") or node.get("nugget_id") or "nugget")


def node_value(node: Node) -> str:
    return str(node.get("nugget_data") or node.get("data") or "")


def descriptor_phrase(node: Node) -> str:
    return f"**{node_label(node)}** (`{node_value(node)}`)"


class SemanticGraph:
    """Index nodes and edges for ontology-aware narrative traversal."""

    def __init__(self, graph: Graph) -> None:
        self.nodes: Dict[str, Node] = {
            str(n["id"]): n for n in graph.get("nodes", []) if n.get("id")
        }
        self.out_edges: Dict[str, List[Tuple[Relation, str]]] = {}
        self.in_edges: Dict[str, List[Tuple[Relation, str]]] = {}
        for edge in graph.get("edges", []):
            source = edge.get("source", "")
            target = edge.get("target", "")
            relation = edge.get("relation", "")
            if not source or not target:
                continue
            self.out_edges.setdefault(source, []).append((relation, target))
            self.in_edges.setdefault(target, []).append((relation, source))

    def get(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def outgoing(
        self,
        node_id: str,
        relation: Optional[Relation] = None,
        nugget_id: Optional[str] = None,
    ) -> List[Node]:
        results: List[Node] = []
        for rel, target in self.out_edges.get(node_id, []):
            if relation and rel != relation:
                continue
            node = self.get(target)
            if not node:
                continue
            if nugget_id and node.get("nugget_id") != nugget_id:
                continue
            results.append(node)
        return self._sort_nodes(results)

    def incoming(
        self,
        node_id: str,
        relation: Optional[Relation] = None,
        nugget_id: Optional[str] = None,
    ) -> List[Node]:
        results: List[Node] = []
        for rel, source in self.in_edges.get(node_id, []):
            if relation and rel != relation:
                continue
            node = self.get(source)
            if not node:
                continue
            if nugget_id and node.get("nugget_id") != nugget_id:
                continue
            results.append(node)
        return self._sort_nodes(results)

    def descriptors(self, entity_id: str) -> List[Node]:
        return self.outgoing(entity_id, relation="had")

    def contained(self, entity_id: str, nugget_id: Optional[str] = None) -> List[Node]:
        return self.outgoing(entity_id, relation="contains", nugget_id=nugget_id)

    def contained_ip_addresses(self, entity_id: str) -> List[Node]:
        """Host/system address nodes: IPV4_ADDRESS and/or IPV6_ADDRESS (SPEC-010 AH)."""
        nodes: List[Node] = []
        for nugget_id in ("IPV4_ADDRESS", "IPV6_ADDRESS"):
            nodes.extend(self.contained(entity_id, nugget_id=nugget_id))
        return self._sort_nodes({n["id"]: n for n in nodes}.values())

    def find_by_nugget_id(self, nugget_id: str) -> List[Node]:
        return self._sort_nodes(
            [node for node in self.nodes.values() if node.get("nugget_id") == nugget_id]
        )

    def find_scan(self, scan_nugget_id: str = "SCAN_RECORD") -> Optional[Node]:
        scans = self.find_by_nugget_id(scan_nugget_id)
        return scans[0] if scans else None

    def find_trace(self, trace_nugget_id: str = "TRACE") -> Optional[Node]:
        traces = self.find_by_nugget_id(trace_nugget_id)
        return traces[0] if traces else None

    def scan_hosts(
        self,
        scan_nugget_id: str = "SCAN_RECORD",
        host_nugget_id: str = "HOST",
    ) -> List[Node]:
        scan = self.find_scan(scan_nugget_id)
        if not scan:
            return self.find_by_nugget_id(host_nugget_id)
        return self.contained(scan["id"], nugget_id=host_nugget_id)

    def ordered_hosts(
        self,
        scan_nugget_id: str = "SCAN_RECORD",
        host_nugget_id: str = "HOST",
    ) -> List[Node]:
        primary_ids = {
            host["id"] for host in self.scan_hosts(scan_nugget_id, host_nugget_id)
        }
        primary = self.scan_hosts(scan_nugget_id, host_nugget_id)
        trace_only = [
            host
            for host in self.find_by_nugget_id(host_nugget_id)
            if host["id"] not in primary_ids
        ]
        return primary + trace_only

    def trace_hops(self, trace: Node) -> List[Node]:
        hops = self.contained(trace["id"], nugget_id="TRACE_HOP")

        def hop_order(hop: Node) -> Tuple[int, str]:
            order = self.descriptors(hop["id"])
            for desc in order:
                if desc.get("nugget_id") == "HOP_ORDER":
                    try:
                        return (int(node_value(desc)), hop["id"])
                    except ValueError:
                        return (9999, hop["id"])
            return (9999, hop["id"])

        return sorted(hops, key=hop_order)

    def hop_router_host(self, hop: Node) -> Optional[Node]:
        return next(iter(self.contained(hop["id"], nugget_id="HOST")), None)

    def hop_ip(self, hop: Node) -> Optional[str]:
        host = self.hop_router_host(hop)
        if not host:
            return None
        networks = self.contained(host["id"], nugget_id="NETWORKS")
        for net in networks:
            for ip in self.contained_ip_addresses(net["id"]):
                return node_value(ip)
        return node_value(host)

    def service_port(self, service: Node) -> Optional[Node]:
        return next(iter(self.outgoing(service["id"], relation="listens-to", nugget_id="PORT")), None)

    def port_services(self, port: Node) -> List[Node]:
        return self.incoming(port["id"], relation="listens-to", nugget_id="SERVICE")

    def host_category(self, host: Node, category_id: str) -> Optional[Node]:
        return next(iter(self.contained(host["id"], nugget_id=category_id)), None)

    def all_nodes(self) -> List[Node]:
        return self._sort_nodes(list(self.nodes.values()))

    @staticmethod
    def _sort_nodes(nodes: Iterable[Node]) -> List[Node]:
        return sorted(
            nodes,
            key=lambda n: (
                str(n.get("nugget_type", "")),
                str(n.get("nugget_id", "")),
                node_value(n),
                str(n.get("id", "")),
            ),
        )


@dataclass
class NarrativeConfig:
    tool_name: str = "OSINT"
    scan_nugget_id: str = "SCAN_RECORD"
    host_nugget_id: str = "HOST"
    trace_nugget_id: str = "TRACE"
    environment_category: str = "ENVIRONMENT"
    networks_category: str = "NETWORKS"
    applications_category: str = "APPLICATIONS"
    vulnerabilities_category: str = "VULNERABILITIES"
    footer_brand: str = "OS-Intel Scan"
    extra_sections: List[Callable[["NarrativeReportBuilder"], None]] = field(default_factory=list)


class NarrativeReportBuilder:
    """Build a §4.3 narrative Markdown document from a semantic graph."""

    def __init__(
        self,
        graph: Graph,
        scenario_key: str,
        config: Optional[NarrativeConfig] = None,
    ) -> None:
        self.raw_graph = graph
        self.graph = SemanticGraph(graph)
        self.scenario_key = scenario_key
        self.config = config or NarrativeConfig()
        self.lines: List[str] = []
        self._mentioned_values: Set[str] = set()

    def build(self) -> str:
        self.lines = []
        self._mentioned_values = set()
        self._title()
        self._introduction()
        self._scan_section()
        for host in self.graph.ordered_hosts(
            self.config.scan_nugget_id, self.config.host_nugget_id
        ):
            self._host_section(host)
        self._trace_section()
        self._conclusion()
        self._appendix()
        self._footer()
        for hook in self.config.extra_sections:
            hook(self)
        return "\n".join(self.lines).strip() + "\n"

    def mention(self, value: str) -> None:
        text = str(value).strip()
        if text:
            self._mentioned_values.add(text)

    def mention_node(self, node: Node) -> None:
        self.mention(node_value(node))

    def _title(self) -> None:
        tool = self.config.tool_name
        self.lines.extend(
            [
                f"# {tool} OSINT Scan Report — {self.scenario_key}",
                "",
            ]
        )

    def _introduction(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        target = self._descriptor_value(scan, "SCAN_TARGET") if scan else self.scenario_key
        self.mention(target)
        self.lines.extend(
            [
                "## Introduction",
                "",
                (
                    f"This report narrates the findings of a **{self.config.tool_name}** scan "
                    f"against **{target}**. The story follows the scan itself, each discovered host, "
                    "and any traceroute path recorded during the run. Every observed nugget and value "
                    "from the semantic graph appears in the narrative below or in the appendix."
                ),
                "",
            ]
        )

    def _scan_section(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        if not scan:
            return

        self.mention_node(scan)
        descriptors = self.graph.descriptors(scan["id"])
        for desc in descriptors:
            self.mention_node(desc)

        tool = self._descriptor_value(scan, "SCAN_TOOL") or self.config.tool_name.lower()
        version = self._descriptor_value(scan, "SCAN_VERSION") or "unknown"
        target = self._descriptor_value(scan, "SCAN_TARGET") or "unspecified target"
        started = self._descriptor_value(scan, "SCAN_START") or "an unspecified time"
        cli = self._descriptor_value(scan, "SCAN_CLI") or "(command not recorded)"
        summary = self._descriptor_value(scan, "SCAN_SUMMARY") or ""
        elapsed = self._descriptor_value(scan, "SCAN_ELAPSED")

        hosts = self.graph.scan_hosts(
            self.config.scan_nugget_id, self.config.host_nugget_id
        )
        host_count = len(hosts)

        self.lines.extend(["## Scan", ""])
        self.lines.append(
            f"The scan was executed with **{tool}** version **{version}**, "
            f"targeting **{target}** from **{started}**. "
            f"The operator invoked: `{cli}`."
        )
        if elapsed:
            self.lines.append(f" The run completed in **{elapsed}** seconds.")
        self.lines.append("")
        if summary:
            self.lines.append(summary)
            self.lines.append("")
        self.lines.append(
            f"During this scan, **{host_count}** host{'s' if host_count != 1 else ''} "
            f"{'were' if host_count != 1 else 'was'} placed under investigation."
        )
        extra_desc = [
            d
            for d in descriptors
            if d.get("nugget_id")
            not in {
                "SCAN_TOOL",
                "SCAN_VERSION",
                "SCAN_TARGET",
                "SCAN_START",
                "SCAN_CLI",
                "SCAN_SUMMARY",
                "SCAN_ELAPSED",
            }
        ]
        if extra_desc:
            self.lines.append("")
            self.lines.append("Additional scan metadata:")
            for desc in extra_desc:
                self.lines.append(f"- {descriptor_phrase(desc)}")
        self.lines.append("")

    def _host_section(self, host: Node) -> None:
        host_data = node_value(host)
        self.mention_node(host)
        self.lines.extend([f"## Host {host_data}", ""])

        desc_lines = []
        for desc in self.graph.descriptors(host["id"]):
            self.mention_node(desc)
            nid = desc.get("nugget_id", "")
            val = node_value(desc)
            if nid == "HOST_STATUS":
                reason = self._descriptor_value(host, "HOST_STATUS_REASON")
                if reason:
                    self.mention(reason)
                    desc_lines.append(
                        f"The host was observed as **{val}** (reason: **{reason}**)."
                    )
                else:
                    desc_lines.append(f"The host was observed as **{val}**.")
            elif nid == "HOST_STATUS_REASON":
                continue
            elif nid == "INTERNET_NAME":
                desc_lines.append(f"It answers to the internet name **{val}**.")
            else:
                desc_lines.append(f"It carries {descriptor_phrase(desc)}.")

        if desc_lines:
            self.lines.extend(desc_lines)
        else:
            self.lines.append(f"Host **{host_data}** was discovered during the scan.")
        self.lines.append("")

        self._host_environment(host)
        self._host_networks(host)
        self._host_applications(host)
        self._host_vulnerabilities(host)

    def _host_environment(self, host: Node) -> None:
        env = self.graph.host_category(host, self.config.environment_category)
        if not env:
            return
        self.mention_node(env)
        self.lines.extend(["### Environment", ""])
        os_nodes = self.graph.contained(env["id"], nugget_id="OPERATING_SYSTEM")
        if not os_nodes:
            self.lines.append(
                f"The **{node_label(env)}** category was recorded but no operating system "
                "fingerprint was attached."
            )
            self.lines.append("")
            return
        for os_node in os_nodes:
            self.mention_node(os_node)
            accuracy = self._descriptor_value(os_node, "OS_MATCH_ACCURACY")
            if accuracy:
                self.mention(accuracy)
                self.lines.append(
                    f"The host environment indicates **{node_value(os_node)}** "
                    f"(match accuracy **{accuracy}**)."
                )
            else:
                self.lines.append(
                    f"The host environment indicates operating system **{node_value(os_node)}**."
                )
            for desc in self.graph.descriptors(os_node["id"]):
                if desc.get("nugget_id") != "OS_MATCH_ACCURACY":
                    self.mention_node(desc)
                    self.lines.append(f"- {descriptor_phrase(desc)}")
        self.lines.append("")

    def _host_networks(self, host: Node) -> None:
        nets = self.graph.host_category(host, self.config.networks_category)
        if not nets:
            return
        self.mention_node(nets)
        self.lines.extend(["### Networks", ""])

        ip_nodes: List[Node] = []
        for net in [nets] + self.graph.contained(host["id"], nugget_id="NETWORKS"):
            if net["id"] == nets["id"]:
                pass
            ip_nodes.extend(self.graph.contained_ip_addresses(net["id"]))
        ip_nodes = self.graph._sort_nodes({n["id"]: n for n in ip_nodes}.values())

        if not ip_nodes:
            self.lines.append("No network addresses were recorded under this host.")
            self.lines.append("")
            return

        for ip in ip_nodes:
            self.mention_node(ip)
            self.lines.append(f"Network address **{node_value(ip)}**:")
            transports = self.graph.contained(ip["id"], nugget_id="TRANSPORT")
            if not transports:
                self.lines.append("- No transport endpoints were enumerated.")
                continue
            for transport in transports:
                self.mention_node(transport)
                transport_label = node_value(transport)
                ports = self.graph.contained(transport["id"], nugget_id="PORT")
                if not ports:
                    self.lines.append(f"- Transport **{transport_label}** carried no enumerated ports.")
                    continue
                for port in ports:
                    self._narrate_port(port, transport_label)
        self.lines.append("")

    def _narrate_port(self, port: Node, transport_label: str) -> None:
        self.mention_node(port)
        port_num = node_value(port)
        state = self._descriptor_value(port, "PORT_STATE") or "unknown"
        reason = self._descriptor_value(port, "PORT_STATE_REASON")
        protocol = self._descriptor_value(port, "PORT_PROTOCOL") or transport_label
        self.mention(state)
        if reason:
            self.mention(reason)
        if protocol:
            self.mention(protocol)

        services = self.port_services(port)
        service_names = ", ".join(node_value(s) for s in services) if services else "an unnamed service"

        line = (
            f"- Port **{port_num}** on **{protocol}** is **{state}**"
        )
        if reason:
            line += f" ({reason})"
        line += f", associated with **{service_names}**."
        self.lines.append(line)

        for desc in self.graph.descriptors(port["id"]):
            if desc.get("nugget_id") not in {"PORT_STATE", "PORT_STATE_REASON", "PORT_PROTOCOL"}:
                self.mention_node(desc)
                self.lines.append(f"  - {descriptor_phrase(desc)}")

    def port_services(self, port: Node) -> List[Node]:
        return self.graph.port_services(port)

    def _host_applications(self, host: Node) -> None:
        apps = self.graph.host_category(host, self.config.applications_category)
        if not apps:
            return
        self.mention_node(apps)
        services = self.graph.contained(apps["id"], nugget_id="SERVICE")
        if not services:
            return

        self.lines.extend(["### Applications", ""])
        for service in services:
            self._narrate_service(service)
        self.lines.append("")

    def _narrate_service(self, service: Node) -> None:
        self.mention_node(service)
        name = node_value(service)
        port = self.graph.service_port(service)
        port_phrase = ""
        if port:
            self.mention_node(port)
            port_phrase = f" listening on port **{node_value(port)}**"

        product = self._descriptor_value(service, "SERVICE_VERSION")
        extra = self._descriptor_value(service, "SERVICE_EXTRAINFO")
        http_title = self._descriptor_value(service, "HTTP_TITLE")

        intro = f"Application service **{name}**{port_phrase}."
        if product:
            self.mention(product)
            intro += f" It runs **{product}**."
        if extra:
            self.mention(extra)
            intro += f" Additional detail: **{extra}**."
        if http_title:
            self.mention(http_title)
            intro += f' The HTTP title banner reads **"{http_title}"**.'
        self.lines.append(intro)

        for desc in self.graph.descriptors(service["id"]):
            if desc.get("nugget_id") not in {
                "SERVICE_VERSION",
                "SERVICE_EXTRAINFO",
                "HTTP_TITLE",
            }:
                self.mention_node(desc)
                self.lines.append(f"- {descriptor_phrase(desc)}")

        for cpe in self.graph.contained(service["id"], nugget_id="CPE_URL"):
            self.mention_node(cpe)
            self.lines.append(f"- Common Platform Enumeration: `{node_value(cpe)}`.")

        for sub in self.graph.contained(service["id"]):
            if sub.get("nugget_id") in SSH_KEY_NUGGETS:
                self._narrate_ssh_key(service, sub)

    def _narrate_ssh_key(self, service: Node, key: Node) -> None:
        self.mention_node(key)
        key_type = node_value(key) if key.get("nugget_id") == key.get("nugget_event_type") else key.get("nugget_id")
        bits = self._descriptor_value(key, "SSH_KEY_BITS")
        algo = self._descriptor_value(key, "SSH_KEY_TYPE")
        pub = self._descriptor_value(key, "SSH_KEY_KEY")
        fingerprint = node_value(key)

        parts = [
            f"The **{node_value(service)}** service exposes an **{key.get('nugget_id')}** SSH host key"
        ]
        if fingerprint and fingerprint not in {bits, algo, pub}:
            parts.append(f" (fingerprint `{fingerprint}`)")
        parts.append(".")
        if algo:
            self.mention(algo)
            parts.append(f" Algorithm: **{algo}**.")
        if bits:
            self.mention(bits)
            parts.append(f" Key size: **{bits}** bits.")
        if pub:
            self.mention(pub)
            parts.append(f" Public key material: `{pub}`")
        self.lines.append("".join(parts))

    def _host_vulnerabilities(self, host: Node) -> None:
        vulns = self.graph.host_category(host, self.config.vulnerabilities_category)
        if not vulns:
            return
        self.mention_node(vulns)
        findings = [
            n
            for n in self.graph.contained(vulns["id"])
            if n.get("nugget_id") not in {self.config.vulnerabilities_category}
        ]
        self.lines.extend(["### Vulnerabilities", ""])
        if not findings:
            self.lines.append("No vulnerability findings were attached to this host.")
        else:
            for finding in findings:
                self.mention_node(finding)
                self.lines.append(f"- {descriptor_phrase(finding)}")
                for desc in self.graph.descriptors(finding["id"]):
                    self.mention_node(desc)
                    self.lines.append(f"  - {descriptor_phrase(desc)}")
        self.lines.append("")

    def _trace_section(self) -> None:
        trace = self.graph.find_trace(self.config.trace_nugget_id)
        if not trace:
            return

        self.mention_node(trace)
        self.lines.extend(["## Traceroute Path", ""])
        for desc in self.graph.descriptors(trace["id"]):
            self.mention_node(desc)
            self.lines.append(f"- {descriptor_phrase(desc)}")

        hops = self.graph.trace_hops(trace)
        if not hops:
            self.lines.append("")
            self.lines.append("No traceroute hops were recorded.")
            self.lines.append("")
            return

        self.lines.extend(["", "Each hop along the path:", ""])
        mermaid_nodes: List[str] = []
        mermaid_edges: List[str] = []
        prev_id: Optional[str] = None

        for index, hop in enumerate(hops, start=1):
            self.mention_node(hop)
            order = self._descriptor_value(hop, "HOP_ORDER") or str(index)
            ttl = self._descriptor_value(hop, "HOP_TTL")
            rtt = self._descriptor_value(hop, "HOP_RTT")
            router = self.graph.hop_router_host(hop)
            ip = self.graph.hop_ip(hop) or (node_value(router) if router else "unknown")
            self.mention(order)
            if ttl:
                self.mention(ttl)
            if rtt:
                self.mention(rtt)
            if router:
                self.mention_node(router)

            hop_line = f"{index}. Hop **{order}**"
            if ttl:
                hop_line += f" (TTL **{ttl}**"
                if rtt:
                    hop_line += f", RTT **{rtt} ms**"
                hop_line += ")"
            hop_line += f" reaches **{ip}**."
            self.lines.append(hop_line)

            node_id = f"hop{index}"
            label = ip.replace('"', "'")
            mermaid_nodes.append(f'  {node_id}["{label}"]')
            if prev_id:
                mermaid_edges.append(f"  {prev_id} --> {node_id}")
            prev_id = node_id

            for desc in self.graph.descriptors(hop["id"]):
                if desc.get("nugget_id") not in {"HOP_ORDER", "HOP_TTL", "HOP_RTT"}:
                    self.mention_node(desc)
                    self.lines.append(f"   - {descriptor_phrase(desc)}")

        self.lines.extend(["", "### Trace diagram", "", "```mermaid", "flowchart LR"])
        self.lines.extend(mermaid_nodes)
        self.lines.extend(mermaid_edges)
        self.lines.extend(["```", ""])

    def _conclusion(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        summary = self._descriptor_value(scan, "SCAN_SUMMARY") if scan else ""
        host_count = len(
            self.graph.ordered_hosts(
                self.config.scan_nugget_id, self.config.host_nugget_id
            )
        )
        node_count = len(self.graph.nodes)
        if summary:
            self.mention(summary)
        self.lines.extend(
            [
                "## Conclusion",
                "",
                (
                    f"The scan captured **{node_count}** semantic nuggets across "
                    f"**{host_count}** host{'s' if host_count != 1 else ''}."
                ),
            ]
        )
        if summary:
            self.lines.append(f" {summary}")
        self.lines.append(
            " The appendix lists every nugget instance and value for audit and downstream review."
        )
        self.lines.extend(["", ""])

    def _appendix(self) -> None:
        self.lines.extend(
            [
                "## Appendix — Complete Nugget Inventory",
                "",
                "| Type | Nugget | Description | Value |",
                "|------|--------|-------------|-------|",
            ]
        )
        for node in self.graph.all_nodes():
            value = node_value(node)
            self.mention(value)
            desc = str(node.get("nugget_description", "")).replace("|", "\\|")
            val_cell = value.replace("|", "\\|")
            self.lines.append(
                f"| {node.get('nugget_type', '')} | {node.get('nugget_id', '')} "
                f"| {desc} | `{val_cell}` |"
            )
        self.lines.append("")

    def _footer(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        date = self._descriptor_value(scan, "SCAN_START") if scan else "unknown date"
        self.mention(date)
        self.lines.extend(
            [
                "---",
                "",
                f"*{self.config.footer_brand} · {date} · Page 1*",
                "",
            ]
        )

    def _descriptor_value(self, entity: Node | str, nugget_id: str) -> Optional[str]:
        entity_id = entity if isinstance(entity, str) else entity["id"]
        for desc in self.graph.descriptors(entity_id):
            if desc.get("nugget_id") == nugget_id:
                return node_value(desc)
        return None


def build_narrative_report(
    graph: Graph,
    scenario_key: str,
    config: Optional[NarrativeConfig] = None,
) -> str:
    return NarrativeReportBuilder(graph, scenario_key, config).build()


def validate_narrative_coverage(
    graph: Graph,
    markdown: str,
    *,
    require_appendix: bool = True,
) -> Tuple[bool, List[str]]:
    """Return (ok, missing_values) — every node nugget_data must appear in markdown."""
    missing: List[str] = []
    for node in graph.get("nodes", []):
        value = node_value(node)
        if not value:
            continue
        if value not in markdown:
            missing.append(value)
    ok = not missing
    if require_appendix and "## Appendix" not in markdown:
        ok = False
        missing.append("(appendix section missing)")
    return ok, missing


NMAP_NARRATIVE_CONFIG = NarrativeConfig(
    tool_name="Nmap",
    scan_nugget_id="SCAN_RECORD",
    host_nugget_id="HOST",
    trace_nugget_id="TRACE",
    environment_category="ENVIRONMENT",
    networks_category="NETWORKS",
    applications_category="APPLICATIONS",
    vulnerabilities_category="VULNERABILITIES",
    footer_brand="OS-Intel Scan",
)


def build_nmap_narrative_report(graph: Graph, scenario_key: str) -> str:
    return build_narrative_report(graph, scenario_key, NMAP_NARRATIVE_CONFIG)


def _mermaid_label(value: str) -> str:
    return str(value).replace('"', "'").replace("\n", " ").strip()


NETDISCOVER_NARRATIVE_CONFIG = NarrativeConfig(
    tool_name="Netdiscover",
    scan_nugget_id="SCAN_RECORD",
    host_nugget_id="SYSTEM",
    trace_nugget_id="TRACE",
    environment_category="ENVIRONMENT",
    networks_category="NETWORKS",
    applications_category="APPLICATIONS",
    vulnerabilities_category="VULNERABILITIES",
    footer_brand="OS-Intel Scan",
)


class NetdiscoverNarrativeReportBuilder(NarrativeReportBuilder):
    """§4.3 narrative for ARP/LAN discovery graphs (SYSTEM / NETWORKS / MAC_VENDOR)."""

    def _introduction(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        target = node_value(scan) if scan else self.scenario_key
        self.mention(target)
        self.lines.extend(
            [
                "## Introduction",
                "",
                (
                    f"This report narrates the findings of a **{self.config.tool_name}** ARP discovery "
                    f"run for **{target}**. The story follows the scan metadata, each discovered "
                    "**system** on the segment, and the **networks** inventory (IPv4, MAC, and vendor) "
                    "attached to every system. Every observed nugget and value from the semantic graph "
                    "appears in the narrative below or in the appendix."
                ),
                "",
            ]
        )

    def _scan_section(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        if not scan:
            return

        self.mention_node(scan)
        descriptors = self.graph.descriptors(scan["id"])
        for desc in descriptors:
            self.mention_node(desc)

        args = self._descriptor_value(scan, "SCAN_ARGS") or node_value(scan)
        started = self._descriptor_value(scan, "SCAN_TIMESTAMP") or "an unspecified time"
        ended = self._descriptor_value(scan, "SCAN_END_TIME")
        summary = self._descriptor_value(scan, "SCAN_SUMMARY") or ""
        exit_status = self._descriptor_value(scan, "SCAN_EXIT_STATUS")
        tries = self._descriptor_value(scan, "SCAN_TRIES")
        empty = self._descriptor_value(scan, "SCAN_EMPTY_SCANS")
        discovered = self._descriptor_value(scan, "SCAN_DISCOVERED")

        systems = self.graph.scan_hosts(
            self.config.scan_nugget_id, self.config.host_nugget_id
        )
        system_count = len(systems)

        self.lines.extend(["## Scan", ""])
        self.lines.append(
            f"The scan started at **{started}** with arguments `{args}`."
        )
        if ended:
            self.mention(ended)
            self.lines.append(f" It finished at **{ended}**.")
        if exit_status:
            self.mention(exit_status)
            self.lines.append(f" Exit status: **{exit_status}**.")
        self.lines.append("")
        if summary:
            self.mention(summary)
            self.lines.append(summary)
            self.lines.append("")
        if tries is not None:
            self.mention(tries)
            empty_phrase = f", **{empty}** empty scan(s)" if empty is not None else ""
            self.lines.append(
                f"Netdiscover recorded **{tries}** scan frame(s){empty_phrase} "
                f"before settling on the host table used for this graph."
            )
        if discovered is not None:
            self.mention(discovered)
            self.lines.append(
                f"**{discovered}** system(s) appear in the structured host inventory."
            )
        self.lines.append(
            f"**{system_count}** system node(s) are linked from the scan record in this graph."
        )

        extra_desc = [
            d
            for d in descriptors
            if d.get("nugget_id")
            not in {
                "SCAN_ARGS",
                "SCAN_TIMESTAMP",
                "SCAN_END_TIME",
                "SCAN_SUMMARY",
                "SCAN_EXIT_STATUS",
                "SCAN_TRIES",
                "SCAN_EMPTY_SCANS",
                "SCAN_DISCOVERED",
            }
        ]
        if extra_desc:
            self.lines.append("")
            self.lines.append("Additional scan metadata:")
            for desc in extra_desc:
                self.lines.append(f"- {descriptor_phrase(desc)}")
        self.lines.append("")
        if systems:
            self._scan_topology_mermaid(scan, systems)

    def _scan_topology_mermaid(self, scan: Node, systems: Sequence[Node]) -> None:
        self.lines.extend(["### Scan topology", "", "```mermaid", "flowchart TD"])
        scan_id = "scan"
        self.lines.append(f'  {scan_id}["SCAN_RECORD"]')
        for index, system in enumerate(systems, start=1):
            node_id = f"sys{index}"
            label = _mermaid_label(node_value(system))
            self.lines.append(f'  {node_id}["SYSTEM {label}"]')
            self.lines.append(f"  {scan_id} -->|contains| {node_id}")
        self.lines.extend(["```", ""])

    def _host_section(self, host: Node) -> None:
        system_data = node_value(host)
        self.mention_node(host)
        self.lines.extend([f"## System {system_data}", ""])
        self.lines.append(
            f"System **{system_data}** was observed on the local segment during ARP discovery."
        )
        self.lines.append("")
        self._host_networks(host)

    def _host_networks(self, host: Node) -> None:
        nets = self.graph.host_category(host, self.config.networks_category)
        if not nets:
            return
        self.mention_node(nets)
        self.lines.extend(["### Networks", ""])
        self._system_network_mermaid(host, nets)

        ip_nodes = self.graph.contained_ip_addresses(nets["id"])
        mac_nodes = self.graph.contained(nets["id"], nugget_id="MAC_ADDRESS")

        if not ip_nodes and not mac_nodes:
            self.lines.append("No network addresses were recorded under this system.")
            self.lines.append("")
            return

        for ip in ip_nodes:
            self.mention_node(ip)
            self.lines.append(f"- IPv4 address **{node_value(ip)}**.")

        for mac in mac_nodes:
            self.mention_node(mac)
            mac_val = node_value(mac)
            vendors = [
                d for d in self.graph.descriptors(mac["id"]) if d.get("nugget_id") == "MAC_VENDOR"
            ]
            if vendors:
                for vendor in vendors:
                    self.mention_node(vendor)
                    self.lines.append(
                        f"- MAC address **{mac_val}** — vendor **{node_value(vendor)}**."
                    )
            else:
                self.lines.append(f"- MAC address **{mac_val}** (no vendor descriptor).")

        self.lines.append("")

    def _system_network_mermaid(self, system: Node, networks: Node) -> None:
        ip = next(iter(self.graph.contained_ip_addresses(networks["id"])), None)
        mac = next(iter(self.graph.contained(networks["id"], nugget_id="MAC_ADDRESS")), None)
        vendor = None
        if mac:
            vendor = next(
                (
                    d
                    for d in self.graph.descriptors(mac["id"])
                    if d.get("nugget_id") == "MAC_VENDOR"
                ),
                None,
            )
            if vendor:
                self.mention_node(vendor)

        self.lines.extend(["```mermaid", "flowchart TD"])
        self.lines.append(f'  system["SYSTEM {_mermaid_label(node_value(system))}"]')
        self.lines.append('  nets["NETWORKS"]')
        self.lines.append(f"  system -->|contains| nets")
        if ip:
            ip_type = str(ip.get("nugget_id") or "IPV4_ADDRESS")
            self.lines.append(f'  ip["{ip_type}"]')
            self.lines.append(f"  nets -->|contains| ip")
        if mac:
            self.lines.append(f'  mac["MAC_ADDRESS"]')
            self.lines.append(f"  nets -->|contains| mac")
        if mac and vendor:
            self.lines.append(f'  vendor["MAC_VENDOR"]')
            self.lines.append(f"  mac -->|had| vendor")
        self.lines.extend(["```", ""])

    def _conclusion(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        summary = self._descriptor_value(scan, "SCAN_SUMMARY") if scan else ""
        system_count = len(
            self.graph.ordered_hosts(
                self.config.scan_nugget_id, self.config.host_nugget_id
            )
        )
        node_count = len(self.graph.nodes)
        if summary:
            self.mention(summary)
        self.lines.extend(
            [
                "## Conclusion",
                "",
                (
                    f"The scan captured **{node_count}** semantic nuggets across "
                    f"**{system_count}** system{'s' if system_count != 1 else ''}."
                ),
            ]
        )
        if summary:
            self.lines.append(f" {summary}")
        self.lines.append(
            " The appendix lists every nugget instance and value for audit and downstream review."
        )
        self.lines.extend(["", ""])


    def _footer(self) -> None:
        scan = self.graph.find_scan(self.config.scan_nugget_id)
        date = self._descriptor_value(scan, "SCAN_TIMESTAMP") if scan else "unknown date"
        self.mention(date or "unknown date")
        self.lines.extend(
            [
                "---",
                "",
                f"*{self.config.footer_brand} · {date or 'unknown date'} · Page 1*",
                "",
            ]
        )


def build_netdiscover_narrative_report(graph: Graph, scenario_key: str) -> str:
    return NetdiscoverNarrativeReportBuilder(
        graph, scenario_key, NETDISCOVER_NARRATIVE_CONFIG
    ).build()
