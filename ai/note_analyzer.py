import json

from google import genai

ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}
_client = genai.Client()


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
        response = _client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw_text = (response.text or "").strip()

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
        # Keep note creation resilient if AI output is malformed or unavailable.
        return {
            "topic": "Idea",
            "atomic_note": content.strip(),
        }
