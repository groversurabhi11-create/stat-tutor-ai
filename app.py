# Create a minimal FastAPI app with a root endpoint that returns a welcome message

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import EVALUATE_SYSTEM_PROMPT, EXPLAIN_SYSTEM_PROMPT, PRACTICE_SYSTEM_PROMPT
import uvicorn
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# Define separate Pydantic models for explain and practice requests.
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

# Load environment variables
load_dotenv()

# Initialize Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


@app.post("/explain")
def explain_topic(request: ExplainRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": EXPLAIN_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Explain {request.topic}"
            }
        ],
        temperature=0.3
    )

    return {
        "explanation": response.choices[0].message.content
    }

@app.post("/evaluate")
def evaluate_topic(request: EvaluateRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": EVALUATE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"Question: {request.question}\n"
                    f"Student Answer: {request.student_answer}"
                    f"Correct Answer: {request.correct_answer}\n"
                )
            }
        ],
        temperature=0
    )

    # parse JSON string so Swagger shows formatted output
    import json
    try:
        evaluation_json = json.loads(response.choices[0].message.content)
    except Exception:
        evaluation_json = {"raw": response.choices[0].message.content}

    return {
        "evaluation": evaluation_json
    }

@app.post("/practice")
def practice_topic(request: PracticeRequest):
    # include difficulty when asking the model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": PRACTICE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"""Generate one {request.difficulty} practice problem on {request.topic}. 
                    Difficulty guidelines:
                    - easy: basic definition or direct formula application
                    - medium: multi-step calculation or interpretation
                    - hard: conceptual reasoning or combined concepts
                    Follow the required format strictly."""
                )
            }
        ],
        temperature=0.4
    )

    return {
        "problem": response.choices[0].message.content
    }