import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)


def analyze_note(content: str) -> dict:
    prompt = f"""
You are extracting structured memory for a second-brain system.

Input:
{content}

Return ONLY valid JSON:

{{
  "title": "short meaningful title (max 8 words)",
  "topic": "Idea|Bug|Reminder|Task|Research",
  "atomic_note": "one sentence summary",
  "entities": ["entity1", "entity2"],
  "relations": [
    {{
      "source": "entity1",
      "type": "RELATED_TO|DEPENDS_ON|PART_OF",
      "target": "entity2"
    }}
  ]
}}

Rules:
- title must be concise and informative
- entities must be noun phrases
- relations must be valid or []
- no extra text
"""

    try:
        response = llm.invoke(prompt)
        raw = (response.content or "").strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        data = json.loads(raw)

        topic = data.get("topic", "Idea")
        if topic not in ALLOWED_TOPICS:
            topic = "Idea"

        return {
            "title": data.get("title", "").strip() or "Untitled",
            "topic": topic,
            "atomic_note": data.get("atomic_note", content),
            "entities": data.get("entities", []) or [],
            "relations": data.get("relations", []) or []
        }

    except Exception:
        return {
            "title": "Untitled",
            "topic": "Idea",
            "atomic_note": content,
            "entities": [],
            "relations": []
        }