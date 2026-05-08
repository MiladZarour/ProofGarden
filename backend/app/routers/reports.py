from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.investigations import _get_or_404
from app.utils.report_markdown import generate_markdown_report


router = APIRouter(prefix="/investigations", tags=["reports"])


@router.get("/{investigation_id}/report.md")
def markdown_report(investigation_id: int, db: Session = Depends(get_db)) -> Response:
    investigation = _get_or_404(db, investigation_id)
    markdown = generate_markdown_report(investigation)
    filename = f"proofgarden-investigation-{investigation.id}.md"
    return Response(
        content=markdown,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

