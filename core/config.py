from pathlib import Path

# Folder of this file (core/)
BASE_DIR = Path(__file__).resolve().parent

# Folder where uploaded files are stored: core/uploads
# (always the same place, no matter where uvicorn is started)
UPLOAD_DIR = BASE_DIR / "uploads"

# Allowed MIME types (sent by the client, so it can be faked; we also check magic bytes)
ALLOWED_TYPES = {"image/jpeg", "image/png"}

# Maximum allowed size: 2 MB
MAX_SIZE = 2 * 1024 * 1024
