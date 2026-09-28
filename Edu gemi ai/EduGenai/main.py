from pathlib import Path
from typing import Literal

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="AI Powered Learning Assistant",
    version="1.0.0",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR/ "static"),
    name="static",
)


# --------------------------------------------------
#---------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"


class QuizRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


# --------------------------------------------------
# Frontend
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    html_file = BASE_DIR / "templates" / "index.html"

    html = html_file.read_text(
        encoding="utf-8"
    )

    return HTMLResponse(html)


# --------------------------------------------------
# Explain Topic
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    result = await explain_topic(
        payload.text
    )

    return {
        "task": "explain",
        "result": result
    }


# --------------------------------------------------
# Question & Answer
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    result = await answer_question(
        payload.text
    )

    return {
        "task": "qa",
        "result": result
    }


# --------------------------------------------------
# Summarization
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    result = await summarize_text(
        payload.text
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    result = await generate_quiz(
        payload.topic,
        payload.count
    )

    return {
        "task": "quiz",
        "result": result
    }


# --------------------------------------------------
# Prerequisites
# --------------------------------------------------

@app.post("/prerequisites")
async def prerequisites(payload: TextRequest):

    result = await recommend_learning_path(
        payload.text,
        "beginner"
    )

    return {
        "task": "prerequisites",
        "result": result
    }


# --------------------------------------------------
# Personalized Learning Path
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: LearningRequest
):

    result = await recommend_learning_path(
        payload.topic,
        payload.level
    )

    return {
        "task": "learn/recommendations",
        "result": result
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }