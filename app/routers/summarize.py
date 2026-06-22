from fastapi import APIRouter
from app.services.rag_service import (
                    summarize_document, 
                )
from app.schemas.schemas import (
    SummaryRequest
)

router = APIRouter()

@router.post("/summarize")
def summarize(
    request: SummaryRequest
):

    try:

        summary = (
            summarize_document(
                request.filename
            )
        )

        return {
            "success": True,
            "summary": summary
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
