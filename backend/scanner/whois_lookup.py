from __future__ import annotations

from urllib.parse import urlparse

import whois


def lookup_whois(target: str) -> dict[str, object]:
    try:
        parsed = urlparse(target)
        host = parsed.hostname or target
        domain_info = whois.whois(host)
        registrar = getattr(domain_info, "registrar", None) or domain_info.get("registrar") or "Unknown"
        creation_date = getattr(domain_info, "creation_date", None) or domain_info.get("creation_date")
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        severity = "info"
        return {
            "registrar": str(registrar),
            "creation_date": creation_date.isoformat() if hasattr(creation_date, "isoformat") else creation_date,
            "severity": severity,
        }
    except Exception:
        return {"registrar": "Unknown", "creation_date": None, "severity": "info", "error": "whois lookup failed"}
