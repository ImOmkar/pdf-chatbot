from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_chroma import Chroma

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_classic.chains.retrieval import (
    create_retrieval_chain
)


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
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


def update_memory(
    chat_history,
    question,
    answer
):

    chat_history.append(
        HumanMessage(
            content=question
        )
    )

    chat_history.append(
        AIMessage(
            content=answer
        )
    )

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return chat_history

def print_sources(
    documents
):

    print("\nSources:")

    for doc in documents:

        print(
            f"{doc.metadata.get('source')} "
            f"(Page {doc.metadata.get('page', 0) + 1})"
        )


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


def list_documents():

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

def retrieve_with_scores_for_document(
    query,
    document_name
):

    docs_with_scores = (
        vector_store.similarity_search_with_score(
            query,
            k=3
        )
    )

    filtered_docs = []

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

            filtered_docs.append(
                (
                    doc,
                    score
                )
            )

    return filtered_docs

def get_answer_from_docs(
    question,
    docs
):

    return document_chain.invoke(
        {
            "input": question,
            "context": docs
        }
    )


def clear_chat():

    return [], None

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

active_document = None

chat_history = []

print("Testing embedding...")

test = embeddings.embed_query(
    "Who approved the loan?"
)

print(len(test))

while True:

    question = input("\nYou: ")

    if question.lower().startswith(
        "upload "
    ):

        pdf_path = question[7:].strip()

        try:

            print(
                f"Loading: {pdf_path}"
            )

            chunk_count = (
                upload_document(
                    pdf_path
                )
            )

            print(
                f"\nUploaded successfully."
            )

            print(
                f"Chunks created: "
                f"{chunk_count}"
            )

        except Exception as e:

            print(
                f"\nError: {e}"
            )

        continue
        

    if question.lower() == "clear chat":

        chat_history, active_document = (
            clear_chat()
        )

        print(
            "\n Chat history cleared."
        )

        print(
            "Active document removed."
        )

        continue

    if question.lower() == "list documents":

        documents = (
            list_documents()
        )

        print(
            f"\nTotal Documents: "
            f"{len(documents)}\n"
        )

        for document in documents:

            print(document)

        continue

    if question.lower().startswith(
        "chat "
    ):

        active_document = (
            question
            .replace(
                "chat",
                ""
            )
            .strip()
        )

        print(
            f"\nNow chatting with: "
            f"{active_document}"
        )

        continue


    if question.lower().startswith(
        "summarize "
    ):

        filename = (
            question
            .replace(
                "summarize",
                ""
            )
            .strip()
        )

        summary = (
            summarize_document(
                filename
            )
        )

        print("\nAI:")
        print(summary)

        continue

    if question.lower() == "exit":
        break

    history_text = (
        build_history_text(
            chat_history
        )
    )

    rewritten_question = (
        rewrite_question(
            question,
            history_text
        )
    )

    print("\nRewritten Question:")
    print(rewritten_question)

    if active_document:

        docs_with_scores = (
            retrieve_with_scores_for_document(
                rewritten_question,
                active_document
            )
        )

    else:

        docs_with_scores = (
            retrieve_with_scores(
                rewritten_question
            )
        )

    print("\nRetrieval Scores:\n")

    for doc, score in docs_with_scores:

        print(
            f"{doc.metadata.get('source')} "
            f"-> Score: {score}"
        )

    docs = [
        doc
        for doc, score in docs_with_scores
    ]

    if active_document:

        response = get_answer_from_docs(
            rewritten_question,
            docs
        )

    else:

        response = get_answer(
            rewritten_question
        )

    if active_document:

        print_sources(
            docs
        )

    else:

        print_sources(
            response["context"]
        )

    print("\nAI:")
    
    if active_document:

        print(response)

    else:

        print(response["answer"])

    if active_document:

        answer_text = response

    else:

        answer_text = response["answer"]

    chat_history = update_memory(
        chat_history,
        question,
        answer_text
    )

    print(
        f"\nMemory Size: {len(chat_history)}"
    )