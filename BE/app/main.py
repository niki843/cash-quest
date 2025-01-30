import subprocess

from fastapi import FastAPI, Query

from load_data import load_data
from models.Base import SessionLocal
from models.Questions import Questions

from sqlalchemy import func

app = FastAPI()


def run_migrations():
    """Run Alembic migrations automatically at startup."""
    subprocess.run(["alembic", "upgrade", "head"])


@app.on_event("startup")
def startup_event():
    run_migrations()
    load_data()


@app.get("/")
def read_root():
    return {"message": "Welcome to my game"}


@app.get("/question/")
async def get_question(round: str = Query(...), value: str = Query(...)):
    # Clean value, removing any "$" sign and converting to integer
    value_int = int(value.replace("$", "").replace(",", ""))

    db = SessionLocal()

    # Query the database for a question with the provided category and value
    question = db.query(Questions).filter(
        Questions.category == round,
        Questions.value == value_int
    ).order_by(func.random()).first()

    if question:
        return {
            "id": question.id,
            "category": question.category,
            "value": question.value,
            "question": question.question,
            "answer": question.answer
        }
    else:
        return {"message": "Question not found for the given round and value."}