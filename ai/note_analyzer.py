import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}

# -----------------------------
# Groq LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.
)

# -----------------------------
# Main function
# -----------------------------
def analyze_note_with_gemini(content: str) -> dict:
    prompt_template = """
    You are extracting structured memory for a second-brain system.

    Input note:
    {content}

    Return ONLY valid JSON (no markdown, no extra text) with this exact shape:

    {
    "topic": "Idea|Bug|Reminder|Task|Research",
    "atomic_note": "one clear atomic sentence",

    "entities": ["entity1", "entity2"],

    "relations": [
        {
        "source": "entity1",
        "type": "RELATED_TO",
        "target": "entity2"
        }
    ]
    }

    Rules:
    - entities must be short noun phrases (no sentences)
    - relations must ONLY use: RELATED_TO, DEPENDS_ON, PART_OF
    - if no relations exist, return empty list []
    - if no entities exist, return []
    """
    prompt = prompt_template.replace("{content}", content)
    
    try:
        response = llm.invoke(prompt)
        raw_text = (response.content or "").strip()

        # clean possible code blocks
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        parsed = json.loads(raw_text)

        topic = str(parsed.get("topic", "Idea")).strip()
        if topic not in ALLOWED_TOPICS:
            topic = "Idea"

        atomic_note = str(parsed.get("atomic_note", "")).strip()
        if not atomic_note:
            atomic_note = content.strip()

        entities = parsed.get("entities", [])
        if not isinstance(entities, list):
            entities = []
        entities = [str(e).strip() for e in entities if str(e).strip()]

        relations = parsed.get("relations", [])
        if not isinstance(relations, list):
            relations = []

        allowed_relation_types = {"RELATED_TO", "DEPENDS_ON", "PART_OF"}
        normalized_relations = []
        for r in relations:
            if not isinstance(r, dict):
                continue
            src = str(r.get("source", "")).strip()
            rel_type = str(r.get("type", "")).strip().upper()
            dst = str(r.get("target", "")).strip()
            if not src or not dst or rel_type not in allowed_relation_types:
                continue
            normalized_relations.append({"source": src, "type": rel_type, "target": dst})

        return {
            "topic": topic,
            "atomic_note": atomic_note,
            "entities": entities,
            "relations": normalized_relations,
        }

    except Exception:
        return {
        "topic": "Idea",
        "atomic_note": content.strip(),
        "entities": [],
        "relations": []
    }