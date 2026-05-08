from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def is_image_file(file_name: str, content_type: str | None = None) -> bool:
    suffix = Path(file_name).suffix.lower()
    return suffix in IMAGE_EXTENSIONS or bool(content_type and content_type.startswith("image/"))


def inspect_image_metadata(
    path: Path,
    file_name: str,
    content_type: str,
    file_size: int,
    evidence_id: int | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    metadata: dict[str, Any] = {
        "file_name": file_name,
        "file_size": file_size,
        "mime_type": content_type,
    }
    findings: list[dict[str, Any]] = []

    if not is_image_file(file_name, content_type):
        findings.append(
            {
                "module": "image_metadata",
                "title": "Image metadata check skipped",
                "severity": "info",
                "explanation": "This evidence item is not an image supported by the MVP image metadata checker.",
                "evidence_id": evidence_id,
                "score_delta": 0,
                "details": {"file_name": file_name},
            }
        )
        return metadata, findings

    try:
        with Image.open(path) as image:
            metadata.update(
                {
                    "format": image.format,
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                }
            )
            exif = image.getexif()
            if exif and len(exif) > 0:
                metadata["exif_available"] = True
                metadata["exif_tag_count"] = len(exif)
                findings.append(
                    {
                        "module": "image_metadata",
                        "title": "EXIF metadata present",
                        "severity": "info",
                        "explanation": "The image contains EXIF metadata. Review the original file and context before drawing conclusions.",
                        "evidence_id": evidence_id,
                        "score_delta": 0,
                        "details": {"exif_tag_count": len(exif)},
                    }
                )
            else:
                metadata["exif_available"] = False
                metadata["exif_tag_count"] = 0
                findings.append(
                    {
                        "module": "image_metadata",
                        "title": "No EXIF metadata available",
                        "severity": "info",
                        "explanation": "No EXIF metadata available. This is common for screenshots, social platforms, and compressed images and is not evidence of manipulation by itself.",
                        "evidence_id": evidence_id,
                        "score_delta": 0,
                        "details": {"exif_available": False},
                    }
                )
    except (UnidentifiedImageError, OSError) as exc:
        findings.append(
            {
                "module": "image_metadata",
                "title": "Image metadata could not be read",
                "severity": "low",
                "explanation": "The file appears to be an image, but its metadata could not be read by the local parser.",
                "evidence_id": evidence_id,
                "score_delta": 0,
                "details": {"error": str(exc)},
            }
        )

    return metadata, findings

