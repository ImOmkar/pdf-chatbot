from fastapi import APIRouter, File, UploadFile
from app.services.rag_service import (
                    upload_document, 
                )
import os

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

router = APIRouter()

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = (
        os.path.join(
            UPLOAD_DIR,
            file.filename
        )
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    chunk_count = (
        upload_document(
            file_path
        )
    )

    return {
        "success": True,
        "filename": file.filename,
        "chunks": chunk_count
    }

