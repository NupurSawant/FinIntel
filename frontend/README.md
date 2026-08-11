# Finance Risk & Investment Intelligence — React Frontend

A modern React + Vite + Tailwind CSS frontend for the Finance Risk & Investment Intelligence FastAPI backend.

## Features

- **Authentication**: Email + password login with persistent Auth token in `localStorage` (survives page refreshes).
- **Sidebar Layout**:
  - **User Profile**: Avatar badge, username display, and Logout action.
  - **Conversations**: Create new chats ("➕ New Chat"), switch between active conversations, and delete chats ("×").
  - **Documents (RAG)**: Multi-file uploader (.pdf, .docx, .txt), ingestion feedback, and list of indexed documents with deletion capability.
  - **Database (SQL)**: Ingest `.sql` database schema and view current database tables.
- **Main Chat Area**:
  - Real-time SSE query streaming with live multi-agent phase tracking (Crew -> Critic -> Route decision -> Final response).
  - Graceful fallback to non-streaming REST endpoint if stream interrupted.
  - Role-based chat bubbles and status indicators.

## Running Locally

### 1. Start the FastAPI Backend
```bash
cd ../backend
uvicorn main:app --reload
```
By default, the backend runs on `http://localhost:8000`.

### 2. Start the React Dev Server
```bash
npm install
npm run dev
```
Open `http://localhost:3000` (or `http://localhost:5173`) in your browser.