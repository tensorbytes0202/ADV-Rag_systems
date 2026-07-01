from huggingface_hub.inference._generated.types import document_question_answering
from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import save_pdf
from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_parent_child_chunks
from app.services.embedding_service import generate_embeddings

from app.services.vector_store import (
    create_collection,
    store_embeddings
)

from app.services.chunk_store import (
    save_chunks,
    save_parent_chunks
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

    parents = []

    print(
    "Total Pages:",
    len(pdf_data["pages"])
)

    for page in pdf_data["pages"]:

        page_text = page["text"]

        parent_documents = create_parent_child_chunks(
        page_text
    )

        for parent in parent_documents:
            parent_unique_id = (
    f"{file.filename}_page_{page['page_number']}_parent_{parent['parent_id']}"
)

            parents.append({

                "parent_id": parent_unique_id,

                "parent_text": parent["parent_text"],

                "page": page["page_number"],

                "document": file.filename

})

            for child in parent["children"]:

                chunks.append({

                "text": child["text"],

                "page": page["page_number"],

                "document": file.filename,

                "parent_id": parent_unique_id,
                "parent_text": parent["parent_text"],

                "child_id": child["child_id"]

            })
  
    print(
        "Total Chunks:",
        len(chunks)
    )
    save_parent_chunks(parents)

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