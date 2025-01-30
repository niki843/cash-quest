import pandas as pd
from sqlalchemy.orm import declarative_base

from models.Questions import Questions
from models.Base import SessionLocal

CSV_FILE_PATH = "data/jeopardy_questions.csv"

Base = declarative_base()


def load_data():
    """Load CSV data into the database."""

    db = SessionLocal()

    if db.query(Questions.id).first() is not None:
        return

    df = pd.read_csv(CSV_FILE_PATH)
    for index, row in df.iterrows():
        row_price = int(row[4].replace('$', '').replace(',', '')) if isinstance(row[4], str) else 0
        question = Questions(
            category=row[3],
            value=row_price,
            question=row[5],
            answer=row[6]
        )
        db.add(question)

    db.commit()
    db.close()
    print("✅ Data loaded into the database.")


if __name__ == "__main__":
    load_data()
