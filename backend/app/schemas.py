from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Category(str, Enum):
    screenshot = "Screenshot"
    image = "Image"
    email = "Email"
    social_media_post = "Social media post"
    document = "Document"
    scam_message = "Scam message"
    delivery_support_claim = "Delivery/customer support claim"
    public_claim = "Public claim"
    other = "Other"


class InvestigationStatus(str, Enum):
    unverified = "Unverified"
    likely_real = "Likely real"
    likely_edited = "Likely edited"
    likely_ai_generated = "Likely AI-generated"
    likely_scam = "Likely scam"
    needs_more_evidence = "Needs more evidence"
    debunked = "Debunked"


class NoteType(str, Enum):
    metadata_clue = "Metadata clue"
    text_clue = "Text clue"
    source_mismatch = "Source mismatch"
    timestamp_mismatch = "Timestamp mismatch"
    known_scam_pattern = "Known scam pattern"
    visual_inconsistency = "Visual inconsistency"
    user_testimony = "User testimony"
    external_reference = "External reference"
    other = "Other"


class Confidence(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class InvestigationBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    claim: str = Field(min_length=1)
    category: Category
    source_url: HttpUrl | None = None
    description: str | None = None
    status: InvestigationStatus = InvestigationStatus.unverified


class InvestigationCreate(InvestigationBase):
    pass


class InvestigationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    claim: str | None = Field(default=None, min_length=1)
    category: Category | None = None
    source_url: HttpUrl | None = None
    description: str | None = None
    status: InvestigationStatus | None = None


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    investigation_id: int
    file_name: str
    stored_name: str
    content_type: str
    file_size: int
    sha256: str
    metadata_json: dict[str, Any]
    analysis_findings: list[dict[str, Any]]
    uploaded_at: datetime


class EvidenceNoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    type: NoteType
    confidence: Confidence
    explanation: str = Field(min_length=1)
    source: str | None = Field(default=None, max_length=500)


class EvidenceNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    investigation_id: int
    title: str
    type: str
    confidence: str
    explanation: str
    source: str | None
    created_at: datetime


class InvestigationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    claim: str
    category: str
    source_url: str | None
    description: str | None
    status: str
    risk_score: int
    risk_label: str
    risk_reasons: list[dict[str, Any]]
    analysis_findings: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    evidence_items: list[EvidenceRead] = []
    notes: list[EvidenceNoteRead] = []


class AnalysisFinding(BaseModel):
    module: str
    title: str
    severity: str
    explanation: str
    evidence_id: int | None = None
    score_delta: int = 0
    details: dict[str, Any] = {}


class RiskResult(BaseModel):
    score: int
    label: str
    reasons: list[dict[str, Any]]


class AnalyzeResponse(BaseModel):
    investigation: InvestigationRead
    findings: list[AnalysisFinding]
    risk: RiskResult


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "ProofGarden API"

