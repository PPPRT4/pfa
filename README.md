# PFA - Agentic Second Brain 🧠

## Overview 🔎
PFA (Personal Future Assistant) is an agentic second-brain system designed to store, connect, and retrieve personal knowledge using a hybrid architecture.

It combines:
- Neo4j for graph-based memory and relationships 🕸️
- ChromaDB for vector-based semantic search 🔎
- LangGraph for agent orchestration 🧭
- LangSmith for evaluation and tracing 📊
- FastAPI as the backend service ⚡
- React as the frontend interface ⚛️

The system enables users to store notes, query them semantically, and retrieve context using an LLM-driven agent that leverages both structured (graph) and unstructured (vector) memory.

## System Architecture 🏛️
1. User interacts via React frontend
2. Requests are handled by FastAPI backend
3. LangGraph agent processes queries
4. Retrieval happens via:
   - ChromaDB (semantic similarity search)
   - Neo4j (graph relationships)
5. Results are synthesized by the agent and returned to the user

### 🏗️ Architecture
```
              ┌────────────────────┐
              │   React Frontend   │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │  FastAPI Backend   │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │   LangGraph Agent  │
              └──────┬──────┬──────┘
                     │      │
           ┌─────────┘      └─────────────────┐
           ▼                                  ▼
    ┌──────────────┐                    ┌──────────────┐
    │   ChromaDB   │                    │    Neo4j     │
    │ (Vector DB)  │                    │ (Graph DB)   │
    └──────────────┘                    └──────────────┘
```

## Features ✨
- Note ingestion and storage
- Hybrid search (vector + graph)
- Agentic reasoning using LangGraph
- Persistent knowledge graph with Neo4j
- Semantic embeddings via ChromaDB
- Evaluation and tracing with LangSmith
- Full-stack implementation (FastAPI + React)

## Requirements ✅
- Python 3.10+
- Node.js 18+
- Docker and Docker Compose

## Setup Instructions 🛠️

### 1. Start infrastructure services
Run the required databases and services:

```bash
docker compose up -d
```

This initializes Neo4j, Postgres, and supporting services defined in the compose file.

### 2. Backend setup
Navigate to the backend directory and install dependencies:

```bash
cd backend

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

Backend will run at:
http://localhost:8000

### 3. Frontend setup
Navigate to the frontend directory:

```bash
cd sb-v3

npm install
npm start
```

Frontend will run at:
http://localhost:3000

## Environment Variables ⚙️

### Backend (backend/.env)
- DATABASE_URL
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- NEO4J_URI
- NEO4J_USERNAME
- NEO4J_PASSWORD
- NEO4J_TRANSPORT
- NEO4J_MCP_SERVER_HOST
- NEO4J_MCP_SERVER_PORT
- GEMINI_API_KEY
- GROQ_API_KEY
- LANGCHAIN_TRACING_V2
- LANGSMITH_ENDPOINT
- LANGSMITH_API_KEY
- LANGSMITH_PROJECT

### Frontend (sb-v3/.env)
- REACT_APP_API_URL
- REACT_APP_ANTHROPIC_KEY

## API Usage Examples 🔌

### Add a note
```bash
curl -X POST http://localhost:8000/add-note \
  -H "Content-Type: application/json" \
  -d '{"content":"Read Atomic Habits this weekend"}'
```

### Semantic search
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"habits productivity"}'
```

### Evaluation
Run LangSmith evaluation pipeline:

```bash
python Langgraph_agent/run_eval.py
```

## Project Structure 🗂️
```
ai/               # Embeddings, ChromaDB, Neo4j utilities
backend/          # FastAPI backend, routes, models, migrations
Langgraph_agent/  # Agent logic and evaluation pipeline
mcp/              # MCP server / vector-related assets
sb-v3/            # React frontend application
seed/             # Seed scripts for initializing data
```

## Notes 📝
- The system is designed for extensibility, allowing new memory types and retrieval strategies.
- Neo4j and ChromaDB work together to provide both relational and semantic context.
- LangGraph handles multi-step reasoning and tool use for retrieval and synthesis.
