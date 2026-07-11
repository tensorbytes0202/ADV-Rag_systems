import os
from app.core.logger import logger
from app.core.settings import settings

UPLOAD_DIR=settings.RAW_DATA_PATH

os.makedirs(UPLOAD_DIR,exist_ok=True)

def save_pdf(file):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())

    logger.info(f"PDF Saved: {file.filename}")

    return file_path