from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import save_pdf
from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_chunks
from app.services.embedding_service import generate_embeddings

from app.services.vector_store import (
    create_collection,
    store_embeddings
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = save_pdf(file)

    pdf_data = extract_pdf_data(file_path)

    full_text = ""

    for page in pdf_data["pages"]:
        full_text += page["text"] + "\n"

    chunks = create_chunks(full_text)

    print("Total Chunks:", len(chunks))

    embeddings = generate_embeddings(chunks)

    print("Total Embeddings:", len(embeddings))

    create_collection()

    store_embeddings(
        chunks,
        embeddings
    )

    return {
        "filename": file.filename,
        "pages": pdf_data["total_pages"],
        "total_chunks": len(chunks),
        "vectors_stored": len(embeddings)
    }