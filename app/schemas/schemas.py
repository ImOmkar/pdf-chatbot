from pydantic import BaseModel
from typing import Optional

class ChatRequest(
    BaseModel
):
    session_id: str
    question: str
    document: Optional[str] = None

class SummaryRequest(BaseModel):
    filename: str