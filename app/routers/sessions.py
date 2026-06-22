from fastapi import APIRouter

from app.services.chat_service import (
    get_sessions,
    get_session_messages,
    delete_session)


router = APIRouter()

@router.get("/sessions")
def sessions():

    return {
        "sessions": get_sessions()
    }
    
@router.get(
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
    
@router.delete(
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
  