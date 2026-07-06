from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

PDF_FOLDER = "documents"


@router.get("/pdf/{document_name}")
def get_pdf(document_name: str):

    pdf_path = os.path.join(
        PDF_FOLDER,
        document_name
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf"
    )