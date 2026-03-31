from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os
from google import genai

try:
    from ..database import get_db
    from ..models import Note
    from ..schemas import NoteCreate, PromptRequest
except ImportError:
    from database import get_db
    from models import Note
    from schemas import NoteCreate, PromptRequest

router = APIRouter()


client = genai.Client()

@router.post("/note")
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "message": "Note created successfully",
        "note": {
            "id": new_note.id,
            "title": new_note.title,
            "content": new_note.content,
        },
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