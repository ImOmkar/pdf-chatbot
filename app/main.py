from fastapi import FastAPI, UploadFile, File
from app.services.rag_service import (
                    upload_document, 
                    summarize_document, 
                    ask_question, 
                    ask_question_in_document,
                    get_documents
                )
from app.schemas.schemas import (
    ChatRequest,
    SummaryRequest
)

from app.services.chat_service import (
    get_sessions,
    get_session_messages,
    get_langchain_history,
    save_message,
    delete_session
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
        
        history = get_langchain_history(
            request.session_id
        )

        if request.document:

            answer = (
                ask_question_in_document(
                    request.question,
                    request.document
                )
            )

        else:
            
            print("\nLoaded History:\n")

            for msg in history:

                print(
                    type(msg).__name__,
                    msg.content
                )

            answer = (
                ask_question(
                    request.question,
                    history
                )
            )
            
        save_message(
            request.session_id,
            "human",
            request.question
        )

        save_message(
            request.session_id,
            "ai",
            answer
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

@app.get("/sessions")
def sessions():

    return {
        "sessions": get_sessions()
    }
    
@app.get(
    "/sessions/{session_id}"
)
def session_messages(
    session_id: str
):

    return {
        "messages":
        get_session_messages(
            session_id
        )
    }
    
@app.delete(
    "/sessions/{session_id}"
)
def remove_session(
    session_id: str
):

    delete_session(
        session_id
    )

    return {
        "success": True
    }
    
@app.get("/")
def home():
    return {
        "message": "PDF ChatBot  API Running"
    }

