from app.db.database import (
    SessionLocal
)

from app.db.models import (
    ChatMessage,
    ChatSession
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

def create_session(session_id, title):
    
    db = SessionLocal()
    
    session = ChatSession(
        session_id=session_id,
        title=title
    )
    
    db.add(session)
    db.commit()
    db.close()
    
def session_exists(session_id):
    
    db = SessionLocal()
    
    session = (
        db.query(
            ChatSession
        ).filter(
            ChatSession.session_id == session_id
        )
        .first()
    )
    
    db.close()
    
    return session is not None

def get_sessions():

    db = SessionLocal()

    sessions = (
        db.query(
            ChatSession.session_id,
            ChatSession.title
        )
        .all()
    )

    db.close()

    return [
        {
            "session_id": session_id,
            "title": title
        }
        for session_id, title in sessions
    ]
    
    
def get_session_messages(
    session_id
):

    db = SessionLocal()

    messages = (
        db.query(
            ChatMessage
        )
        .filter(
            ChatMessage.session_id
            == session_id
        )
        .order_by(
            ChatMessage.id
        )
        .all()
    )

    db.close()

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]
    
    
def save_message(
    session_id,
    role,
    content
):
    db = SessionLocal()
    
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    
    db.add(message)
    db.commit()
    db.close()
    

def load_history(
    session_id,
):
    db = SessionLocal()
    
    message = (
        db.query(
            ChatMessage
        )
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.id
        )
        .all()
    )
    
    db.close()
    
    return message


def get_langchain_history(
    session_id
):

    history = load_history(
        session_id
    )

    messages = []

    for msg in history:

        if msg.role == "human":

            messages.append(
                HumanMessage(
                    content=msg.content
                )
            )

        elif msg.role == "ai":

            messages.append(
                AIMessage(
                    content=msg.content
                )
            )

    return messages

history = get_langchain_history(
    "session1"
)

print(history)


def rename_session(
    session_id,
    title
):

    db = SessionLocal()

    session = (
        db.query(
            ChatSession
        )
        .filter(
            ChatSession.session_id
            == session_id
        )
        .first()
    )

    if session:

        session.title = title

        db.commit()

    db.close()

def delete_session(
    session_id
):

    db = SessionLocal()

    db.query(
        ChatMessage
    ).filter(
        ChatMessage.session_id
        == session_id
    ).delete()

    db.query(
        ChatSession
    ).filter(
        ChatSession.session_id
        == session_id
    ).delete()

    db.commit()

    db.close()
    