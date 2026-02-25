# Create a minimal FastAPI app with a root endpoint that returns a welcome message

from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# Create a Pydantic Model called ExplainRequest which takes a single field called topic which is a string.
from pydantic import BaseModel
class ExplainRequest(BaseModel):
    topic: str

# Create a POST endpoint called /explain which takes an ExplainRequest as input and returns a message that says "The topic you want to learn about is: {topic}" where {topic} is the value of the topic field in the ExplainRequest.
@app.post("/explain")
def explain_topic(request: ExplainRequest):
    return {"message": f"The topic you want to learn about is: {request.topic}"}

# I want to test this app using uvicorn. How do I run this app using uvicorn?
