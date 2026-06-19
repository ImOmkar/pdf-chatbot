import os
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from rag import (
    process_pdf,
    ask_question
)

from models import ChatRequest

app = FastAPI(
    title="PDF Chatbot API"
)

os.makedirs(
    "uploads",
    exist_ok=True
)

@app.get("/")
def home():

    return {
        "message":
        "PDF Chatbot Running"
    }


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = (
        f"uploads/{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = process_pdf(
        file_path
    )

    return {
        "message":
        "PDF processed successfully",

        "details":
        result
    }


@app.post("/chat")
def chat(
    request: ChatRequest
):

    result = ask_question(
        request.question
    )

    return result.get("answer", "got some issues....")