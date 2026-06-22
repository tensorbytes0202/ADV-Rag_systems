from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import save_pdf
from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_chunks
from app.services.embedding_service import generate_embeddings

from app.services.vector_store import (
    create_collection,
    store_embeddings
)

from app.services.chunk_store import (
    save_chunks
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = save_pdf(file)

    pdf_data = extract_pdf_data(
        file_path
    )

    chunks = []

    print(
        "Total Pages:",
        len(pdf_data["pages"])
    )

    for page in pdf_data["pages"]:

        page_text = page["text"]

        page_chunks = create_chunks(
            page_text
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page": page["page_number"],
                "document": file.filename
            })

    print(
        "Total Chunks:",
        len(chunks)
    )

    save_chunks(
        chunks
    )

    embeddings = generate_embeddings(
        [
            chunk["text"]
            for chunk in chunks
        ]
    )

    print(
        "Total Embeddings:",
        len(embeddings)
    )

    create_collection()

    store_embeddings(
        chunks,
        embeddings,
        file.filename
    )

    return {
        "filename": file.filename,
        "pages": pdf_data["total_pages"],
        "total_chunks": len(chunks),
        "vectors_stored": len(embeddings)
    }