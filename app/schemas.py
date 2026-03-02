from pydantic import BaseModel


class ExplainRequest(BaseModel):
    topic: str


class PracticeRequest(BaseModel):
    topic: str
    difficulty: str  # e.g. "easy", "medium", "hard"


class EvaluateRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: str
