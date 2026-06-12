from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.query import router as query_router
app = FastAPI(
    title="Advanced RAG System",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(query_router)
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "RAG System Active"
    }