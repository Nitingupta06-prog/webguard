from __future__ import annotations

from urllib.parse import urlparse

import requests


SQLI_PAYLOADS = ["'", '"', "' OR '1'='1"]
XSS_PAYLOAD = "<script>webguard_xss_probe</script>"


def test_payloads(target: str) -> dict[str, object]:
    parsed = urlparse(target)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"

    sqli_detected = False
    xss_detected = False

    try:
        for payload in SQLI_PAYLOADS:
            response = requests.get(base_url, params={"webguard": payload}, timeout=10)
            body = response.text.lower()
            if any(keyword in body for keyword in ["sql syntax", "mysql", "postgresql", "odbc", "sqlite"]):
                sqli_detected = True
                break

        response = requests.get(base_url, params={"webguard": XSS_PAYLOAD}, timeout=10)
        if XSS_PAYLOAD.lower() in response.text.lower():
            xss_detected = True

        severity = "critical" if sqli_detected or xss_detected else "info"
        return {"sqli_detected": sqli_detected, "xss_detected": xss_detected, "severity": severity}
    except Exception:
        return {"sqli_detected": False, "xss_detected": False, "severity": "info", "error": "payload test failed"}
