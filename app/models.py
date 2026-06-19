from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    declarative_base
)

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_message"
    
    id = Column(
        Integer,
        primary_key=True
    )
    
    session_id = Column(
        String,
        index=True
    )
    
    role = Column(
        String
    )
    
    content = Column(
        Text
    )
    
    
from .database import engine

Base.metadata.create_all(
    bind=engine
)