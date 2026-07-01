from fastapi import APIRouter
from app.services.rag_service import (
                    get_document_metadata,
                    get_documents,
                    delete_document,
                )


router = APIRouter()

@router.get("/documents")
def documents():

    return {
        "documents": get_documents()
    }
    
    
@router.get(
    "/document-info"
)
def document_info(
    filename: str
):

    return (
        get_document_metadata(
            filename
        )
    )
    
    
@router.delete(
    "/documents"
)
def remove_document(
    filename: str
):

    deleted_count = (
        delete_document(
            filename
        )
    )

    return {
        "success": True,
        "deleted_chunks":
            deleted_count
    }