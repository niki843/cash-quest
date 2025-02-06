import os
import subprocess
import openai
from dotenv import load_dotenv

from fastapi import FastAPI, Query, HTTPException

from load_data import load_data
from models.Base import SessionLocal
from models.Questions import Questions
from pydantic_models.Answer import Answer

from sqlalchemy import func


app = FastAPI()

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


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
        Questions.round == round,
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


def compare_answers_with_gpt(correct_answer: str, user_answer: str) -> bool:
    prompt = f"Is the user's answer '{user_answer}' mean the same as this answer: '{correct_answer}'?"

    try:
        response = openai.Completion.create(
            engine="gpt-",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the response from OpenAI's API
        gpt_answer = response.choices[0].text.strip()

        # If GPT thinks the answer is correct, we consider it true
        if "yes" in gpt_answer.lower():
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error with GPT API: " + str(e))


@app.post("/verify-answer/")
async def verify_answer(answer: Answer):
    db = SessionLocal()

    # Retrieve the question from the database using the question_id
    question = db.query(Questions).filter(Questions.id == answer.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    does_answer_match = compare_answers_with_gpt(question.answer, answer.user_answer)

    # Check if the user's answer is correct
    is_correct = True if does_answer_match else False

    # Return a response with the result
    return {"correct": is_correct, "question": question.question, "user_answer": answer.user_answer}
