from __future__ import annotations

from typing import Any, Iterable


NEGATIVE_NOTE_TYPES = {
    "Source mismatch",
    "Timestamp mismatch",
    "Known scam pattern",
    "Visual inconsistency",
    "Text clue",
}
NEGATIVE_WORDS = {"scam", "fake", "edited", "mismatch", "inconsistent", "spoof", "phishing", "impersonation"}
VERIFIED_WORDS = {"verified", "official", "confirmed", "authentic", "original source", "source confirms"}
CONFIDENCE_POINTS = {"Low": 5, "Medium": 10, "High": 20}


def risk_label(score: int) -> str:
    if score <= 24:
        return "Low"
    if score <= 49:
        return "Medium"
    if score <= 74:
        return "High"
    return "Critical"


def clamp_score(score: int) -> int:
    return max(0, min(100, score))


def _note_text(note: Any) -> str:
    return f"{getattr(note, 'title', '')} {getattr(note, 'explanation', '')}".lower()


def calculate_risk_score(
    *,
    source_url: str | None,
    notes: Iterable[Any],
    findings: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    score = 0
    reasons: list[dict[str, Any]] = []

    if not source_url:
        score += 10
        reasons.append(
            {
                "reason": "No source URL provided",
                "delta": 10,
                "explanation": "Claims without an origin are harder to verify and receive a small risk increase.",
            }
        )

    for finding in findings:
        delta = int(finding.get("score_delta") or 0)
        if finding.get("module") == "text_patterns" and delta:
            score += delta
            reasons.append(
                {
                    "reason": finding.get("title", "Suspicious text pattern"),
                    "delta": delta,
                    "explanation": finding.get("explanation", ""),
                    "details": finding.get("details", {}),
                }
            )

    for note in notes:
        note_type = getattr(note, "type", "")
        confidence = getattr(note, "confidence", "Low")
        text = _note_text(note)
        base_delta = CONFIDENCE_POINTS.get(confidence, 5)

        looks_negative = note_type in NEGATIVE_NOTE_TYPES or any(word in text for word in NEGATIVE_WORDS)
        if looks_negative:
            score += base_delta
            reasons.append(
                {
                    "reason": f"{confidence}-confidence {note_type} note",
                    "delta": base_delta,
                    "explanation": getattr(note, "explanation", ""),
                }
            )

        looks_verified = note_type == "External reference" and any(word in text for word in VERIFIED_WORDS)
        if looks_verified:
            delta = -8 if confidence == "High" else -5
            score += delta
            reasons.append(
                {
                    "reason": f"{confidence}-confidence verified source evidence",
                    "delta": delta,
                    "explanation": getattr(note, "explanation", ""),
                }
            )

    clamped = clamp_score(score)
    if clamped != score:
        reasons.append(
            {
                "reason": "Risk score clamped",
                "delta": clamped - score,
                "explanation": "Scores are constrained to the transparent 0-100 range.",
            }
        )

    return {"score": clamped, "label": risk_label(clamped), "reasons": reasons}

