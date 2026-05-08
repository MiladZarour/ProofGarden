from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern


@dataclass(frozen=True)
class PatternRule:
    key: str
    title: str
    severity: str
    score_delta: int
    expressions: tuple[Pattern[str], ...]


def _compile(*patterns: str) -> tuple[Pattern[str], ...]:
    return tuple(re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


PATTERN_RULES: tuple[PatternRule, ...] = (
    PatternRule(
        "urgent_payment",
        "Urgent payment language",
        "medium",
        12,
        _compile(r"\burgent\b.{0,80}\b(pay|payment|fee|invoice|charge)\b", r"\bpay\b.{0,50}\b(now|immediately|today)\b"),
    ),
    PatternRule(
        "fake_delivery",
        "Delivery pressure or failed-delivery wording",
        "medium",
        10,
        _compile(r"\b(package|parcel|delivery|shipment)\b.{0,90}\b(failed|held|customs|fee|reschedule)\b"),
    ),
    PatternRule(
        "support_impersonation",
        "Suspicious support or account security wording",
        "medium",
        10,
        _compile(r"\b(support|helpdesk|customer service)\b.{0,80}\b(verify|restore|unlock|secure)\b"),
    ),
    PatternRule(
        "shortened_link",
        "Shortened link",
        "high",
        15,
        _compile(r"https?://(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|rebrand\.ly|ow\.ly|shorturl\.at)/\S+"),
    ),
    PatternRule(
        "credential_request",
        "Request for credentials or BankID",
        "high",
        20,
        _compile(r"\b(bankid|password|passcode|security code|one-time code|otp|login details)\b"),
    ),
    PatternRule(
        "crypto_payment",
        "Crypto payment request",
        "high",
        18,
        _compile(r"\b(bitcoin|btc|ethereum|eth|usdt|crypto wallet|cryptocurrency)\b"),
    ),
    PatternRule(
        "gift_cards",
        "Gift card payment request",
        "high",
        18,
        _compile(r"\b(gift card|itunes card|apple card|google play card|steam card|voucher)\b"),
    ),
    PatternRule(
        "pressure_phrase",
        "Pressure phrase",
        "medium",
        10,
        _compile(r"\b(act now|final warning|account blocked|last chance|immediate action required|limited time)\b"),
    ),
)


def _sample_matches(text: str, expressions: tuple[Pattern[str], ...]) -> list[str]:
    samples: list[str] = []
    for expression in expressions:
        for match in expression.finditer(text):
            snippet = re.sub(r"\s+", " ", match.group(0)).strip()
            if snippet and snippet.lower() not in {item.lower() for item in samples}:
                samples.append(snippet[:160])
            if len(samples) >= 3:
                return samples
    return samples


def analyze_text_patterns(text: str, context: str, evidence_id: int | None = None) -> list[dict]:
    if not text or not text.strip():
        return []

    findings: list[dict] = []
    for rule in PATTERN_RULES:
        samples = _sample_matches(text, rule.expressions)
        if not samples:
            continue
        findings.append(
            {
                "module": "text_patterns",
                "title": rule.title,
                "severity": rule.severity,
                "explanation": f"Matched suspicious wording in {context}. Review the surrounding source before treating this as conclusive.",
                "evidence_id": evidence_id,
                "score_delta": rule.score_delta,
                "details": {
                    "rule": rule.key,
                    "context": context,
                    "matches": samples,
                },
            }
        )
    return findings

