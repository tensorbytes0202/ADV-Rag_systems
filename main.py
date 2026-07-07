from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.api.pdf_preview import router as pdf_router
from app.api import query_stream
app = FastAPI(
    title="Advanced RAG System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(upload_router)
app.include_router(query_router)
app.include_router(pdf_router)
app.include_router(query_stream.router)


@app.get("/")
def home():

    return {
        "status": "running",
        "message": "RAG System Active"
    }