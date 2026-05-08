from __future__ import annotations

from datetime import datetime
from typing import Iterable

from app.models import EvidenceItem, EvidenceNote, Investigation


def _line(value: str | None) -> str:
    return value.strip() if value and value.strip() else "Not provided"


def _format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M UTC")


def _risk_reasons(reasons: Iterable[dict]) -> str:
    items = list(reasons)
    if not items:
        return "- No risk adjustments have been recorded yet."
    return "\n".join(
        f"- {item.get('reason', 'Risk adjustment')}: {item.get('delta', 0):+d}. {item.get('explanation', '')}".rstrip()
        for item in items
    )


def _analysis_findings(findings: Iterable[dict]) -> str:
    items = list(findings)
    if not items:
        return "- No analysis findings recorded. Run analysis to populate this section."
    lines = []
    for finding in items:
        evidence = f" (evidence #{finding['evidence_id']})" if finding.get("evidence_id") else ""
        delta = finding.get("score_delta", 0)
        lines.append(
            f"- **{finding.get('title', 'Finding')}**{evidence} [{finding.get('severity', 'info')}, {delta:+d}]: {finding.get('explanation', '')}"
        )
    return "\n".join(lines)


def _evidence_list(evidence_items: Iterable[EvidenceItem]) -> str:
    items = list(evidence_items)
    if not items:
        return "- No uploaded evidence yet."
    lines = []
    for item in items:
        dimensions = ""
        if item.metadata_json.get("width") and item.metadata_json.get("height"):
            dimensions = f", {item.metadata_json['width']}x{item.metadata_json['height']}"
        lines.append(
            f"- **{item.file_name}** ({item.content_type}, {item.file_size} bytes{dimensions}) uploaded {_format_datetime(item.uploaded_at)}. SHA-256: `{item.sha256}`"
        )
    return "\n".join(lines)


def _notes_list(notes: Iterable[EvidenceNote]) -> str:
    items = list(notes)
    if not items:
        return "- No evidence notes yet."
    lines = []
    for note in items:
        source = f" Source: {_line(note.source)}." if note.source else ""
        lines.append(
            f"- **{note.title}** ({note.type}, {note.confidence}, {_format_datetime(note.created_at)}): {note.explanation}{source}"
        )
    return "\n".join(lines)


def _timeline(investigation: Investigation) -> str:
    entries = [
        (_format_datetime(investigation.created_at), "Investigation created"),
    ]
    entries.extend((_format_datetime(item.uploaded_at), f"Evidence uploaded: {item.file_name}") for item in investigation.evidence_items)
    entries.extend((_format_datetime(note.created_at), f"Evidence note added: {note.title}") for note in investigation.notes)
    entries = sorted(entries, key=lambda item: item[0])
    return "\n".join(f"- {date}: {text}" for date, text in entries)


def generate_markdown_report(investigation: Investigation) -> str:
    summary = investigation.description or "No written summary has been added yet."
    conclusion = (
        f"Current status: **{investigation.status}**. "
        f"The transparent risk score is **{investigation.risk_score}/100 ({investigation.risk_label})**. "
        "Treat this as an evidence organization aid, not an absolute truth judgment."
    )

    return f"""# ProofGarden Verification Report: {investigation.title}

## Claim
{investigation.claim}

## Overview
- Category: {investigation.category}
- Status: {investigation.status}
- Source URL: {_line(investigation.source_url)}
- Created: {_format_datetime(investigation.created_at)}
- Updated: {_format_datetime(investigation.updated_at)}
- Risk score: {investigation.risk_score}/100 ({investigation.risk_label})

## Summary
{summary}

## Uploaded Evidence
{_evidence_list(investigation.evidence_items)}

## Evidence Notes
{_notes_list(investigation.notes)}

## Analysis Findings
{_analysis_findings(investigation.analysis_findings)}

## Risk Score Explanation
{_risk_reasons(investigation.risk_reasons)}

## Timeline
{_timeline(investigation)}

## Conclusion
{conclusion}

## Recommended Next Steps
- Preserve original files and URLs where possible.
- Compare the claim against primary sources or official accounts.
- Document any uncertainty and avoid overstating conclusions.
- Add more evidence notes when new context is discovered.

## Disclaimer
ProofGarden helps organize evidence and surface transparent signals. It does not prove absolute truth, identify people, or replace expert forensic review. Use careful language such as "likely", "unverified", or "needs more evidence" when sharing conclusions.
"""

