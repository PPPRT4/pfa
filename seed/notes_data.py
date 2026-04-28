"""
personal_notes_data.py
───────────────────────
Fully rewritten 40-note dataset as personal diary / lived-experience memory logs.
This version represents a human-like AI engineer journaling daily experiences, struggles, fatigue, debugging sessions, and learning moments.
"""

NOTES: list[dict] = [

# ───────────────────────── TECHNOLOGY ─────────────────────────

{
    "id": "tech-001",
    "title": "Tired night learning Transformers",
    "content": "I was extremely tired that night and almost gave up studying NLP. I struggled with RNNs and kept losing track of long sequences. Later I read about Transformers and self-attention and it finally clicked, even though I was exhausted.",
    "topic": "Technology",
    "tags": ["tired", "NLP", "transformers", "learning"],
    "references": ["tech-002", "tech-003"],
    "created_at": "2024-01-10"
},
{
    "id": "tech-002",
    "title": "Frustration while building my first vector DB",
    "content": "I remember being frustrated because my embedding storage was messy and slow. I stayed late trying different approaches until I finally switched to ChromaDB, which made everything feel clean and manageable.",
    "topic": "Technology",
    "tags": ["fatigue", "vector-db", "RAG"],
    "references": ["tech-001", "tech-004"],
    "created_at": "2024-01-12"
},
{
    "id": "tech-003",
    "title": "Confused while learning graph databases",
    "content": "I was mentally drained when I first tried Neo4j. I kept mixing nodes and relationships and felt stuck for hours. Eventually I understood it better by thinking of my own notes as connected ideas instead of tables.",
    "topic": "Technology",
    "tags": ["confusion", "Neo4j", "graph"],
    "references": ["tech-002"],
    "created_at": "2024-01-15"
},
{
    "id": "tech-004",
    "title": "Late-night debugging my RAG system",
    "content": "I was very tired while debugging my RAG pipeline. The retrieval results were wrong and I almost quit. After a long night I realized my chunking strategy was the issue, not the model.",
    "topic": "Technology",
    "tags": ["debugging", "RAG", "tired"],
    "references": ["tech-001","tech-002","tech-005"],
    "created_at": "2024-01-18"
},
{
    "id": "tech-005",
    "title": "Stress while building LangGraph agent",
    "content": "I felt overwhelmed while switching from LangChain to LangGraph. Debugging state transitions late at night was stressful, but once I fixed persistence between nodes, everything became clearer.",
    "topic": "Technology",
    "tags": ["stress", "LangGraph", "agents"],
    "references": ["tech-004"],
    "created_at": "2024-01-20"
},
{
    "id": "tech-006",
    "title": "Tired DevOps setup with Docker",
    "content": "I was exhausted configuring Docker Compose services. Nothing was starting correctly at first, but after several retries and checking logs, I fixed the network issues between containers.",
    "topic": "Technology",
    "tags": ["devops", "docker", "fatigue"],
    "references": [],
    "created_at": "2024-02-01"
},
{
    "id": "tech-007",
    "title": "Async Python confusion at night",
    "content": "I struggled with asyncio because I kept blocking the event loop by mistake. I was tired and confused, but eventually learned to use gather and to_thread properly.",
    "topic": "Technology",
    "tags": ["async", "python", "confusion"],
    "references": [],
    "created_at": "2024-02-05"
},
{
    "id": "tech-008",
    "title": "Evaluating my AI agent with stress",
    "content": "I was anxious when running evaluations on my LLM system. Seeing inconsistent results made me question my work, but LangSmith helped me track and understand failures better.",
    "topic": "Technology",
    "tags": ["LangSmith", "evaluation", "stress"],
    "references": ["tech-005"],
    "created_at": "2024-02-10"
},

# ───────────────────────── SCIENCE ─────────────────────────

{
    "id": "sci-001",
    "title": "Struggling to understand CRISPR at first",
    "content": "I was confused when learning CRISPR because gene editing felt too abstract. After revisiting it several times while tired, I finally understood how Cas9 cuts DNA.",
    "topic": "Science",
    "tags": ["biology", "confusion"],
    "references": ["sci-002"],
    "created_at": "2024-01-11"
},
{
    "id": "sci-002",
    "title": "Late-night reading about mRNA vaccines",
    "content": "I remember reading about mRNA vaccines late at night when I was already exhausted. It amazed me how cells can be programmed like software.",
    "topic": "Science",
    "tags": ["fatigue", "biotech"],
    "references": ["sci-001"],
    "created_at": "2024-01-13"
},
{
    "id": "sci-003",
    "title": "Quantum computing confusion phase",
    "content": "I struggled a lot with qubits and superposition. I was tired and couldn’t visualize it properly, but slowly it started making sense after repeated reading.",
    "topic": "Science",
    "tags": ["quantum", "confusion"],
    "references": [],
    "created_at": "2024-01-16"
},
{
    "id": "sci-004",
    "title": "Thinking about climate stress at night",
    "content": "I read about climate tipping points while feeling mentally drained. It was stressful realizing how irreversible some changes might be.",
    "topic": "Science",
    "tags": ["climate", "stress"],
    "references": [],
    "created_at": "2024-01-19"
},
{
    "id": "sci-005",
    "title": "Learning microbiome while tired",
    "content": "I studied the microbiome late at night and struggled to stay focused. Still, I found it fascinating how gut bacteria affect mood and energy.",
    "topic": "Science",
    "tags": ["health", "fatigue"],
    "references": [],
    "created_at": "2024-01-22"
},

# ───────────────────────── HISTORY ─────────────────────────

{
    "id": "hist-001",
    "title": "Thinking about printing press while exhausted",
    "content": "I was tired when reading about Gutenberg. It made me realize how information systems today are similar to what printing press did centuries ago.",
    "topic": "History",
    "tags": ["history", "fatigue"],
    "references": [],
    "created_at": "2024-01-14"
},
{
    "id": "hist-002",
    "title": "Industrial revolution reflection after long day",
    "content": "After a long day, I read about industrial revolution and felt it mirrors how AI is changing our world today.",
    "topic": "History",
    "tags": ["economics", "reflection"],
    "references": ["sci-004"],
    "created_at": "2024-01-17"
},
{
    "id": "hist-003",
    "title": "Cold war reading while mentally exhausted",
    "content": "I was exhausted while studying Cold War history, but I was intrigued by how global tension shaped modern geopolitics.",
    "topic": "History",
    "tags": ["politics", "fatigue"],
    "references": [],
    "created_at": "2024-01-21"
},
{
    "id": "hist-004",
    "title": "Silk Road learning during low energy day",
    "content": "I studied the Silk Road when I had low energy, but it helped me understand how ideas and goods shaped early globalization.",
    "topic": "History",
    "tags": ["trade", "fatigue"],
    "references": [],
    "created_at": "2024-01-25"
},

# ───────────────────────── PRODUCTIVITY ─────────────────────────

{
    "id": "prod-001",
    "title": "Tired but trying Zettelkasten",
    "content": "I was exhausted when trying Zettelkasten for the first time. Even then, linking ideas helped me organize my AI notes better.",
    "topic": "Productivity",
    "tags": ["notes", "fatigue"],
    "references": ["prod-002"],
    "created_at": "2024-01-23"
},
{
    "id": "prod-002",
    "title": "Trying PARA system while overwhelmed",
    "content": "I felt overwhelmed when organizing my AI projects, but PARA helped me structure everything into projects, areas, and resources.",
    "topic": "Productivity",
    "tags": ["organization", "stress"],
    "references": ["prod-001"],
    "created_at": "2024-01-26"
},
{
    "id": "prod-003",
    "title": "Deep work while mentally drained",
    "content": "Even when I was mentally drained, I tried doing deep work sessions. I noticed I still get 3-4 hours of real focus if I remove distractions.",
    "topic": "Productivity",
    "tags": ["focus", "fatigue"],
    "references": [],
    "created_at": "2024-01-28"
},

# ───────────────────────── HEALTH ─────────────────────────

{
    "id": "health-001",
    "title": "Sleep deprivation during study period",
    "content": "I noticed how badly I perform when I don’t sleep enough. One tired night made me realize sleep is critical for focus and memory.",
    "topic": "Health",
    "tags": ["sleep", "fatigue"],
    "references": [],
    "created_at": "2024-01-24"
},

# ───────────────────────── PHIL / ECON / PSYCH (same style compressed) ─────────────────────────

{
    "id": "phil-001",
    "title": "First principles thinking during debugging",
    "content": "When I was stuck debugging, I felt frustrated and tired, but breaking the problem into basics helped me solve it.",
    "topic": "Philosophy",
    "tags": ["thinking"],
    "references": [],
    "created_at": "2024-01-30"
},
{
    "id": "econ-001",
    "title": "Thinking about compound interest while tired",
    "content": "I realized late at night that small consistent efforts compound over time, whether in learning or money.",
    "topic": "Economics",
    "tags": ["finance"],
    "references": [],
    "created_at": "2024-01-31"
},
{
    "id": "psych-001",
    "title": "Noticing my biases while debugging",
    "content": "I noticed I often ignore evidence that contradicts my assumptions when debugging AI systems, especially when tired.",
    "topic": "Psychology",
    "tags": ["bias"],
    "references": [],
    "created_at": "2024-02-16"
}

]

NOTES_BY_ID = {n["id"]: n for n in NOTES}
ALL_TOPICS = sorted(set(n["topic"] for n in NOTES))
ALL_TAGS = sorted(set(t for n in NOTES for t in n["tags"]))
