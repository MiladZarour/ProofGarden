from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.analysis.image_metadata import inspect_image_metadata, is_image_file
from app.analysis.risk_score import calculate_risk_score
from app.analysis.text_patterns import analyze_text_patterns
from app.database import get_db


router = APIRouter(prefix="/investigations", tags=["investigations"])


def _get_or_404(db: Session, investigation_id: int) -> models.Investigation:
    investigation = crud.get_investigation(db, investigation_id)
    if not investigation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investigation not found")
    return investigation


@router.get("", response_model=list[schemas.InvestigationRead])
def list_investigations(db: Session = Depends(get_db)) -> list[models.Investigation]:
    return crud.list_investigations(db)


@router.post("", response_model=schemas.InvestigationRead, status_code=status.HTTP_201_CREATED)
def create_investigation(
    payload: schemas.InvestigationCreate, db: Session = Depends(get_db)
) -> models.Investigation:
    return crud.create_investigation(db, payload)


@router.get("/{investigation_id}", response_model=schemas.InvestigationRead)
def get_investigation(investigation_id: int, db: Session = Depends(get_db)) -> models.Investigation:
    return _get_or_404(db, investigation_id)


@router.put("/{investigation_id}", response_model=schemas.InvestigationRead)
def update_investigation(
    investigation_id: int,
    payload: schemas.InvestigationUpdate,
    db: Session = Depends(get_db),
) -> models.Investigation:
    investigation = _get_or_404(db, investigation_id)
    return crud.update_investigation(db, investigation, payload)


@router.delete("/{investigation_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_investigation(investigation_id: int, db: Session = Depends(get_db)) -> Response:
    investigation = _get_or_404(db, investigation_id)
    crud.delete_investigation(db, investigation)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{investigation_id}/analyze", response_model=schemas.AnalyzeResponse)
def analyze_investigation(investigation_id: int, db: Session = Depends(get_db)) -> schemas.AnalyzeResponse:
    investigation = _get_or_404(db, investigation_id)
    findings: list[dict] = []

    investigation_text = "\n\n".join(
        part
        for part in [
            investigation.title,
            investigation.claim,
            investigation.description or "",
            investigation.source_url or "",
        ]
        if part
    )
    findings.extend(analyze_text_patterns(investigation_text, "investigation fields"))

    for item in investigation.evidence_items:
        path = Path(item.file_path)
        if path.exists() and is_image_file(item.file_name, item.content_type):
            metadata, image_findings = inspect_image_metadata(
                path,
                item.file_name,
                item.content_type,
                item.file_size,
                evidence_id=item.id,
            )
            item.metadata_json = {**item.metadata_json, **metadata}
            item.analysis_findings = image_findings
            db.add(item)
            findings.extend(image_findings)
        elif item.analysis_findings:
            findings.extend(item.analysis_findings)

        if item.extracted_text:
            findings.extend(analyze_text_patterns(item.extracted_text, f"uploaded text file {item.file_name}", item.id))

    risk = calculate_risk_score(
        source_url=investigation.source_url,
        notes=investigation.notes,
        findings=findings,
    )
    saved = crud.save_analysis(db, investigation, findings=findings, risk=risk)
    return schemas.AnalyzeResponse(investigation=saved, findings=findings, risk=risk)
