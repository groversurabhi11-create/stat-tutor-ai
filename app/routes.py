from fastapi import APIRouter, HTTPException

from . import llm, utils
from .schemas import ExplainRequest, PracticeRequest, EvaluateRequest

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


@router.post("/explain")
def explain_topic(request: ExplainRequest):
    try:
        explanation = llm.explain(request.topic)
        return {"explanation": explanation}
    except Exception as exc:
        raise utils.handle_llm_error(exc)


@router.post("/practice")
def practice_topic(request: PracticeRequest):
    try:
        problem = llm.practice(request.topic, request.difficulty)
        return {"problem": problem}
    except Exception as exc:
        raise utils.handle_llm_error(exc)


@router.post("/evaluate")
def evaluate_topic(request: EvaluateRequest):
    try:
        raw = llm.evaluate(request.question, request.student_answer, request.correct_answer)
        evaluation = utils.parse_json_safe(raw)
        return {"evaluation": evaluation}
    except Exception as exc:
        raise utils.handle_llm_error(exc)
