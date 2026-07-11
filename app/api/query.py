from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.query_service import process_query


router = APIRouter()


# ==========================================================
# Request Model
# ==========================================================

class QueryRequest(BaseModel):

    question: str

    documents: List[str] = []


# ==========================================================
# Query Endpoint
# ==========================================================

@router.post("/query")
def query_document(request: QueryRequest):

    return process_query(
        request.question
    )