from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.pdf_service import save_pdf

router = APIRouter()

@router.post("/upload")

async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = save_pdf(file)

    return {
        "status": "success",
        "filename": file.filename,
        "path": file_path
    }