import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
os.environ.setdefault("GROQ_API_KEY", "")

llm = ChatGroq(model="llama-3.3-70b-versatile")

ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}


def analyze_note_with_langchain(content: str) -> dict:
    messages = [
        SystemMessage(content=(
            "You are classifying notes for a second-brain app. "
            "Always respond with ONLY valid JSON, no markdown, no extra text."
        )),
        HumanMessage(content=f"""
Classify this note:
{content}

Return ONLY this JSON shape:
{{
  "topic": "Idea|Bug|Reminder|Task|Research",
  "atomic_note": "one clear atomic note sentence"
}}
""")
    ]

    try:
        response = llm.invoke(messages)
        raw_text = (response.content or "").strip()
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
        return {"topic": topic, "atomic_note": atomic_note}
    except Exception as e:
        print(f"[note_analyzer] error: {e}")
        return {"topic": "Idea", "atomic_note": content.strip()}