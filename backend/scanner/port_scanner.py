from __future__ import annotations
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse


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


def _check_port(host: str, port: int, timeout: float = 1.0) -> int | None:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port
    except Exception:
        return None


def scan_ports(target: str) -> dict[str, object]:
    host = _extract_host(target)

    if _is_private_host(host):
        return {"open_ports": [], "severity": "critical", "error": "private or localhost targets are blocked"}

    # Common important ports to scan
    ports_to_scan = [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
        465, 587, 993, 995, 1433, 1521, 3306, 3389,
        5432, 5900, 6379, 8080, 8443, 8888, 27017
    ]

    open_ports: list[int] = []

    try:
        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = {executor.submit(_check_port, host, port): port for port in ports_to_scan}
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    open_ports.append(result)

        open_ports = sorted(open_ports)
        standard_ports = {80, 443}
        if any(port not in standard_ports for port in open_ports):
            severity = "critical"
        elif open_ports:
            severity = "info"
        else:
            severity = "info"

        return {"open_ports": open_ports, "severity": severity}

    except Exception:
        return {"open_ports": [], "severity": "info", "error": "port scan failed"}