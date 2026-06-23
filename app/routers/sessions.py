from fastapi import APIRouter
import uuid

from app.services.chat_service import (
    get_sessions,
    get_session_messages,
    delete_session,
    rename_session)

from app.schemas.schemas import (
    RenameSessionRequest,
)


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


@router.post("/sessions")
def create_new_session():
    session_id = str(uuid.uuid4())

    return {
        "session_id": session_id
    }
    
    
@router.put(
    "/sessions/{session_id}"
)
def update_session(
    session_id: str,
    request: RenameSessionRequest
):

    rename_session(
        session_id,
        request.title
    )

    return {
        "success": True
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
  