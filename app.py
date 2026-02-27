# Create a minimal FastAPI app with a root endpoint that returns a welcome message

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import uvicorn
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# Create a Pydantic Model called ExplainRequest which takes a single field called topic which is a string.
from pydantic import BaseModel
class ExplainRequest(BaseModel):
    topic: str

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
                "content": """
            You are an expert statistics tutor.

            Always respond strictly in the following format:

            Definition:
            (Provide a clear and precise definition.)

            Intuition:
            (Explain the intuition in simple language.)

            Example:
            (Give one small numerical example if applicable.)

            Do not add extra sections.
            Do not add conclusions.
            Do not add key takeaways.
            Keep explanations concise and clear.
            """
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