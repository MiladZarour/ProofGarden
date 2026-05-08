from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.routers.investigations import _get_or_404


router = APIRouter(tags=["evidence"])


@router.get("/investigations/{investigation_id}/evidence", response_model=list[schemas.EvidenceRead])
def list_evidence(investigation_id: int, db: Session = Depends(get_db)) -> list[models.EvidenceItem]:
    _get_or_404(db, investigation_id)
    return crud.list_evidence(db, investigation_id)


@router.post(
    "/investigations/{investigation_id}/notes",
    response_model=schemas.EvidenceNoteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    investigation_id: int,
    payload: schemas.EvidenceNoteCreate,
    db: Session = Depends(get_db),
) -> models.EvidenceNote:
    _get_or_404(db, investigation_id)
    return crud.create_note(db, investigation_id, payload)


@router.get("/investigations/{investigation_id}/notes", response_model=list[schemas.EvidenceNoteRead])
def list_notes(investigation_id: int, db: Session = Depends(get_db)) -> list[models.EvidenceNote]:
    _get_or_404(db, investigation_id)
    return crud.list_notes(db, investigation_id)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence note not found")
    crud.delete_note(db, note)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
