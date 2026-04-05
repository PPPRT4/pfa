import json, os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

os.environ.setdefault("GROQ_API_KEY", "")
llm = ChatGroq(model="llama-3.3-70b-versatile")
ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}
TASK_KEYWORDS = ["acheter", "buy", "je dois", "commander"]
REMINDER_KEYWORDS = ["medecin", "doctor", "rendez-vous", "mal ", "douleur", "voir un"]
RESEARCH_KEYWORDS = ["etudier", "apprendre", "research", "cours"]

def classify_by_keywords(content):
    text = content.lower()
    for kw in REMINDER_KEYWORDS:
        if kw in text: return "Reminder"
    for kw in TASK_KEYWORDS:
        if kw in text: return "Task"
    for kw in RESEARCH_KEYWORDS:
        if kw in text: return "Research"
    return None

def analyze_note_with_langchain(content):
    keyword_topic = classify_by_keywords(content)
    if keyword_topic:
        return {"topic": keyword_topic, "atomic_note": content.strip()}
    try:
        messages = [
            SystemMessage(content="Classify. Return ONLY JSON."),
            HumanMessage(content=f"Classify: {content}\nReturn: {{\"topic\": \"Task|Reminder|Idea|Bug|Research\", \"atomic_note\": \"one sentence\"}}")
        ]
        response = llm.invoke(messages)
        raw = (response.content or "").strip().strip("`").lstrip("json").strip()
        parsed = json.loads(raw)
        topic = parsed.get("topic", "Idea")
        if topic not in ALLOWED_TOPICS: topic = "Idea"
        return {"topic": topic, "atomic_note": parsed.get("atomic_note", content)}
    except:
        return {"topic": "Idea", "atomic_note": content}
