import os
import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
#from google import genai
import requests
try:
    from ..database import get_db
    from ..models import Note
    from ..schemas import ChatRequest, NoteCreate, NoteUpdate
except ImportError:
    from database import get_db
    from models import Note
    from schemas import PromptRequest, NoteCreate, NoteUpdate
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Langgraph_agent.langgraph_agent import build_graph
from ai.note_analyzer import analyze_note
from ai.neo4j import save_to_neo4j
from ai.neo4j import save_to_neo4j
from ai.notes_ai import ajouter_note

router = APIRouter()
MCP_URL = "http://localhost:8001"

#client = genai.Client()
graph_app = build_graph()

def create_note_payload(note, db: Session):
    ai_result = analyze_note(note.content)

    new_note = Note(
        title=ai_result["title"],
        content=note.content,
        topic=ai_result["topic"],
    )

    try:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        # optional secondary graph system
        ajouter_note(str(new_note.id),
                     
            ai_result["atomic_note"],
            ai_result["topic"]
        )

        # neo4j graph ingestion
        save_to_neo4j(
            note_id=new_note.id,
            payload={
                **ai_result,
                "content": note.content
            }
        )

    except Exception as e:
        db.rollback()
        raise e

    return {
        "id": new_note.id,
        "title": ai_result["title"],
        "content": new_note.content,
        "topic": ai_result["topic"],
        "atomic_note": ai_result["atomic_note"],
        "entities": ai_result["entities"],
        "relations": ai_result["relations"],
    }

def serialize_note_for_front(note: Note):
    topic_to_type = {
        "Task": "task",
        "Reminder": "reminder",
        "Idea": "idea",
        "Research": "resource",
        "Bug": "other",
    }
    note_type = topic_to_type.get(note.topic, "other")

    return {
        "id": note.id,
        "content": note.content,
        "createdAt": note.created_at.isoformat() if note.created_at else None,
        "apiStatus": "success",
        "aiResult": {
            "type": note_type,
            "summary": note.content,
            "keywords": [],
        },
    }

@router.post("/add-note")
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    result = create_note_payload(note, db)
    return {"status": "success", "data": result}


@router.get("/notes")
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).order_by(Note.created_at.desc()).all()
    return [serialize_note_for_front(note) for note in notes]


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"status": "deleted"}


@router.put("/notes/{note_id}")
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.content = payload.content
    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "content": note.content,
        "createdAt": note.created_at.isoformat() if note.created_at else None,
        "apiStatus": "success",
        "aiResult": None,
    }


@router.post("/chat")
def get_chat_result(payload: PromptRequest):
    print("Received prompt:", payload.prompt)
    try :
        result = graph_app.invoke({"query": payload.prompt},
                                 config={"configurable": {"thread_id": "user-1"}})
        print("Graph result:", result.get("docs", []))
        return {"answer": result.get("answer", "No answer")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))