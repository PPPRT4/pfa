import os
import sys

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from google import genai

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

from ai.note_analyzer import analyze_note_with_gemini

router = APIRouter()


client = genai.Client()


def create_note_payload(note: NoteCreate, db: Session):
    ai_result = analyze_note_with_gemini(note.content)
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
    return {
        "message": "Note created successfully",
        "note": create_note_payload(note, db),
    }


@router.post("/prompt")
def get_prompt_result(payload: PromptRequest):
    try :
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=payload.prompt
        )
        return {
            "result": response.text
        }
    except Exception as e:
        return {
            "error": str(e)
        }