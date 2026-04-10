import os
import sys
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

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
from ai.vector_store import add_note_to_vector_store
from ai.graph_store import add_note_to_graph, get_related_notes

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
    add_note_to_vector_store(new_note.id, new_note.content, ai_result["topic"])
    add_note_to_graph(new_note.id, new_note.title, ai_result["topic"])
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


@router.get("/related-notes/{topic}")
def related_notes(topic: str):
    results = get_related_notes(topic)
    return {"topic": topic, "related_notes": results}


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
@router.get("/evaluation")
def run_evaluation():
    try:
        import sys, os
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        if PROJECT_ROOT not in sys.path:
            sys.path.append(PROJECT_ROOT)

        from ai.vector_store import search_notes, add_note_to_vector_store
        from ai.note_analyzer import analyze_note_with_langchain

        EVAL_NOTES = [
            {"content": "LangChain is a framework for building LLM applications.", "expected_topic": "Research"},
            {"content": "Neo4j stores data as nodes and relationships.", "expected_topic": "Research"},
            {"content": "I need to buy groceries tomorrow.", "expected_topic": "Task"},
            {"content": "I have a doctor appointment next Monday.", "expected_topic": "Reminder"},
            {"content": "What if we used embeddings to cluster user feedback?", "expected_topic": "Idea"},
        ]
        EVAL_QUERIES = [
            {"query": "LangChain framework", "expected_in_results": "LangChain"},
            {"query": "graph database nodes", "expected_in_results": "Neo4j"},
            {"query": "doctor appointment", "expected_in_results": "doctor"},
        ]

        # Populate Chroma
        for i, item in enumerate(EVAL_NOTES):
            result = analyze_note_with_langchain(item["content"])
            add_note_to_vector_store(9000 + i, item["content"], result["topic"])

        # Classification
        classification = []
        correct_class = 0
        for item in EVAL_NOTES:
            result = analyze_note_with_langchain(item["content"])
            predicted = result["topic"]
            expected = item["expected_topic"]
            ok = predicted == expected
            if ok: correct_class += 1
            classification.append({
                "ok": ok,
                "expected": expected,
                "predicted": predicted,
                "content": item["content"][:50]
            })
        accuracy = correct_class / len(EVAL_NOTES) * 100

        # RAG
        rag = []
        correct_rag = 0
        for item in EVAL_QUERIES:
            results = search_notes(item["query"], n_results=3)
            found = any(item["expected_in_results"].lower() in r["content"].lower() for r in results)
            if found: correct_rag += 1
            rag.append({
                "ok": found,
                "query": item["query"],
                "top_result": results[0]["content"][:60] if results else "No results"
            })
        recall = correct_rag / len(EVAL_QUERIES) * 100
        overall = (accuracy + recall) / 2

        return {
            "classification": classification,
            "rag": rag,
            "summary": {
                "classification_accuracy": accuracy,
                "rag_recall": recall,
                "overall": overall
            }
        }
    except Exception as e:
        return {"error": str(e)}