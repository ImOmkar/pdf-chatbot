from fastapi import FastAPI

# routes import3d
from app.routers.chat import router as chat_router
from app.routers.upload import router as upload_router
from app.routers.documents import router as document_router
from app.routers.sessions import router as sessions_router
from app.routers.summarize import router as summarize_router

app = FastAPI()

app.include_router(
    chat_router,
)

app.include_router(
    upload_router
)

app.include_router(
    document_router
)

app.include_router(
    sessions_router
)

app.include_router(
    summarize_router
)

  
@app.get("/")
def home():
    return {
        "message": "PDF ChatBot  API Running"
    }

