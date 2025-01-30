import subprocess

from fastapi import FastAPI

app = FastAPI()


def run_migrations():
    """Run Alembic migrations automatically at startup."""
    subprocess.run(["alembic", "upgrade", "head"])


@app.on_event("startup")
def startup_event():
    run_migrations()


@app.get("/")
def read_root():
    return {"message": "Welcome to my game"}