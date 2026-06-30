from pydantic import BaseModel
from typing import Optional

class ChatRequest(
    BaseModel
):
    session_id: str
    question: str
    document: Optional[str] = None
    regenerate_message_id: int | None = None

class SummaryRequest(BaseModel):
    filename: str

class SessionCreateResponse(BaseModel):
    session_id: str
    
class RenameSessionRequest(
    BaseModel
):

    title: str