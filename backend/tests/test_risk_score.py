from dataclasses import dataclass

from app.analysis.risk_score import calculate_risk_score, risk_label


@dataclass
class Note:
    title: str
    type: str
    confidence: str
    explanation: str


def test_risk_score_is_transparent_and_clamped():
    result = calculate_risk_score(
        source_url=None,
        notes=[
            Note(
                title="Phishing language",
                type="Known scam pattern",
                confidence="High",
                explanation="The message asks for a password and contains impersonation language.",
            ),
            Note(
                title="Official source verified",
                type="External reference",
                confidence="High",
                explanation="The original source confirms the claim is authentic.",
            ),
        ],
        findings=[
            {
                "module": "text_patterns",
                "title": "Request for credentials or BankID",
                "score_delta": 20,
                "explanation": "Matched credential request language.",
                "details": {"rule": "credential_request"},
            },
            {
                "module": "text_patterns",
                "title": "Shortened link",
                "score_delta": 15,
                "explanation": "Matched shortened link.",
                "details": {"rule": "shortened_link"},
            },
        ],
    )

    assert result["score"] == 57
    assert result["label"] == "High"
    assert len(result["reasons"]) == 5
    assert all("delta" in reason for reason in result["reasons"])


def test_risk_labels():
    assert risk_label(0) == "Low"
    assert risk_label(25) == "Medium"
    assert risk_label(50) == "High"
    assert risk_label(75) == "Critical"

