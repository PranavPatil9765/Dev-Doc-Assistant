# FastAPI entry point
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dev Doc Assistant API!"}