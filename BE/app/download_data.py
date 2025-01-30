import requests
import os
from dotenv import load_dotenv
from app.exceptions.DataLoadException import DataLoadException

load_dotenv()

CSV_URL = os.getenv("JEOPARDY_DATA_URL")

DATA_DIR = "data"
CSV_FILE_PATH = os.path.join(DATA_DIR, "jeopardy_questions.csv")


def download_csv():
    """Used for downloading initial data from Jeopardy"""
    if os.path.exists(CSV_FILE_PATH) and os.path.getsize(CSV_FILE_PATH) > 0:
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    response = requests.get(CSV_URL)

    if response.status_code == 200:
        with open(CSV_FILE_PATH, "w") as csv_data:
            csv_data.writelines(response.content.decode())
    else:
        raise DataLoadException("Could not load initial data")


if __name__ == "__main__":
    download_csv()
