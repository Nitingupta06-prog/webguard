from __future__ import annotations

import datetime as dt
import ssl
from urllib.parse import urlparse

import socket


def check_ssl(target: str) -> dict[str, object]:
    parsed = urlparse(target)
    host = parsed.hostname or target
    port = parsed.port or 443

    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                cert = secure_sock.getpeercert()

        expiry_text = cert.get("notAfter")
        expiry_date = None
        severity = "info"
        valid = bool(cert)

        if expiry_text:
            expiry_date = dt.datetime.strptime(expiry_text, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc).isoformat()
            expiry_dt = dt.datetime.strptime(expiry_text, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
            if (expiry_dt - dt.datetime.now(dt.timezone.utc)).days <= 30:
                severity = "warning"

        issuer = ", ".join(value for pair in cert.get("issuer", []) for _, value in pair) or "Unknown"
        return {"valid": valid, "expiry_date": expiry_date, "issuer": issuer, "severity": severity}
    except Exception:
        return {"valid": False, "expiry_date": None, "issuer": "Unknown", "severity": "info", "error": "ssl check failed"}
