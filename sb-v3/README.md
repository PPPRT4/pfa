# 🧠 Second Brain v3.0 — AI Notes + Chat

A modern dark-themed app to capture notes, classify them with AI, and **chat with your notes** like ChatGPT.

---

## 🚀 Quick start

```bash
git clone <your-repo-url>
cd second-brain
npm install
npm start
# → http://localhost:3000
```

---

## 🤖 Enable AI Chat

1. Get an API key from [console.anthropic.com](https://console.anthropic.com/)
2. Open `.env` and add your key:

```env
REACT_APP_ANTHROPIC_KEY=sk-ant-api03-...
```

3. Restart the dev server: `npm start`

The chat uses your notes as context to give personalized answers.

---

## 📁 Project structure

```
second-brain/
├── public/index.html
├── src/
│   ├── App.js                      # Router + protected routes
│   ├── index.js / index.css        # Entry + Tailwind + global styles
│   │
│   ├── pages/
│   │   ├── Login.js                # Split-panel login with password
│   │   └── Notes.js                # Dashboard: Add / Notes / Chat views
│   │
│   ├── components/
│   │   ├── Sidebar.js              # Dark sidebar with Chat nav item
│   │   ├── AddNote.js              # Note form with chips + shortcuts
│   │   ├── NoteCard.js             # Collapsible card + AI result
│   │   ├── StatsPanel.js           # Stats + mood tracker
│   │   └── ChatView.js             # ★ NEW — ChatGPT-style chat interface
│   │
│   └── utils/
│       ├── classifier.js           # Local AI classifier (no key needed)
│       ├── api.js                  # POST /add-note helper
│       └── chatApi.js              # ★ NEW — Anthropic API + context builder
│
├── tailwind.config.js
├── postcss.config.js
├── .env                            # API keys config
└── package.json
```

---

## ✨ Features

### Notes
| Feature | Detail |
|---|---|
| Login | Username + password (≥4 chars), show/hide, remember me |
| Add note | Quick chips, ⌘↵ shortcut, 800-char limit, toast feedback |
| AI classify | Idea / Bug / Reminder / Task / Research (local, no key) |
| AI result | Type badge, summary, keywords per note |
| Filter & search | Filter by type, live text search |
| Backend sync | `POST /add-note` with graceful fallback |

### AI Chat (new in v3)
| Feature | Detail |
|---|---|
| ChatGPT-style UI | Message bubbles, avatars, timestamps |
| Notes as context | All your notes injected as system context |
| Note references | Shows which note was cited in the reply |
| Suggested questions | Quick prompts based on your note types |
| Auto-resize input | Textarea grows with your message |
| Typing indicator | Animated dots while AI responds |
| Clear chat | Reset conversation anytime |

---

## 🔌 Backend API

```
POST http://localhost:8000/add-note
{ "content": "note text" }
```

### Minimal FastAPI backend

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])

class Note(BaseModel):
    content: str

@app.post("/add-note")
async def add_note(note: Note):
    return {"status": "ok"}
```

```bash
pip install fastapi uvicorn && uvicorn main:app --reload
```

---

## 🏗️ How the chat works

1. User adds notes → classified locally by `classifier.js`
2. On opening Chat, `chatApi.js` builds a system prompt with all notes as context
3. Each message is sent to Anthropic's API (`claude-sonnet-4-20250514`)
4. The response references relevant notes when possible
5. Suggested questions adapt based on what types of notes you have

---

## 📜 Scripts

| Command | Description |
|---|---|
| `npm start` | Dev server → localhost:3000 |
| `npm run build` | Production build |
| `npm test` | Run tests |

---

## 👥 Team workflow

```bash
git checkout -b feature/your-feature
# make changes
git add . && git commit -m "feat: your message"
git push origin feature/your-feature
# open Pull Request
```
