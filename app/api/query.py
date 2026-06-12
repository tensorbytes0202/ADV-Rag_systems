from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.vector_store import (
    search_similar_chunks
)

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_document(
    request: QueryRequest
):

    query_embedding = generate_query_embedding(
        request.question
    )

    results = search_similar_chunks(
        query_embedding,
        limit=5
    )

    response = []

    for result in results:

        response.append({
            "score": result.score,
            "text": result.payload.get(
                "text",
                ""
            )
        })

    return {
        "question": request.question,
        "results": response
    }