from typing import Annotated

from fastapi import Body, Path, Query

# Path param (int): the ID of a name, must be between 1 and 10000
NameId = Annotated[
    int,
    Path(
        ge=1,  # greater than or equal to 1
        le=10_000,  # less than or equal to 10000
        title="Name ID",
        description="Unique identifier, positive integer (1 to 10000)",
        examples=[1, 2, 3],
    ),
]

# Path param (str): an exact name to look up, English letters only
NamePath = Annotated[
    str,
    Path(
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",  # regex: only English letters
        title="Name",
        description="Exact name to look up (English letters only)",
        examples=["ali"],
    ),
]

# Path param (int): zero-based index of a character inside a name
CharIndex = Annotated[
    int,
    Path(
        ge=0,  # first character is at index 0
        lt=50,  # strictly less than 50
        title="Character index",
        description="Zero-based position of a character in the name (0 to 49)",
        examples=[0],
    ),
]

# Query param (optional str): used for searching, e.g. /names?q=ali
SearchQuery = Annotated[
    str | None,
    Query(
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",
        title="Search name",
        description="Part of a name to search for (English letters only)",
        examples=["ali", "mary"],
    ),
]

# Body field (str): JSON body like {"name": "reza"}
# embed=True makes FastAPI expect a JSON object with the key "name"
NameBody = Annotated[
    str,
    Body(
        embed=True,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",
        title="Name",
        description="English letters only",
        examples=["reza"],
    ),
]
