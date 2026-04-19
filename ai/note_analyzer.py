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
    temperature=0.2
)

# -----------------------------
# Main function
# -----------------------------
def analyze_note_with_gemini(content: str) -> dict:
    prompt = f"""
You are classifying a note for a second-brain app.

Input note:
{content}

Return ONLY valid JSON (no markdown, no extra text) with this exact shape:
{{
  "topic": "Idea|Bug|Reminder|Task|Research",
  "atomic_note": "one clear atomic note sentence"
}}
"""

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

        return {
            "topic": topic,
            "atomic_note": atomic_note,
        }

    except Exception:
        return {
            "topic": "Idea",
            "atomic_note": content.strip(),
        }