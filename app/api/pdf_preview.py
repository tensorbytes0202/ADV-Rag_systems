from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("data/raw")


@router.get("/pdf/{filename}")
def get_pdf(filename: str):

    print("=" * 60)
    print("REQUESTED FILE :", filename)

    pdf_path = UPLOAD_DIR / filename

    print("FULL PATH :", pdf_path)
    print("EXISTS :", pdf_path.exists())
    print("=" * 60)

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF not found."
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf"
    )