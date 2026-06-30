from fastapi import APIRouter
from fastapi import HTTPException

from app.services.source_service import (
    source_service
)

router = APIRouter()


@router.get(
    "/source"
)
def get_source(

    document: str,

    page: int

):

    result = (

        source_service.get_source_details(

            document,

            page

        )

    )

    if not result:

        raise HTTPException(

            status_code=404,

            detail="Source not found"

        )

    return result