from fastapi import APIRouter

from app.services.chat_service import (
    create_session,
    get_langchain_history,
    save_message,
    session_exists
)

from app.services.rag_service import (
                    ask_question, 
                    ask_question_in_document,
                    generate_session_title,
                )

from app.schemas.schemas import (
    ChatRequest,
)

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
