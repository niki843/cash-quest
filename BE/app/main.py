import subprocess

from fastapi import FastAPI

from load_data import load_data

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