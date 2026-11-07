from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from core.config import ALLOWED_TYPES, MAX_SIZE
from core.services.file_service import validate_and_save

router = APIRouter(tags=["uploads"])


# Option 1: UploadFile (recommended). Large files are spooled to disk, not held in RAM.
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check the declared type first (cheap check before reading the file)
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG and PNG images are allowed",
        )

    # Read at most MAX_SIZE + 1 bytes, so an oversized file is detected
    # without loading the whole thing into memory
    content = await file.read(MAX_SIZE + 1)

    result = validate_and_save(content, file.filename)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


# Option 2: File as bytes. The whole file is loaded into RAM, so use it for small files only.
# There is no filename here, because we only receive raw bytes.
@router.post("/upload-bytes")
async def upload_bytes(file: bytes = File(...)):
    result = validate_and_save(file, None)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
