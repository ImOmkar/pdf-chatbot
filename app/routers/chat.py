from fastapi import APIRouter
from fastapi import HTTPException
from app.services.chat_service import (
    chat_service,
    create_session,
    get_langchain_history,
    save_message,
    session_exists
)
import json

from app.services.rag_service import (
                    ask_question, 
                    ask_question_in_document,
                    generate_session_title,
                    stream_answer
                )

from app.schemas.schemas import (
    ChatRequest,
)

from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/chat")
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

            sources = []

        else:

            print("\nLoaded History:\n")

            for msg in history:

                print(
                    type(msg).__name__,
                    msg.content
                )

            result = (
                ask_question(
                    request.question,
                    history
                )
            )

            answer = (
                result["answer"]
            )

            sources = (
                result["sources"]
            )

        if not session_exists(
            request.session_id
        ):

            title = (
                generate_session_title(
                    request.question
                )
            )

            create_session(
                request.session_id,
                title
            )

        save_message(
            request.session_id,
            "human",
            request.question
        )

        save_message(
            request.session_id,
            "ai",
            answer,
            sources
        )

        return {

            "success": True,

            "answer": answer,

            "sources": sources

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@router.post("/chat/stream")
def chat_stream(
    request: ChatRequest
):

    return chat_service.stream_chat(
        request
    )