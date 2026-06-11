from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf_report(scan: dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("WebGuard Vulnerability Scan Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Target: {scan.get('target', 'Unknown')}", styles["BodyText"]),
        Paragraph(f"Timestamp: {scan.get('timestamp', 'Unknown')}", styles["BodyText"]),
        Paragraph(f"Overall Severity: {scan.get('overall_severity', 'info').title()}", styles["BodyText"]),
        Spacer(1, 12),
    ]

    results = scan.get("results", {})
    rows = [["Check", "Findings", "Severity"]]
    for label, value in [
        ("Ports", results.get("ports", {})),
        ("SSL", results.get("ssl", {})),
        ("Headers", results.get("headers", {})),
        ("Payloads", results.get("payloads", {})),
        ("WHOIS", results.get("whois", {})),
    ]:
        rows.append([label, str(value), str(value.get("severity", "info")).title()])

    table = Table(rows, colWidths=[70, 370, 70])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f8fafc")]),
            ]
        )
    )
    story.append(table)
    document.build(story)
    return buffer.getvalue()
