import os
from dotenv import load_dotenv
from openai import OpenAI

from .prompts import (
    EXPLAIN_SYSTEM_PROMPT,
    PRACTICE_SYSTEM_PROMPT,
    EVALUATE_SYSTEM_PROMPT,
)

# load environment before we create the client so that GROQ_API_KEY is available
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


# helpers that encapsulate the chat completion calls


# internal helpers -----------------------------------------------------------

def _llm_call(callable_, *args, **kwargs):
    """Invoke an LLM helper and convert any raised exception into a dict.

    Returning a dict with an ``error`` key lets the routes uniformly
    detect a failure without relying on exceptions.
    """
    try:
        return callable_(*args, **kwargs)
    except Exception as exc:  # pylint: disable=broad-except
        # we deliberately catch every exception type; the router will
        # translate the dict to the standard envelope.
        return {"error": str(exc)}


def explain(topic: str):
    def _do(topic: str):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
                {"role": "user", "content": f"Explain {topic}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    return _llm_call(_do, topic)


def practice(topic: str, difficulty: str):
    # difficulty guidelines are embedded in the prompt so the caller does not
    # need to remember them.
    def _do(topic: str, difficulty: str):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": PRACTICE_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Generate one {difficulty} practice problem on {topic}. \n"
                        "Difficulty guidelines:\n"
                        "- easy: basic definition or direct formula application\n"
                        "- medium: multi-step calculation or interpretation\n"
                        "- hard: conceptual reasoning or combined concepts\n"
                        "Follow the required format strictly."
                    ),
                },
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content

    return _llm_call(_do, topic, difficulty)


def evaluate(question: str, student_answer: str, correct_answer: str):
    def _do(question: str, student_answer: str, correct_answer: str):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": EVALUATE_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\n"
                        f"Student Answer: {student_answer}\n"
                        f"Correct Answer: {correct_answer}\n"
                    ),
                },
            ],
            temperature=0,
        )
        return response.choices[0].message.content

    return _llm_call(_do, question, student_answer, correct_answer)
