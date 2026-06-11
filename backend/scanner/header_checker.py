from __future__ import annotations

import requests


IMPORTANT_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy",
]


def check_headers(target: str) -> dict[str, object]:
    try:
        response = requests.get(target, timeout=10, allow_redirects=True)
        present = [header for header in IMPORTANT_HEADERS if header in response.headers]
        missing = [header for header in IMPORTANT_HEADERS if header not in response.headers]
        severity = "warning" if missing else "info"
        return {"missing": missing, "present": present, "severity": severity}
    except Exception:
        return {"missing": [], "present": [], "severity": "info", "error": "header check failed"}
