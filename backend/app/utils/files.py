from __future__ import annotations

import hashlib
import mimetypes
import os
from pathlib import Path
import re
import shutil
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


DEFAULT_UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR = Path(os.getenv("PROOFGARDEN_UPLOAD_DIR", DEFAULT_UPLOAD_DIR)).resolve()
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".txt", ".eml"}
TEXT_EXTENSIONS = {".txt", ".eml"}


def ensure_upload_dir() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def safe_filename(file_name: str) -> str:
    cleaned = Path(file_name).name.strip() or "upload"
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", cleaned)
    return cleaned[:180] or "upload"


def validate_upload(file_name: str) -> None:
    extension = Path(file_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed extensions: {allowed}",
        )


def guess_content_type(file_name: str, provided: str | None) -> str:
    if provided and provided != "application/octet-stream":
        return provided
    guessed, _ = mimetypes.guess_type(file_name)
    return guessed or "application/octet-stream"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_text(path: Path, file_name: str) -> str | None:
    if Path(file_name).suffix.lower() not in TEXT_EXTENSIONS:
        return None
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return None


def save_upload(file: UploadFile, investigation_id: int) -> dict:
    ensure_upload_dir()
    original_name = safe_filename(file.filename or "upload")
    validate_upload(original_name)

    stored_name = f"investigation-{investigation_id}-{uuid4().hex}-{original_name}"
    target_path = UPLOAD_DIR / stored_name
    with target_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = target_path.stat().st_size
    return {
        "file_name": original_name,
        "stored_name": stored_name,
        "file_path": str(target_path),
        "file_size": file_size,
        "content_type": guess_content_type(original_name, file.content_type),
        "sha256": file_sha256(target_path),
        "extracted_text": extract_text(target_path, original_name),
    }

