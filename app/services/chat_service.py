import json

from fastapi.responses import StreamingResponse

from app.db.database import (
    SessionLocal
)

from app.services.rag_service import (
    
    generate_session_title,
    stream_answer
)

from app.db.models import (
    ChatMessage,
    ChatSession
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)


def truncate_conversation_after_message(
    session_id,
    human_message_id
):

    db = SessionLocal()

    delete = False

    for message in (

        db.query(
            ChatMessage
        )

        .filter(
            ChatMessage.session_id == session_id
        )

        .order_by(
            ChatMessage.id
        )

    ):

        if delete:

            db.delete(
                message
            )

        elif (
            message.id == human_message_id
        ):

            delete = True

    db.commit()

    db.close()


class ChatService:

    def stream_chat(
        self,
        request
    ):

        history = get_langchain_history(
            request.session_id
        )

        return StreamingResponse(

            self._generate_stream(

                request,

                history

            ),

            media_type="text/event-stream"

        )
        
    def _generate_stream(
        self,
        request,
        history
    ):

        answer = ""

        sources = []

        for event in stream_answer(

            request.question,

            history

        ):

            if event["type"] == "chunk":

                answer += event["content"]

            elif event["type"] == "done":

                answer = event["answer"]

                sources = event["sources"]

            yield (
                f"data: "
                f"{json.dumps(event)}\n\n"
            )

        # -------------------------------
        # Save conversation
        # -------------------------------

        if request.regenerate_message_id:

            truncate_conversation_after_message(

                request.session_id,

                request.regenerate_message_id

            )

        self._create_session_if_needed(
            request
        )

        self._save_conversation(

            request,

            answer,

            sources

        )
        
        
    def _create_session_if_needed(
        self,
        request
    ):

        if session_exists(
            request.session_id
        ):
            return

        title = generate_session_title(
            request.question
        )

        create_session(
            request.session_id,
            title
        )
        
    def _save_conversation(
        self,
        request,
        answer,
        sources
    ):

        if not request.regenerate_message_id:

            save_message(

                request.session_id,

                "human",

                request.question

            )

        save_message(

            request.session_id,

            "ai",

            answer,

            sources

        )


chat_service = ChatService()

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

def get_session_title(
    session_id
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

    db.close()

    if not session:

        return "Conversation"

    return session.title
    
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
            "id": msg.id,

            "role": msg.role,

            "content": msg.content,

            "sources": msg.sources or []
        }
        for msg in messages
    ]
    
    
def save_message(
    session_id,
    role,
    content,
    sources=None
):
    db = SessionLocal()
    
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        sources=sources
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
    