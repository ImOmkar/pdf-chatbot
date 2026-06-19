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


def upload_document(
    pdf_path
):

    loader = PyPDFLoader(
        pdf_path
    )

    documents = loader.load()

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = splitter.split_documents(
        documents
    )

    vector_store.add_documents(
        chunks
    )

    return len(chunks)



def rewrite_question(
    question,
    history_text
):

    rewrite_prompt = f"""
History:

{history_text}

Question:

{question}

Rewrite the question only.
Do not answer.
"""

    response = llm.invoke(
        rewrite_prompt
    )

    return response.content

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

def build_history_text(
    chat_history
):

    history_text = ""

    for msg in chat_history:

        if isinstance(
            msg,
            HumanMessage
        ):

            history_text += (
                f"User: {msg.content}\n"
            )

        elif isinstance(
            msg,
            AIMessage
        ):

            history_text += (
                f"AI: {msg.content}\n"
            )

    return history_text


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
    question
):

    response = (
        retrieval_chain.invoke(
            {
                "input": question
            }
        )
    )

    return response["answer"]

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