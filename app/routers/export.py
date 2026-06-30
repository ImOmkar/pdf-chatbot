from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import re

from app.services.export_service import (
    export_service
)

router = APIRouter()


@router.get(
    "/sessions/{session_id}/export"
)
def export_chat(
    session_id: str,
    format: str = "txt"
):

    if format != "txt":

        return {
            "detail":
                "Unsupported format"
        }

    result = (
        export_service.export_txt(
            session_id
        )
    )

    filename = re.sub(

        r'[<>:"/\\|?*]',

        "",

        result["title"]

    ).strip()

    if not filename:

        filename = "Conversation"

    return PlainTextResponse(

        result["content"],

        headers={

            "Content-Disposition":

                f'attachment; filename="{filename}.txt"'

        }

    )