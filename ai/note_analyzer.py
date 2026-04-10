import json, os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")
llm = ChatGroq(model="llama-3.3-70b-versatile")

ALLOWED_TOPICS = {"Idea", "Bug", "Reminder", "Task", "Research"}

TASK_KEYWORDS = ["acheter", "buy", "je dois", "commander", "todo", "finish", "complete", "submit", "send", "fix"]
REMINDER_KEYWORDS = ["medecin", "doctor", "rendez-vous", "appointment", "mal ", "douleur", "voir un", "reminder", "don't forget", "remember"]
RESEARCH_KEYWORDS = ["etudier", "apprendre", "research", "cours", "framework", "library", "algorithm",
                     "model", "llm", "database", "api", "architecture", "paper", "study", "learning",
                     "langchain", "vector", "embedding", "neural", "machine learning", "deep learning"]
IDEA_KEYWORDS = ["what if", "imagine", "maybe we", "idea", "could we", "proposal", "concept"]
BUG_KEYWORDS = ["bug", "error", "fix", "crash", "issue", "broken", "not working", "exception"]


def classify_by_keywords(content):
    text = content.lower()
    for kw in REMINDER_KEYWORDS:
        if kw in text: return "Reminder"
    for kw in TASK_KEYWORDS:
        if kw in text: return "Task"
    for kw in BUG_KEYWORDS:
        if kw in text: return "Bug"
    for kw in RESEARCH_KEYWORDS:
        if kw in text: return "Research"
    for kw in IDEA_KEYWORDS:
        if kw in text: return "Idea"
    return None


def analyze_note_with_langchain(content):
    keyword_topic = classify_by_keywords(content)
    if keyword_topic:
        return {"topic": keyword_topic, "atomic_note": content.strip()}
    try:
        messages = [
            SystemMessage(content="""You are a note classifier. Classify the note into exactly one topic.
Topics:
- Research: technical topics, frameworks, libraries, databases, AI, programming concepts
- Task: things to do, actions, todos
- Reminder: appointments, deadlines, medical, don't forget
- Idea: creative thoughts, proposals, what if scenarios
- Bug: errors, crashes, issues in code
Return ONLY valid JSON with no extra text."""),
            HumanMessage(content=f"Classify this note: {content}\nReturn: {{\"topic\": \"Task|Reminder|Idea|Bug|Research\", \"atomic_note\": \"one sentence summary\"}}")
        ]
        response = llm.invoke(messages)
        raw = (response.content or "").strip().strip("`").lstrip("json").strip()
        parsed = json.loads(raw)
        topic = parsed.get("topic", "Idea")
        if topic not in ALLOWED_TOPICS: topic = "Idea"
        return {"topic": topic, "atomic_note": parsed.get("atomic_note", content)}
    except:
        return {"topic": "Idea", "atomic_note": content}