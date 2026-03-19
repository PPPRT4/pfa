# 🧠 Second Brain — AI Notes Assistant v2.0

A modern, dark-themed AI-powered notes app built with **React + Tailwind CSS**.

---

## 🚀 Quick start

```bash
git clone <your-repo-url>
cd second-brain
npm install
npm start
# → http://localhost:3000
```

> **Requires Node.js 16+**

---

## 📁 Project structure

```
second-brain/
├── public/
│   └── index.html                  # Google Fonts loaded here
├── src/
│   ├── App.js                      # Router + protected routes
│   ├── index.js                    # React entry point
│   ├── index.css                   # Tailwind base + global component styles
│   │
│   ├── pages/
│   │   ├── Login.js                # Split-panel login with password field
│   │   └── Notes.js                # Main dashboard shell
│   │
│   ├── components/
│   │   ├── Sidebar.js              # Dark sidebar with nav, tag counts, user info
│   │   ├── AddNote.js              # Note input form with chips, char limit, shortcuts
│   │   ├── NoteCard.js             # Collapsible card with AI result panel
│   │   └── StatsPanel.js          # Session stats, type breakdown bar, mood tracker
│   │
│   └── utils/
│       ├── classifier.js           # Local AI classifier (no API key needed)
│       └── api.js                  # Backend fetch helper (POST /add-note)
│
├── tailwind.config.js              # Custom ink/gold/cream token system
├── postcss.config.js
├── .env                            # REACT_APP_API_URL config
├── .gitignore
└── package.json
```

---

## 🎨 Design system

| Token | Value | Usage |
|---|---|---|
| `ink-900` | `#0e1117` | Page background |
| `ink-800` | `#1c2233` | Card surfaces |
| `ink-700` | `#2a3350` | Borders, hover |
| `gold-400` | `#f0a93b` | Primary accent |
| Font | Plus Jakarta Sans | All text |
| Font mono | JetBrains Mono | Code, indices |

---

## ✨ Features

| Feature | Detail |
|---|---|
| Login | Username + password (≥4 chars), show/hide, remember me |
| Add note | Quick-type chips, ⌘↵ shortcut, 800-char limit, toast feedback |
| AI classify | Local classifier — Idea, Bug, Reminder, Task, Research |
| AI result | Type badge, summary sentence, keyword chips |
| Notes list | Filter by type, live search, collapse/expand per card |
| Stats panel | Total / analyzed / synced + type breakdown bars + mood tracker |
| Sidebar | Tag counts, user avatar, sign-out |
| Responsive | Mobile sidebar overlay, hidden panels on small screens |
| Backend | `POST /add-note` with 3s timeout + graceful fallback |

---

## 🔌 Backend API

Configure in `.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

The app calls `POST /add-note` with:
```json
{ "content": "your note text" }
```

**If the server is unreachable**, notes are saved locally with an amber indicator.

### Minimal FastAPI backend

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Note(BaseModel):
    content: str

@app.post("/add-note")
async def add_note(note: Note):
    print(f"[+] {note.content[:60]}")
    return {"status": "ok"}
```

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

---

## 🤖 AI Classifier

The built-in classifier in `src/utils/classifier.js` uses regex — **no API key needed**:

| Type | Trigger keywords |
|---|---|
| 🐛 Bug | `bug`, `error`, `crash`, `broken`, `fix` |
| ⏰ Reminder | `remind`, `must`, `todo`, `don't forget` |
| ✅ Task | `task`, `complete`, `ship`, `deploy` |
| 🔬 Research | `research`, `learn`, `study`, `explore` |
| 💡 Idea | *(default)* |

To connect a real LLM, replace `classifyNote()` in `src/utils/classifier.js` with a `fetch` call to your AI endpoint.

---

## 📜 Available scripts

| Command | Description |
|---|---|
| `npm start` | Dev server at localhost:3000 |
| `npm run build` | Production build → `build/` |
| `npm test` | Run test suite |

---

## 👥 Contributing

1. `git checkout -b feature/your-feature`
2. Make your changes
3. `git commit -m "feat: your message"`
4. `git push origin feature/your-feature`
5. Open a Pull Request
