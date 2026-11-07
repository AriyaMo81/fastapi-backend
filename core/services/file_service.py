from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, status

from core.config import MAX_SIZE, UPLOAD_DIR


def validate_and_save(content: bytes, filename: str | None) -> dict:
    # 1. Validate the size
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File is too large (max 2 MB)",
        )

    # 2. Validate that the file is not empty
    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty",
        )

    # 3. Check magic bytes (the real file signature), not just the client's content_type
    is_jpeg = content.startswith(b"\xff\xd8\xff")
    is_png = content.startswith(b"\x89PNG")
    if not (is_jpeg or is_png):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG and PNG images are allowed",
        )

    # 4. Build a unique, safe filename.
    # Path(...).name strips directories (prevents path traversal like "../../x"),
    # uuid4 prevents overwriting files that have the same name.
    original_name = Path(filename or "file").name
    unique_name = f"{uuid4().hex}_{original_name}"

    # 5. Save the file to disk
    # Re-create the folder in case it was deleted while the server was running
    UPLOAD_DIR.mkdir(exist_ok=True)
    (UPLOAD_DIR / unique_name).write_bytes(content)

    return {
        "original_name": original_name,
        "saved_as": unique_name,
        "size_bytes": len(content),
    }
