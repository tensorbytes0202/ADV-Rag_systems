from fastapi import FastAPI

app = FastAPI(
    title="Production RAG System",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "RAG System Active"
    }