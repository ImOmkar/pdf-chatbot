from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routes import3d
from app.routers.chat import router as chat_router
from app.routers.upload import router as upload_router
from app.routers.documents import router as document_router
from app.routers.sessions import router as sessions_router
from app.routers.summarize import router as summarize_router

app = FastAPI()

# cross origin support
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

