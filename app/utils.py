import json
from fastapi import HTTPException


def parse_json_safe(content: str):
    """Attempt to load a JSON string, otherwise return a wrapper dict.

    This mirrors the parsing logic formerly sitting inside the
    `/evaluate` endpoint and keeps the route lean.
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw": content}


def handle_llm_error(exc: Exception) -> HTTPException:
    """Convert an arbitrary exception into a 500-style HTTPException.

    Routes can raise the returned exception to keep error handling
    consistent.
    """
    return HTTPException(status_code=500, detail=str(exc))
