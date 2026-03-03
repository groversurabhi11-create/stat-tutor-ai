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


def handle_llm_error(exc: Exception) -> dict:
    """Convert an arbitrary exception into a simple error dict.

    The caller can include the returned value in a JSON response body.
    This keeps the API from raising HTTPException so that every route
    can return the same {success,data,error} envelope.
    """
    return {"error": str(exc)}
