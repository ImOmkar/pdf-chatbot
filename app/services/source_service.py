from app.services.rag_service import (
    vector_store
)


class SourceService:

    def get_source_details(
        self,
        document,
        page
    ):
    
        results = vector_store.get()

        page_chunks = []

        metadata_result = None

        for metadata, text in zip(

            results["metadatas"],

            results["documents"]

        ):

            source = (
                metadata.get(
                    "source",
                    ""
                )
                .split("/")[-1]
                .split("\\")[-1]
            )

            page_number = (
                metadata.get(
                    "page",
                    0
                ) + 1
            )

            if (

                source == document

                and

                page_number == page

            ):

                page_chunks.append(
                    text
                )

                metadata_result = metadata

        if not page_chunks:

            return None

        return {

            "document": document,

            "page": page,

            "chunks": page_chunks,

            "metadata": metadata_result

        }


source_service = SourceService()


