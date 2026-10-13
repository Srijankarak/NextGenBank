from fastapi import FastAPI

app = FastAPI(
    title="NextGenBank - FastAPI",
    description="A fully featured banking API built with FastAPI.",
)


@app.get("/")
def home():
    return {"message": "Welcome to NextGenBank API"}
