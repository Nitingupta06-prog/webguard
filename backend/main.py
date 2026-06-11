from __future__ import annotations

import asyncio
import io
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl

from db.mongo import fetch_history, fetch_scan_by_id, save_scan
from scanner.header_checker import check_headers
from scanner.payload_tester import test_payloads
from scanner.port_scanner import scan_ports
from scanner.ssl_checker import check_ssl
from scanner.whois_lookup import lookup_whois
from utils.pdf_report import build_pdf_report


class ScanRequest(BaseModel):
    url: HttpUrl


app = FastAPI(title="WebGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _normalize_target(target: HttpUrl | str) -> str:
    value = str(target)
    parsed = urlparse(value)
    if parsed.scheme:
        return value
    return f"https://{value}"


def _overall_severity(results: dict[str, Any]) -> str:
    severities = [
        results.get("ports", {}).get("severity", "info"),
        results.get("ssl", {}).get("severity", "info"),
        results.get("headers", {}).get("severity", "info"),
        results.get("payloads", {}).get("severity", "info"),
        results.get("whois", {}).get("severity", "info"),
    ]
    if "critical" in severities:
        return "critical"
    if "warning" in severities:
        return "warning"
    return "info"


@app.get("/")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/scan")
async def run_scan(payload: ScanRequest) -> dict[str, Any]:
    target = _normalize_target(payload.url)

    try:
        results = await asyncio.gather(
            asyncio.to_thread(scan_ports, target),
            asyncio.to_thread(check_ssl, target),
            asyncio.to_thread(check_headers, target),
            asyncio.to_thread(test_payloads, target),
            asyncio.to_thread(lookup_whois, target),
        )
    except Exception:
        results = [
            {"open_ports": [], "severity": "info", "error": "scan failed"},
            {"valid": False, "expiry_date": None, "issuer": "Unknown", "severity": "info", "error": "scan failed"},
            {"missing": [], "present": [], "severity": "info", "error": "scan failed"},
            {"sqli_detected": False, "xss_detected": False, "severity": "info", "error": "scan failed"},
            {"registrar": "Unknown", "creation_date": None, "severity": "info", "error": "scan failed"},
        ]

    scan_results = {
        "ports": results[0],
        "ssl": results[1],
        "headers": results[2],
        "payloads": results[3],
        "whois": results[4],
    }
    overall = _overall_severity(scan_results)
    timestamp = datetime.now(timezone.utc).isoformat()

    document = {
        "target": target,
        "timestamp": timestamp,
        "results": scan_results,
        "overall_severity": overall,
    }

    scan_id = await save_scan(document)
    document["scan_id"] = scan_id
    return document


@app.get("/api/history")
async def history() -> dict[str, Any]:
    scans = await fetch_history(limit=20)
    return {"scans": scans}


@app.get("/api/report/{scan_id}")
async def report(scan_id: str) -> StreamingResponse:
    scan = await fetch_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    pdf_bytes = build_pdf_report(scan)
    headers = {"Content-Disposition": f'attachment; filename="webguard-report-{scan_id}.pdf"'}
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers=headers)
