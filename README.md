# Stat Tutor AI

StatTutor AI is an AI-powered statistics tutor that explains concepts, generates practice problems, and evaluates student answers using large language models.

The system includes a FastAPI backend, a Streamlit user interface, and is deployed publicly using Docker and Render.

## Live Demo

You can try the deployed tutor here:

https://stat-tutor-ai.onrender.com/

## Features

- 📘 Concept explanation for statistics topics
- 🧠 Practice question generation
- ✅ Answer evaluation with feedback
- 💻 Interactive Streamlit interface
- ⚡ FastAPI backend for LLM interactions
- 🐳 Dockerized deployment

## System Architecture

1. **Streamlit UI**
   - Provides an interactive interface for learning, practicing, and evaluating answers.

2. **FastAPI Backend**
   - Handles requests from the UI.
   - Manages prompt construction and LLM interaction.

3. **Groq API**
   - Generates explanations, practice questions, and evaluation feedback.

## Project Structure

```
stat-tutor-ai/
├── Dockerfile
├── README.md
├── frontend.py
├── requirements.txt
└── app/
    ├── __init__.py
    ├── llm.py
    ├── main.py
    ├── prompts.py
    ├── routes.py
    ├── schemas.py
    └── utils.py
```

## Deployment

The application is containerized using Docker and deployed on Render.

Deployment pipeline:

Local development → GitHub → Render → Docker container → Live application



## Limitations

- The tutor may respond to non-statistics questions because LLMs are trained as general-purpose assistants.
- Numerical answer evaluation may occasionally be inconsistent due to probabilistic reasoning in large language models.
- Some explanations may be overly verbose.

## Future Improvements

- Add domain guardrails to restrict non-statistics questions.
- Implement deterministic numeric validation for mathematical problems.
- Add student progress tracking.
- Improve explanation formatting.

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- OpenAI or other LLM provider (API-based)
- Docker (containerization)
- Render

## Reflections

This repo demonstrates small-scale tutoring app architecture with clear separation of endpoint logic, prompt engineering, and execution flow. It is a strong foundation for scaling to a more robust personalized statistics learning platform.
