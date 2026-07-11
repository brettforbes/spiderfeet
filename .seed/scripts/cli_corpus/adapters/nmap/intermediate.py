"""Parse Nmap -oX XML into the SPEC-004 `nmap_scan_v1` intermediate document."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Any


def _host_key(addresses: list[tuple[str, str]]) -> str:
    for addr, _ in addresses:
        if "." in addr:
            return addr
    return addresses[0][0] if addresses else "unknown-host"


def _parse_addresses(host_el: ET.Element) -> list[tuple[str, str]]:
    return [
        (el.get("addr", ""), el.get("addrtype", ""))
        for el in host_el.findall("address")
        if el.get("addr")
    ]


def _table_values(table_el: ET.Element) -> dict[str, str]:
    values: dict[str, str] = {}
    for elem in table_el.findall("elem"):
        key = elem.get("key")
        if key:
            values[key] = (elem.text or "").strip()
    return values


def _parse_scripts(port_el: ET.Element) -> dict[str, Any]:
    scripts: dict[str, Any] = {}
    for script_el in port_el.findall("script"):
        script_id = script_el.get("id")
        if not script_id:
            continue
        if script_id == "ssh-hostkey":
            keys = []
            for table_el in script_el.findall("table"):
                values = _table_values(table_el)
                if values:
                    keys.append(values)
            scripts["ssh_hostkeys"] = keys
        elif script_id == "http-title":
            title = ""
            for elem in script_el.findall("elem"):
                if elem.get("key") == "title":
                    title = (elem.text or "").strip()
                    break
            if not title:
                output = (script_el.get("output") or "").strip()
                title = next((line.strip() for line in output.splitlines() if line.strip()), "")
            if title:
                scripts["http_title"] = title
    return scripts


def _parse_ports(host_el: ET.Element) -> list[dict[str, Any]]:
    ports_el = host_el.find("ports")
    if ports_el is None:
        return []

    ports: list[dict[str, Any]] = []
    for port_el in ports_el.findall("port"):
        portid = port_el.get("portid", "")
        if not portid:
            continue
        state_el = port_el.find("state")
        service_el = port_el.find("service")
        service: dict[str, Any] = {}
        if service_el is not None:
            service = {
                "name": service_el.get("name") or "unknown",
                "product": service_el.get("product"),
                "version": service_el.get("version"),
                "extrainfo": service_el.get("extrainfo"),
                "servicefp": service_el.get("servicefp"),
                "cpes": [(cpe_el.text or "").strip() for cpe_el in service_el.findall("cpe") if (cpe_el.text or "").strip()],
            }
        ports.append(
            {
                "protocol": port_el.get("protocol", "tcp"),
                "portid": portid,
                "state": state_el.get("state") if state_el is not None else None,
                "state_reason": state_el.get("reason") if state_el is not None else None,
                "source": "port_scan",
                "service": service,
                "scripts": _parse_scripts(port_el),
            }
        )
    return ports


def _parse_os(host_el: ET.Element) -> dict[str, Any] | None:
    os_el = host_el.find("os")
    if os_el is None:
        return None

    matches: list[dict[str, Any]] = []
    for match_el in os_el.findall("osmatch"):
        classes: list[dict[str, Any]] = []
        for class_el in match_el.findall("osclass"):
            classes.append(
                {
                    "type": class_el.get("type"),
                    "vendor": class_el.get("vendor"),
                    "osfamily": class_el.get("osfamily"),
                    "accuracy": class_el.get("accuracy"),
                    "osgen": class_el.get("osgen"),
                    "cpes": [(cpe_el.text or "").strip() for cpe_el in class_el.findall("cpe") if (cpe_el.text or "").strip()],
                }
            )
        matches.append(
            {
                "name": match_el.get("name", "unknown"),
                "accuracy": match_el.get("accuracy"),
                "classes": classes or [{}],
            }
        )

    portused = [
        {
            "state": el.get("state"),
            "proto": el.get("proto"),
            "portid": el.get("portid"),
        }
        for el in os_el.findall("portused")
        if el.get("portid")
    ]
    return {"matches": matches, "portused": portused}


def _parse_trace(host_el: ET.Element) -> dict[str, Any] | None:
    trace_el = host_el.find("trace")
    if trace_el is None:
        return None
    hops = []
    for hop in trace_el.findall("hop"):
        ipaddr = hop.get("ipaddr", "")
        if not ipaddr:
            continue
        hops.append(
            {
                "ipaddr": ipaddr,
                "ttl": hop.get("ttl"),
                "rtt": hop.get("rtt"),
                "host": hop.get("host"),
            }
        )
    return {"proto": trace_el.get("proto", "unknown"), "hops": hops}


def parse_nmap_xml(xml_text: str) -> dict[str, Any]:
    """Convert one Nmap XML document into `nmap_scan_v1` intermediate JSON."""
    root = ET.fromstring(xml_text)
    args = root.get("args", "")
    version = root.get("version", "")
    startstr = root.get("startstr", "")

    target_match = re.search(r"\s(?:-oX\s+-\s+)?(\S+)\s*$", args)
    scan_target = target_match.group(1) if target_match else "unknown"

    finished: dict[str, Any] = {}
    finished_el = root.find("./runstats/finished")
    if finished_el is not None:
        finished = {
            "summary": finished_el.get("summary"),
            "elapsed": finished_el.get("elapsed"),
            "exit_status": finished_el.get("exit"),
        }

    hosts: list[dict[str, Any]] = []
    for host_el in root.findall("host"):
        addresses = _parse_addresses(host_el)
        if not addresses:
            continue
        host_key = _host_key(addresses)
        status_el = host_el.find("status")
        status = None
        if status_el is not None:
            status = {"state": status_el.get("state"), "reason": status_el.get("reason")}
        hostnames = [
            hn.get("name", "")
            for hn in host_el.findall("./hostnames/hostname")
            if hn.get("name")
        ]
        hosts.append(
            {
                "host_key": host_key,
                "addresses": [{"addr": addr, "addrtype": addrtype} for addr, addrtype in addresses],
                "status": status,
                "hostnames": hostnames,
                "ports": _parse_ports(host_el),
                "os": _parse_os(host_el),
                "trace": _parse_trace(host_el),
            }
        )

    return {
        "schema": "nmap_scan_v1",
        "command": args,
        "version": version,
        "startstr": startstr,
        "scan_target": scan_target,
        "scan_data": f"nmap:{scan_target}:{startstr or args}",
        "finished": finished,
        "hosts": hosts,
    }
