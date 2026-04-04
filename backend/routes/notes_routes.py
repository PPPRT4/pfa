import os
import sys
os.environ.setdefault("GROQ_API_KEY", "")

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

try:
    from ..database import get_db
    from ..models import Note
    from ..schemas import NoteCreate, PromptRequest
except ImportError:
    from database import get_db
    from models import Note
    from schemas import NoteCreate, PromptRequest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from ai.note_analyzer import analyze_note_with_langchain

router = APIRouter()
llm = ChatGroq(model="llama-3.3-70b-versatile")


def create_note_payload(note: NoteCreate, db: Session):
    ai_result = analyze_note_with_langchain(note.content)
    new_note = Note(
        title=note.title or "Untitled",
        content=note.content,
        topic=ai_result["topic"],
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "topic": new_note.topic,
        "atomic_note": ai_result["atomic_note"],
    }


@router.post("/add-note")
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    return {"message": "Note created successfully", "note": create_note_payload(note, db)}


@router.post("/prompt")
def get_prompt_result(payload: PromptRequest):
    try:
        messages = [
            SystemMessage(content="You are a helpful second-brain assistant."),
            HumanMessage(content=payload.prompt)
        ]
        response = llm.invoke(messages)
        return {"result": response.content}
    except Exception as e:
        return {"error": str(e)}