from app.services.chat_service import (
    get_session_messages,
    get_session_title
)


class ExportService:

    def export_txt(
        self,
        session_id
    ):

        messages = get_session_messages(
            session_id
        )

        lines = [

            "Conversation",

            "=" * 50,

            ""

        ]

        for message in messages:

            role = (

                "User"

                if message["role"] == "human"

                else "Assistant"

            )

            lines.append(
                role
            )

            lines.append(
                "-" * len(role)
            )

            lines.append(
                message["content"]
            )

            lines.append("")

        return {

            "title": get_session_title(
                session_id
            ),

            "content": "\n".join(lines)

        }


export_service = ExportService()