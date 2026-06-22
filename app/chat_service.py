from .database import (
    SessionLocal
)

from .models import (
    ChatMessage
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

def get_sessions():
    
    db = SessionLocal()
    
    sessions = (
        db.query(
            ChatMessage.session_id
        )
        .distinct()
        .all()
    )
    
    db.close()
    
    return [
        session[0]
        for session in sessions
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


def delete_session(
    session_id
):

    db = SessionLocal()

    (
        db.query(
            ChatMessage
        )
        .filter(
            ChatMessage.session_id
            == session_id
        )
        .delete()
    )

    db.commit()

    db.close()