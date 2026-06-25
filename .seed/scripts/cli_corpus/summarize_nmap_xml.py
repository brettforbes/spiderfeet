#!/usr/bin/env python3
"""Quick exploration summary of nmap -oX files."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def summarize(path: Path) -> str:
    root = ET.parse(path).getroot()
    hosts = root.findall("host")
    up = [h for h in hosts if h.find("status") is not None and h.find("status").get("state") == "up"]
    lines = [f"=== {path.name} ({len(up)} up / {len(hosts)} total) ==="]
    for h in up[:10]:
        addrs = [(a.get("addrtype"), a.get("addr")) for a in h.findall("address")]
        ip = next((a for t, a in addrs if t == "ipv4"), addrs[0][1] if addrs else "?")
        ports = []
        for p in h.findall(".//port"):
            st = p.find("state")
            if st is None:
                continue
            state = st.get("state")
            pid = p.get("portid")
            proto = p.get("protocol")
            svc = p.find("service")
            sname = svc.get("name") if svc is not None else ""
            prod = (svc.get("product") or "") if svc is not None else ""
            ver = (svc.get("version") or "") if svc is not None else ""
            extra = f" {prod} {ver}".strip()
            ports.append(f"{proto}/{pid} {state} {sname} {extra}".strip())
        os_info = []
        osm = h.find("os")
        if osm is not None:
            for m in osm.findall("osmatch")[:3]:
                os_info.append(f"osmatch {m.get('name')} acc={m.get('accuracy')}")
            if osm.find("osfingerprint") is not None:
                os_info.append("osfingerprint present")
        scripts = [sc.get("id") for sc in h.findall(".//script")]
        lines.append(f"  {ip} ports={len(ports)} scripts={len(scripts)}")
        for p in ports[:15]:
            lines.append(f"    {p}")
        if len(ports) > 15:
            lines.append(f"    ... +{len(ports) - 15} more")
        for o in os_info:
            lines.append(f"    {o}")
        for s in scripts[:8]:
            lines.append(f"    script: {s}")
        if len(scripts) > 8:
            lines.append(f"    ... +{len(scripts) - 8} scripts")
    fin = root.find("runstats/finished")
    if fin is not None:
        lines.append(f"  exit={fin.get('exit')} summary={fin.get('summary')}")
    return "\n".join(lines)


if __name__ == "__main__":
    for f in sorted(Path(sys.argv[1]).glob("*.xml")):
        print(summarize(f))
        print()
