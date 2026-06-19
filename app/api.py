from fastapi import FastAPI, UploadFile, File
from .rag import (
                    upload_document, 
                    summarize_document, 
                    ask_question, 
                    ask_question_in_document,
                    get_documents
                )
from .schemas import (
    ChatRequest,
    SummaryRequest
)
import os

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

app = FastAPI()

@app.post("/upload")
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

@app.post("/chat")
def chat(
    request: ChatRequest
):

    try:

        if request.document:

            answer = (
                ask_question_in_document(
                    request.question,
                    request.document
                )
            )

        else:

            answer = (
                ask_question(
                    request.question
                )
            )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

@app.get("/documents")
def documents():

    return {
        "documents": get_documents()
    }

@app.post("/summarize")
def summarize(
    request: SummaryRequest
):

    try:

        summary = (
            summarize_document(
                request.filename
            )
        )

        return {
            "success": True,
            "summary": summary
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

@app.get("/")
def home():
    return {
        "message": "PDF ChatBot  API Running"
    }

