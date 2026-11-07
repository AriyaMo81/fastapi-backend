# fastapi-backend

Projects from the FastAPI service design course: REST APIs, SQLAlchemy,
Alembic, JWT auth, PyTest, Docker, Celery, and CI/CD.

## Current progress

- [x] REST API basics: path, query, and JSON body validation
- [x] CRUD endpoints (`/names`)
- [x] File upload (`UploadFile` and `bytes`) with validation
- [x] Modular structure with `APIRouter` and `lifespan`
- [ ] SQLAlchemy
- [ ] Alembic migrations
- [ ] JWT authentication
- [ ] PyTest
- [ ] Docker
- [ ] Celery
- [ ] CI/CD

## Project structure

```
core/
├── main.py          # app, lifespan, routers
├── config.py        # settings (upload dir, max size, allowed types)
├── database.py      # in-memory data (temporary)
├── dependencies.py  # reusable validated params
├── routers/
│   ├── names.py     # /names endpoints
│   └── uploads.py   # /upload endpoints
└── services/
    └── file_service.py  # upload validation and saving
```

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install fastapi uvicorn python-multipart

# 3. Run the server (from the project root, outside `core/`)
uvicorn core.main:app --reload --reload-exclude "core/uploads"
```

Then open http://127.0.0.1:8000/docs for the interactive API docs.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/names` | List names (optional `?q=` search) |
| GET | `/names/{id}` | Get one name |
| POST | `/names` | Create a name (`{"name": "reza"}`) |
| PUT | `/names/{id}` | Update a name |
| DELETE | `/names/{id}` | Delete a name |
| POST | `/upload` | Upload a JPEG/PNG (max 2 MB) |

## Notes

- Data is stored in memory and resets on restart (a database comes later).
- Uploaded files are saved in `core/uploads/` (ignored by git).