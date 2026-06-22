from fastapi import APIRouter
from app.services.rag_service import (
                    get_documents
                )


router = APIRouter()

@router.get("/documents")
def documents():

    return {
        "documents": get_documents()
    }