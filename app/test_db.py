from app.services.chat_service import (
    save_message,
    load_history
)

save_message(
    "session1",
    "human",
    "Who approved the loan?"
)

save_message(
    "session1",
    "ai",
    "Branch Manager Neha Kulkarni"
)

history = load_history(
    "session1"
)

for msg in history:
    
    print(
        msg.role,
        ":",
        msg.content
    )