# DocMind AI – Backend

Backend service for **DocMind AI**, an AI-powered document assistant that lets users chat with one or multiple PDF documents using Retrieval-Augmented Generation (RAG).

Built with **FastAPI**, **LangChain**, **Google Gemini**, **ChromaDB**, and **SQLAlchemy**.

---

## ✨ Features

- 📄 Upload and process PDF documents
- 💬 AI-powered conversational chat
- 📚 Multi-document RAG (chat across multiple PDFs)
- 🔍 Source citations with page numbers
- 📝 AI-generated document summaries
- ⚡ Streaming responses (Server-Sent Events)
- 💡 Suggested follow-up questions
- 🧠 Conversational history with question rewriting
- 📂 Session management
- 📌 Pin and organize chat sessions

---

## 🛠 Tech Stack

- FastAPI
- LangChain
- Google Gemini
- ChromaDB
- SQLAlchemy
- SQLite
- PyMuPDF
- Server-Sent Events (Streaming)

---

## 📁 Project Structure

```text
app/
├── api/
├── services/
├── models/
├── repositories/
├── prompts/
├── utils/
└── ...
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/docmind-ai-backend.git

cd docmind-ai-backend
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file.

```env
GOOGLE_API_KEY=your_google_api_key
```

### Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://localhost:8000
```

---

## 📡 Main API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a PDF |
| POST | `/chat/stream` | Stream AI responses |
| POST | `/summarize` | Generate document summary |
| GET | `/documents` | List uploaded PDFs |
| DELETE | `/documents` | Delete a PDF |
| GET | `/sessions` | Get chat sessions |
| POST | `/sessions` | Create a session |
| PATCH | `/sessions/{id}/pin` | Pin/Unpin session |
| GET | `/source` | View source page |

---

## 🏗 Architecture

```text
React Frontend
        │
        ▼
FastAPI API
        │
        ▼
LangChain
        │
        ▼
Google Gemini
        │
        ▼
ChromaDB Vector Store
        │
        ▼
PDF Documents
```

---

## 🎯 Highlights

- Streaming AI responses
- Multi-document semantic retrieval
- Context-aware conversations
- Source-grounded answers
- Modular service architecture
- Responsive frontend integration

---

## 📄 License

This project is created for learning and portfolio purposes.

---

## 👨‍💻 Author

**Omkar Parab**

If you found this project interesting, feel free to connect or explore the frontend repository.