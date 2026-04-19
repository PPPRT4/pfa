from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

# -----------------------------
# MCP HTTP CLIENT (FIXED)
# -----------------------------
MCP_URL = "http://localhost:8001"

def search_notes(query: str, k: int = 3):
    try:
        response = requests.post(
            f"{MCP_URL}/search_notes",
            json={"query": query, "k": k}
        )
        return response.json().get("results", [])
    except:
        return []

# -----------------------------
# STATE
# -----------------------------
class State(TypedDict):
    user_query: str
    search_queries: List[str]
    notes: List[str]
    answer: str

# -----------------------------
# LLM (GROQ)
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# -----------------------------
# PLANNER NODE
# -----------------------------
def planner_node(state: State):
    question = state["user_query"]

    prompt = f"""
Convert this question into short search queries.

Return ONLY a JSON list of strings.

Question: {question}
"""

    response = llm.invoke(prompt)

    try:
        queries = json.loads(response.content)
    except:
        queries = [question]

    return {"search_queries": queries}

# -----------------------------
# RETRIEVER NODE
# -----------------------------
def retriever_node(state: State):
    all_notes = []

    for q in state["search_queries"]:
        notes = search_notes(q, 3)
        all_notes.extend(notes)

    return {"notes": list(set(all_notes))}

# -----------------------------
# ANSWER NODE
# -----------------------------
def answer_node(state: State):
    question = state["user_query"]
    notes = state["notes"]

    context = "\n".join([f"- {n}" for n in notes])

    prompt = f"""
You are a second brain assistant.

You MUST answer ONLY using the notes.
If missing info, say:
"I don't have enough information in my notes."

NOTES:
{context}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)

    return {"answer": response.content}

# -----------------------------
# BUILD GRAPH
# -----------------------------
def build_agent():
    builder = StateGraph(State)

    builder.add_node("planner", planner_node)
    builder.add_node("retriever", retriever_node)
    builder.add_node("answer", answer_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "retriever")
    builder.add_edge("retriever", "answer")
    builder.add_edge("answer", END)

    return builder.compile(checkpointer=InMemorySaver())

# -----------------------------
# RUN AGENT
# -----------------------------
graph_app = build_agent()

def run_agent(query: str, thread_id: str = "1"):
    result = graph_app.invoke(
        {"user_query": query},
        config={"configurable": {"thread_id": thread_id}}
    )

    return result["answer"]

# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    print(run_agent("Explain AI in 1 sentence"))