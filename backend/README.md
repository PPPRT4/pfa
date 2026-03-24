# Backend - Quick Run Guide

This backend uses FastAPI + PostgreSQL.

## Prerequisites

- Python 3.10+
- Docker + Docker Compose

## 1) Setup environment

From this folder, create your local env file:

```bash
cp .env.example .env
```

## 2) Start PostgreSQL

```bash
docker compose up -d
```

## 3) Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 4) Install dependencies

```bash
pip install -r requirements.txt
```

## 5) Run backend

```bash
uvicorn main:app --reload
```

Backend URL:

- http://127.0.0.1:8000

API docs:

- http://127.0.0.1:8000/docs

## Useful commands

Stop database:

```bash
docker compose down
```

If port 8000 is busy:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
kill -9 <PID>
```
