from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core.database import names_db
from core.dependencies import CharIndex, NameBody, NameId, NamePath, SearchQuery

# All routes in this file start with /names
router = APIRouter(prefix="/names", tags=["names"])


@router.get("")
def get_names(q: SearchQuery = None):
    # If a search term is given, return only names that contain it (case-insensitive)
    if q is not None:
        filtered = [n for n in names_db if q.lower() in n["name"].lower()]
        return JSONResponse(content=filtered, status_code=status.HTTP_200_OK)

    # Otherwise return everything
    return JSONResponse(content=names_db, status_code=status.HTTP_200_OK)


# NOTE: fixed paths like /by-name/... must be defined before /{name_id}
@router.get("/by-name/{name}")
def get_by_name(name: NamePath):
    # Exact match on the name (case-insensitive because we lowercase the input)
    matches = [n for n in names_db if n["name"] == name.lower()]

    # Validation (422) only checks the format; "not found" is our own logic
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Name not found"
        )
    return JSONResponse(content=matches, status_code=status.HTTP_200_OK)


@router.get("/{name_id}/char/{index}")
def get_char(name_id: NameId, index: CharIndex):
    # Two path params, each validated separately
    for n in names_db:
        if n["id"] == name_id:
            # Format is valid (0..49) but may still be beyond this name's length
            if index >= len(n["name"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Index out of range (name has {len(n['name'])} characters)",
                )
            return JSONResponse(
                content={"id": name_id, "index": index, "char": n["name"][index]},
                status_code=status.HTTP_200_OK,
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@router.get("/{name_id}")
def get_one_user(name_id: NameId):
    # Find a single record by its ID
    for n in names_db:
        if n["id"] == name_id:
            return JSONResponse(content=n, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@router.post("")
def create_user(name: NameBody):
    # `name` comes from the JSON body, e.g. {"name": "reza"}
    # New ID = current max ID + 1 (avoids duplicate IDs)
    new_id = max((n["id"] for n in names_db), default=0) + 1
    new_user = {"id": new_id, "name": name}
    names_db.append(new_user)

    # 201 Created: a new resource was made
    return JSONResponse(content=new_user, status_code=status.HTTP_201_CREATED)


@router.put("/{name_id}")
def update_user(name_id: NameId, name: NameBody):
    # `name_id` comes from the URL path, `name` comes from the JSON body
    for n in names_db:
        if n["id"] == name_id:
            n["name"] = name  # update the record in place
            return JSONResponse(content=n, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@router.delete("/{name_id}")
def delete_user(name_id: NameId):
    # DELETE has no body. We return 200 with a JSON message (204 must not have a body).
    for i, n in enumerate(names_db):
        if n["id"] == name_id:
            del names_db[i]
            return JSONResponse(
                content={"message": f"Name with ID {name_id} deleted successfully"},
                status_code=status.HTTP_200_OK,
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")
