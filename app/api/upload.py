from app.services.document_registry import is_document_indexed
from huggingface_hub.inference._generated.types import document_question_answering
from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import save_pdf
from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_parent_child_chunks
from app.services.embedding_service import generate_embeddings
from app.services.document_registry import (
    is_document_indexed,
    register_document
)

from app.services.vector_store import (
    create_collection,
    store_embeddings
)


from app.services.document_registry import (

    is_document_indexed,

    register_document,

    is_collection_available

)

from app.services.document_registry import (
    set_active_document,
    get_active_document
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):  # ======================================
    # Check if already indexed
    # ======================================

    if (

    is_document_indexed(file.filename)

    and

    is_collection_available()

):

        print("=" * 60)
        print("DOCUMENT ALREADY INDEXED")
        print("Skipping Embedding Generation")
        print(file.filename)
        print("=" * 60)

        return {

        "filename": file.filename,

        "message": "Document already indexed.",

        "already_indexed": True

    }

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
    register_document(

    file.filename,

    pdf_data["total_pages"],

    len(chunks)

)

    return {
        "filename": file.filename,
        "pages": pdf_data["total_pages"],
        "total_chunks": len(chunks),
        "vectors_stored": len(embeddings)
    }

@router.get("/documents")
def list_documents():

    from app.services.document_registry import (
    get_documents
    )

    return {

    "documents": get_documents()

    }

@router.post("/documents/active/{document_name}")
def select_document(
    document_name: str
):

    set_active_document(document_name)

    return {

        "message": "Active document updated.",

        "active_document": document_name

    }

@router.get("/documents/active")
def active_document():

    return {

        "active_document": get_active_document()

    }