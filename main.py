from fastapi import FastAPI
from app.api.upload import router

app = FastAPI(
    title="Advanced RAG System",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "RAG System Active"
    }