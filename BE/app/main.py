import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi import Query, HTTPException

from load_data import load_data
from models.Base import SessionLocal
from models.Questions import Questions
from pydantic_models.Answer import Answer

from sqlalchemy import func

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("API_KEY"))

app = FastAPI()


@app.on_event("startup")
def startup_event():
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


async def compare_answers_with_gpt(question: str, correct_answer: str, user_answer: str, retries=10) -> bool:
    lm_response_map = {
        "True": True,
        "False": False
    }
    gpt_answer = call_gpt(question, correct_answer, user_answer)
    while not lm_response_map.get(gpt_answer):
        retries -= 1
        # If GPT thinks the answer is correct, we consider it true
        gpt_answer = await call_gpt(question, correct_answer, user_answer)

        if retries < 0:
            raise HTTPException(status_code=422, detail="Could not compare answer")

    return lm_response_map.get(gpt_answer)


async def call_gpt(question: str, correct_answer: str, user_answer: str):
    prompt = f"""
            I want you to answer with only True or False. Based on the question '{question}'
            Does the user's answer '{user_answer}' mean the same as the correct answer: '{correct_answer}'?
        """

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Extract the response from OpenAI's API
        return response.choices[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error with GPT API" + str(e))


@app.post("/verify-answer/")
async def verify_answer(answer: Answer):
    db = SessionLocal()

    # Retrieve the question from the database using the question_id
    question = db.query(Questions).filter(Questions.id == answer.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    does_answer_match = await compare_answers_with_gpt(question.value, question.answer, answer.user_answer)

    # Return a response with the result
    return {"correct": does_answer_match, "question": question.question, "user_answer": answer.user_answer}
