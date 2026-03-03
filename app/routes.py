from fastapi import APIRouter

from . import llm, utils
from .schemas import ExplainRequest, PracticeRequest, EvaluateRequest

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


@router.post("/explain")
def explain_topic(request: ExplainRequest):
    # call through to the helper; if it returned a dict with an error key we
    # surface it rather than letting an exception propagate.
    result = llm.explain(request.topic)
    if isinstance(result, dict) and "error" in result:
        return {"success": False, "data": None, "error": result["error"]}

    return {"success": True, "data": {"explanation": result}, "error": None}


@router.post("/practice")
def practice_topic(request: PracticeRequest):
    result = llm.practice(request.topic, request.difficulty)
    if isinstance(result, dict) and "error" in result:
        return {"success": False, "data": None, "error": result["error"]}

    return {"success": True, "data": {"problem": result}, "error": None}


@router.post("/evaluate")
def evaluate_topic(request: EvaluateRequest):
    result = llm.evaluate(request.question, request.student_answer, request.correct_answer)
    if isinstance(result, dict) and "error" in result:
        return {"success": False, "data": None, "error": result["error"]}

    evaluation = utils.parse_json_safe(result)
    return {"success": True, "data": {"evaluation": evaluation}, "error": None}
