from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import nmap


def _extract_host(target: str) -> str:
    parsed = urlparse(target)
    return parsed.hostname or target


def _is_private_host(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
    except ValueError:
        try:
            resolved = socket.gethostbyname(host)
            ip = ipaddress.ip_address(resolved)
            return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
        except Exception:
            return True


def scan_ports(target: str) -> dict[str, object]:
    host = _extract_host(target)
    if _is_private_host(host):
        return {"open_ports": [], "severity": "critical", "error": "private or localhost targets are blocked"}

    try:
        scanner = nmap.PortScanner()
        scanner.scan(host, arguments="-Pn -p 1-1000")
        open_ports: list[int] = []
        severity = "info"

        for port in scanner.all_tcp():
            if scanner[host]["tcp"][port]["state"] == "open":
                open_ports.append(int(port))

        if any(port not in {80, 443} for port in open_ports):
            severity = "critical"
        elif open_ports:
            severity = "info"

        return {"open_ports": sorted(open_ports), "severity": severity}
    except Exception:
        return {"open_ports": [], "severity": "info", "error": "port scan failed"}
