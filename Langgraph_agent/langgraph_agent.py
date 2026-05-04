from langgraph.graph import StateGraph, START, END
from ai.neo4j import search_graph
from ai.notes_ai import chercher_notes
from google import genai
from typing import TypedDict, List, Optional
from groq import Groq
from langchain_core.tracers import LangChainTracer
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
import time

def safe_generate(prompt, model="llama-3.3-70b-versatile", retries=3):
    for i in range(retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content

        except Exception as e:
            print(f"[Groq retry {i+1}] {e}")
            time.sleep(2 ** i)

    return "ERROR: Groq failed after retries"



class GraphState(TypedDict, total=False):
    query: str
    queries: List[str]
    docs: List[str]
    answer: str
    is_good: bool
    history: List[str]
    mode: str


# ---------------- NODES ----------------
def decide_tool(state):
    query = state["query"]

    prompt = f"""

If the question needs external knowledge → SEARCH
If it can be answered directly → DIRECT

    Query: {query}
Return ONLY:
SEARCH
or
DIRECT
No punctuation. No explanation.

   
    """

    text = safe_generate(prompt)

    return {"mode": text.strip()}


def route(state):
    return state["mode"]

def retrieve(state):
    queries = state.get("queries", [state.get("query", "")])
    vector_docs = []
    graph_docs = []
    for q in queries:
        vector_docs.extend(chercher_notes(q))
        graph_docs.extend(search_graph(q))
    return {"docs": vector_docs + graph_docs}


def generate(state):
    query = state.get("query", "")
    docs = state.get("docs", [])
    history = state.get("history", [])

    context = "\n".join(docs)
    history_text = "\n".join(history)

    prompt = f"""
    You are an AI second brain assistant.

     Conversation history:
    {history_text}

    Use ONLY these notes:
    {context}

    Question:
    {query}

    Rules:
    - Do NOT rewrite the question
    - Do NOT suggest new queries
    - Do NOT explain query improvement
    - Do not answer with a single word. 
    - Keep responses concise but slightly descriptive.
    - Answer clearly
    - If unrelated, say that u dont have enough information to answer because you are talking to a human do not give a signe word
    """

    answer = safe_generate(prompt)

    new_history = history + [
        f"User: {query}",
        f"Assistant: {answer}"
    ]

    return {"answer": answer,  "query": query, "docs": docs, "history": new_history}



def evaluate(state):
    docs = state.get("docs", [])
    answer = state.get("answer", "")

    context = "\n".join(docs)

    prompt = f"""
Is this answer supported by the notes?

Notes:
{context}

Answer:
{answer}

Return ONLY valid JSON:
{{
  "supported": true
}}
"""

    text = safe_generate(prompt)

    try:
        # clean possible markdown formatting
        text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)
        supported = result.get("supported", False)

    except Exception as e:
        print("[evaluate error]", e)
        supported = False

    return {
        "is_good": supported,
        "query": state.get("query", ""),
        "docs": docs,
        "answer": answer
    }

def rewrite(state):
    query = state.get("query", "")

    prompt = f"""
    Improve this query for better search:
    {query}
    """

    text = safe_generate(prompt)

    return {"query": text}

def plan(state):
    query = state.get("query", "")

    prompt = f"""
    Break this question into 2-3 smaller search queries.
        Return ONLY valid JSON array:
["query1", "query2"]
   Query: {query}


    """

    text = safe_generate(prompt)

    try:
        text = text.replace("```json", "").replace("```", "").strip()
        queries = json.loads(text)
    except:
        queries = [query]

    return {"queries": queries}


def decision(state):
    return "good" if state["is_good"] else "good"

# ---------------- GRAPH ----------------

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("plan", plan)
    graph.add_node("decide_tool", decide_tool)
    graph.add_node("retrieve", retrieve)

    graph.add_node("generate", generate)
    graph.add_node("evaluate", evaluate)
    graph.add_node("rewrite", rewrite)

    graph.set_entry_point("plan")

    graph.add_edge("plan", "decide_tool")
    graph.add_conditional_edges(
        "decide_tool",
        route,
        {
            "SEARCH": "retrieve",
            "DIRECT": "generate"
        }
    )
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        decision,
        {
            "good": END,
            "bad": "rewrite"
        }
    )

    graph.add_edge("rewrite", "plan")

    return graph.compile()