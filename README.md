<div align="center">

# 🤖 Multimodal RAG Chatbot

**A ChatGPT-style document chatbot powered by Google Gemini AI and Milvus vector database**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red?style=for-the-badge&logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![Milvus](https://img.shields.io/badge/Milvus-2.4-purple?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?style=for-the-badge&logo=google)
![Docker](https://img.shields.io/badge/Docker-Required-blue?style=for-the-badge&logo=docker)

</div>

---

## 📌 Overview

**Multimodal RAG Chatbot** is a full-stack Retrieval-Augmented Generation (RAG) application that lets you upload any document and chat with it intelligently. Ask questions in natural language and get accurate, context-aware answers generated directly from your document content.

### How it works

```
User uploads document
        ↓
Document is parsed and split into chunks
        ↓
Each chunk is converted to a vector (embedding) using Gemini Embedding API
        ↓
Vectors are stored in Milvus vector database
        ↓
User asks a question
        ↓
Question is embedded and matched against stored vectors
        ↓
Most relevant chunks are retrieved
        ↓
Gemini Flash generates a clear answer from those chunks
        ↓
Answer is displayed in the chat UI
```

---

## ✨ Features

- 📄 **Multi-format document support** — PDF, DOCX, TXT, CSV, PPTX
- 💬 **ChatGPT-style UI** — clean dark interface with chat history
- 🗂️ **Persistent chat sessions** — previous chats saved and resumable
- ✏️ **Rename & delete chats** — 3-dot menu on every chat
- 📊 **Performance metrics dashboard** — success rate, faithfulness, response time, context precision
- 🔑 **API Key guide page** — built-in step-by-step guide for new users
- 🔍 **Semantic search** — Milvus vector similarity search for accurate retrieval
- 🤖 **Google Gemini powered** — uses `gemini-2.5-flash` for generation and `gemini-embedding-001` for embeddings
- 🐳 **Docker-based Milvus** — one command to start the vector database

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Vector Database** | Milvus (via Docker) |
| **AI Model** | Google Gemini 2.5 Flash |
| **Embedding Model** | Gemini Embedding 001 |
| **PDF Parsing** | pdfplumber → pypdf → pdfminer (fallback chain) |
| **Text Chunking** | LangChain Text Splitters |
| **Containerization** | Docker + Docker Compose |

---

## 📁 Project Structure

```
multimodal_rag/
├── app/
│   ├── api/
│   │   ├── chat.py          # Chat endpoint
│   │   └── upload.py        # Document upload & indexing endpoint
│   ├── core/
│   │   └── milvus_db.py     # Milvus connection, insert, search
│   ├── frontend/
│   │   └── streamlit_app.py # Full UI — Chat, Metrics, API Guide pages
│   └── services/
│       ├── chunker.py       # Text splitting
│       ├── embeddings.py    # Gemini embedding with rate limiting
│       ├── gemini_service.py# Answer generation
│       ├── parser.py        # Document parsing (PDF/DOCX/TXT/CSV/PPTX)
│       └── retriever.py     # Vector search + fallback retrieval
├── chats/                   # Auto-created: stores chat history as JSON
├── uploads/                 # Auto-created: stores uploaded documents
├── docker-compose.yml       # Milvus + etcd + MinIO setup
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚙️ Prerequisites

Before you start, make sure you have:

| Tool | Version | Download |
|---|---|---|
| Python | 3.11.x | https://www.python.org/downloads/release/python-3119/ |
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop |
| Git | Latest | https://git-scm.com/downloads |
| Gemini API Key | — | https://aistudio.google.com/apikey |

> ⚠️ **Python 3.13 is NOT recommended** — use Python 3.11 for full compatibility with all packages.

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/multimodal-rag.git
cd multimodal-rag
```

### 2. Create virtual environment with Python 3.11

```bash
py -3.11 -m venv .venv
```

### 3. Activate virtual environment

```bash
# Windows PowerShell (run once if scripts are blocked)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\activate

# Windows CMD alternative
.venv\Scripts\activate.bat

# Mac / Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt --prefer-binary
```

### 5. Start Milvus with Docker

Make sure Docker Desktop is open, then:

```bash
docker compose up -d
```

Verify all 3 containers are running:

```bash
docker ps
```

You should see:
```
milvus_standalone   Up
milvus_etcd         Up
milvus_minio        Up
```

---

## ▶️ Running the App

You need **3 terminals** running simultaneously:

### Terminal 1 — Start FastAPI backend

```bash
.venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Wait for: `Application startup complete`

### Terminal 2 — Start Streamlit frontend

```bash
.venv\Scripts\activate
streamlit run app/frontend/streamlit_app.py
```

Browser opens automatically at **http://localhost:8501**

---

## 🔑 Getting a Gemini API Key

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with your **personal Gmail** account
3. Click **"Create API key"** → select **"Create API key in new project"**
4. Copy the key — it looks like `AIzaSyXXXXXXXXXXXXXXXXXX`
5. Paste it into the **"Gemini API Key"** field in the app sidebar

> ⚠️ Use a **personal Gmail**, not a college/institution account — institutional accounts often have Gemini API blocked by admins.

> 💡 Click the **"🔑 What is an API Key?"** button in the sidebar for a full in-app guide.

---

## 📖 How to Use

1. **Enter your Gemini API Key** in the sidebar
2. **Upload a document** — PDF, DOCX, TXT, CSV, or PPTX
3. Wait for indexing to complete (1–2 minutes for large files)
4. **Ask questions** in the chat input at the bottom
5. View **previous chats** in the sidebar — click to resume any session
6. **Rename or delete** chats using the ⋮ menu
7. Click **"📊 Performance Metrics"** to see answer quality stats
8. Click **"➕ New Chat"** to start a fresh session with a new document

---

## 📊 Performance Metrics

The metrics page (accessible from sidebar) shows:

| Metric | Description |
|---|---|
| **Answer Success Rate** | % of questions that received a valid answer |
| **Total Questions** | Total number of questions asked across all chats |
| **Keyword Relevance** | Word overlap score between question and answer (0–1) |
| **Answer Quality** | Score based on answer completeness and length (0–1) |
| **API Error Count** | Number of failed API calls |
| **Response Breakdown** | Chart of answered / error / no-answer / rate-limited |
| **System Health** | Retrieval health, API health, quality summary |

---

## 🐛 Common Issues & Fixes

| Error | Cause | Fix |
|---|---|---|
| `docker: 500 Internal Server Error` | Docker Desktop engine crashed | Restart Docker Desktop fully |
| `429 RESOURCE_EXHAUSTED` | Gemini free tier quota hit | Wait 1 minute or create a new API key in a new project |
| `401 UNAUTHENTICATED` | Wrong API key format | Re-copy the key from AI Studio, no extra spaces |
| `Scripts disabled` PowerShell error | Windows execution policy | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `Question not related to document` | Retrieval returning no chunks | Re-upload the document in a new chat |
| Upload timeout | Large PDF with many chunks | Wait — it retries automatically up to 600 seconds |

---

## 🛑 Stopping the App

```bash
# Terminal 2 — stop Streamlit
Ctrl + C

# Terminal 1 — stop FastAPI
Ctrl + C

# Stop Docker containers
docker compose down
```

---

## 📝 Notes

- Chat history is stored locally in the `chats/` folder as JSON files
- Uploaded documents are stored in the `uploads/` folder
- Each document's vector chunks are stored separately in Milvus — switching documents does not lose old data
- Free tier Gemini API supports ~15 requests/minute for generation and ~100/minute for embeddings

---

## 📄 License

⚠️ This is a proprietary project. All rights reserved © 2025 Surekha Brundavanam. Usage, reproduction, or distribution without permission is strictly prohibited.

---

<div align="center">
Built with ❤️ using Streamlit · FastAPI · Google Gemini · Milvus
</div>
