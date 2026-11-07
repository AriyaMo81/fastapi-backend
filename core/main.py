from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from core.config import UPLOAD_DIR
from core.database import names_db
from core.routers import names, uploads


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP: runs once, before the app receives requests ----
    UPLOAD_DIR.mkdir(exist_ok=True)  # create the uploads folder if missing
    print("Startup: uploads folder is ready")

    yield  # the app runs while we are paused here

    # ---- SHUTDOWN: runs once, after the app stops receiving requests ----
    print(f"Shutdown: names_db had {len(names_db)} items (in-memory data is lost now)")


app = FastAPI(lifespan=lifespan)

# Attach the routers to the app
app.include_router(names.router)
app.include_router(uploads.router)


@app.get("/")
def say_hello():
    # Simple health-check style endpoint
    return JSONResponse(
        content={"message": "hello from fast api!"},
        status_code=status.HTTP_200_OK,
    )
