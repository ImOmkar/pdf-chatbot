from fastapi import APIRouter

from app.services.chat_service import (
    get_langchain_history,
    save_message
)

from app.services.rag_service import (
                    ask_question, 
                    ask_question_in_document,
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
