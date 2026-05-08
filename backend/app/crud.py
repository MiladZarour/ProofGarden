from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


def get_investigation(db: Session, investigation_id: int) -> models.Investigation | None:
    statement = (
        select(models.Investigation)
        .options(selectinload(models.Investigation.evidence_items), selectinload(models.Investigation.notes))
        .where(models.Investigation.id == investigation_id)
    )
    return db.scalars(statement).first()


def list_investigations(db: Session) -> list[models.Investigation]:
    statement = (
        select(models.Investigation)
        .options(selectinload(models.Investigation.evidence_items), selectinload(models.Investigation.notes))
        .order_by(models.Investigation.created_at.desc())
    )
    return list(db.scalars(statement).all())


def create_investigation(db: Session, payload: schemas.InvestigationCreate) -> models.Investigation:
    investigation = models.Investigation(
        title=payload.title,
        claim=payload.claim,
        category=payload.category.value,
        source_url=str(payload.source_url) if payload.source_url else None,
        description=payload.description,
        status=payload.status.value,
    )
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    return investigation


def update_investigation(
    db: Session, investigation: models.Investigation, payload: schemas.InvestigationUpdate
) -> models.Investigation:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        if hasattr(value, "value"):
            value = value.value
        if key == "source_url" and value is not None:
            value = str(value)
        setattr(investigation, key, value)
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    return get_investigation(db, investigation.id) or investigation


def delete_investigation(db: Session, investigation: models.Investigation) -> None:
    db.delete(investigation)
    db.commit()


def create_evidence_item(
    db: Session,
    *,
    investigation_id: int,
    file_name: str,
    stored_name: str,
    content_type: str,
    file_size: int,
    file_path: str,
    sha256: str,
    extracted_text: str | None,
    metadata_json: dict,
    analysis_findings: list[dict],
) -> models.EvidenceItem:
    item = models.EvidenceItem(
        investigation_id=investigation_id,
        file_name=file_name,
        stored_name=stored_name,
        content_type=content_type,
        file_size=file_size,
        file_path=file_path,
        sha256=sha256,
        extracted_text=extracted_text,
        metadata_json=metadata_json,
        analysis_findings=analysis_findings,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_evidence(db: Session, investigation_id: int) -> list[models.EvidenceItem]:
    statement = (
        select(models.EvidenceItem)
        .where(models.EvidenceItem.investigation_id == investigation_id)
        .order_by(models.EvidenceItem.uploaded_at.desc())
    )
    return list(db.scalars(statement).all())


def create_note(
    db: Session, investigation_id: int, payload: schemas.EvidenceNoteCreate
) -> models.EvidenceNote:
    note = models.EvidenceNote(
        investigation_id=investigation_id,
        title=payload.title,
        type=payload.type.value,
        confidence=payload.confidence.value,
        explanation=payload.explanation,
        source=payload.source,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session, investigation_id: int) -> list[models.EvidenceNote]:
    statement = (
        select(models.EvidenceNote)
        .where(models.EvidenceNote.investigation_id == investigation_id)
        .order_by(models.EvidenceNote.created_at.desc())
    )
    return list(db.scalars(statement).all())


def get_note(db: Session, note_id: int) -> models.EvidenceNote | None:
    return db.get(models.EvidenceNote, note_id)


def delete_note(db: Session, note: models.EvidenceNote) -> None:
    db.delete(note)
    db.commit()


def save_analysis(
    db: Session,
    investigation: models.Investigation,
    *,
    findings: list[dict],
    risk: dict,
) -> models.Investigation:
    investigation.analysis_findings = findings
    investigation.risk_score = risk["score"]
    investigation.risk_label = risk["label"]
    investigation.risk_reasons = risk["reasons"]
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    return get_investigation(db, investigation.id) or investigation

