from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.analysis.image_metadata import inspect_image_metadata
from app.database import get_db
from app.routers.investigations import _get_or_404
from app.utils.files import save_upload


router = APIRouter(prefix="/investigations", tags=["uploads"])


@router.post("/{investigation_id}/upload", response_model=schemas.EvidenceRead, status_code=status.HTTP_201_CREATED)
def upload_evidence(
    investigation_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> models.EvidenceItem:
    _get_or_404(db, investigation_id)
    saved = save_upload(file, investigation_id)
    metadata, findings = inspect_image_metadata(
        Path(saved["file_path"]),
        saved["file_name"],
        saved["content_type"],
        saved["file_size"],
    )
    return crud.create_evidence_item(
        db,
        investigation_id=investigation_id,
        file_name=saved["file_name"],
        stored_name=saved["stored_name"],
        content_type=saved["content_type"],
        file_size=saved["file_size"],
        file_path=saved["file_path"],
        sha256=saved["sha256"],
        extracted_text=saved["extracted_text"],
        metadata_json=metadata,
        analysis_findings=findings,
    )

