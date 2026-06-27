from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_classic.chains.retrieval import (
    create_retrieval_chain
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)



from langchain_core.messages import (
    HumanMessage,
    AIMessage
)


from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_chroma import Chroma



load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

qa_prompt = ChatPromptTemplate.from_template(
"""
Answer the question using only the provided context.

Context:
{context}

Question:
{input}
"""
)

document_chain = create_stuff_documents_chain(
    llm,
    qa_prompt
)

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)


def generate_session_title(first_question):
    
    prompt = f"""
        Generate a short conversation title
        for this question.

        Question:

        {first_question}

        Maximum 5 words.
    """ 
    
    response = llm.invoke(
        prompt
    )

    return response.content

def upload_document(
    pdf_path
):

    loader = PyPDFLoader(
        pdf_path
    )

    documents = loader.load()
    
    page_count = len(documents)

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = splitter.split_documents(
        documents
    )
    
    chunk_count = len(chunks)
    
    for chunk in chunks:

        chunk.metadata["page_count"] = (
            page_count
        )

        chunk.metadata["chunk_count"] = (
            chunk_count
        )

    vector_store.add_documents(
        chunks
    )

    return len(chunks)


def retrieve_with_scores(
    query
):

    return (
        vector_store.similarity_search_with_score(
            query,
            k=3
        )
    )

def get_answer(
    question
):

    return (
        retrieval_chain.invoke(
            {
                "input": question
            }
        )
    )

def get_documents():

    results = vector_store.get()

    sources = set()

    for metadata in results["metadatas"]:

        source = metadata.get(
            "source"
        )

        if source:

            sources.add(
                source
            )

    return sorted(
        list(sources)
    )

def ask_question(
    question,
    session_history
):
    
    rewritten_question = (
        rewrite_question(
            question,
            session_history
        )
    )

    response = (
        retrieval_chain.invoke(
            {
                "input": rewritten_question
            }
        )
    )

    sources = []

    for doc in response["context"]:

        sources.append({

            "document":
                doc.metadata
                .get(
                    "source",
                    ""
                )
                .split("/")[-1]
                .split("\\")[-1],

            "page":
                doc.metadata.get(
                    "page",
                    0
                ) + 1

        })

    return {

        "answer":
            response["answer"],

        "sources":
            sources

    }

def summarize_document(
    filename
):

    docs = vector_store.similarity_search(
        filename,
        k=10
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
            if filename.lower()
            in doc.metadata.get(
                "source",
                ""
            ).lower()
        ]
    )

    if not context:

        return (
            f"No document found: "
            f"{filename}"
        )

    prompt = f"""
Summarize this document.

Document:

{context}

Provide a structured summary.
"""

    response = llm.invoke(
        prompt
    )

    return response.content


def ask_question_in_document(
    question,
    document_name
):

    docs_with_scores = (
        vector_store.similarity_search_with_score(
            question,
            k=5
        )
    )

    docs = []

    for doc, score in docs_with_scores:

        source = (
            doc.metadata.get(
                "source",
                ""
            )
        )

        if (
            document_name.lower()
            in source.lower()
        ):

            docs.append(
                doc
            )

    return document_chain.invoke(
        {
            "input": question,
            "context": docs
        }
    )
    
    
contextualize_q_prompt = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Given a chat history and the latest user question,
rewrite the question so it can be understood
without the chat history.

Do not answer the question.
Only rewrite it.
"""
            ),

            MessagesPlaceholder(
                "chat_history"
            ),

            (
                "human",
                "{input}"
            )
        ]
    )
)

def rewrite_question(
    question,
    chat_history
):

    prompt = (
        contextualize_q_prompt.format_messages(
            input=question,
            chat_history=chat_history
        )
    )

    response = llm.invoke(
        prompt
    )

    return response.content



def get_document_metadata(
    document_name
):

    docs = (
        vector_store.similarity_search(
            document_name,
            k=1
        )
    )

    if not docs:

        return None

    doc = docs[0]

    return {

        "filename":
            document_name,

        "page_count":
            doc.metadata.get(
                "page_count",
                0
            ),

        "chunk_count":
            doc.metadata.get(
                "chunk_count",
                0
            )

    }
    
    
def delete_document(
    document_name
):

    results = vector_store.get()

    ids_to_delete = []

    for doc_id, metadata in zip(
        results["ids"],
        results["metadatas"]
    ):

        source = metadata.get(
            "source",
            ""
        )

        if (
            document_name.lower()
            in source.lower()
        ):

            ids_to_delete.append(
                doc_id
            )

    if ids_to_delete:

        vector_store.delete(
            ids=ids_to_delete
        )

    return len(ids_to_delete)