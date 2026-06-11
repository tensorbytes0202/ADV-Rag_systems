from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import save_pdf
from app.services.pdf_extractor import extract_pdf_data
from app.services.chunker import create_chunks
from app.services.embedding_service import generate_embeddings

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Save PDF
    file_path = save_pdf(file)

    # Extract PDF Data
    pdf_data = extract_pdf_data(file_path)

    # Combine all pages text
    full_text = ""

    for page in pdf_data["pages"]:
        full_text += page["text"] + "\n"

    # Create Chunks
    chunks = create_chunks(full_text)

    # Generate Embeddings
    embeddings = generate_embeddings(chunks)

    return {
        "filename": file.filename,
        "pages": pdf_data["total_pages"],
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "sample_chunk": chunks[0][:200] if chunks else ""
    }