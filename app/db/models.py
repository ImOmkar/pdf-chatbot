from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    JSON,
    Boolean
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
    
    sources = Column(
        JSON,
        nullable=True
    )
        
    
class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(
        Integer,
        primary_key=True
    )

    session_id = Column(
        String,
        unique=True,
        index=True
    )

    title = Column(
        String
    )

    is_pinned = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    
from .database import engine

Base.metadata.create_all(
    bind=engine
)