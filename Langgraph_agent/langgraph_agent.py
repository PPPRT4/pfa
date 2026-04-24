from langgraph.graph import StateGraph, START, END
# from ai.notes_ai import chercher_notes
from google import genai
from typing import TypedDict, List, Optional
from groq import Groq
from langchain_core.tracers import LangChainTracer
from dotenv import load_dotenv
import os
from mcp import ClientSession
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

import traceback

async def mcp_search_notes(query):
    try:
        server = StdioServerParameters(
            command="python",
            args=["ai/mcp_notes_server.py"]
        )

        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "search_notes",
                    {"query": query, "k": 3}
                )

                return result.content

    except Exception as e:
        print("🔥 FULL ERROR:")
        traceback.print_exc()
        return str(e)

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
    Should I:
    1. Search notes
    2. Answer directly

    Query: {query}

    Reply: SEARCH or DIRECT
    """

    text = safe_generate(prompt)

    return {"mode": text.strip()}


def route(state):
    return state["mode"]

def retrieve(state):
    queries = state.get("queries", [state.get("query", "")])

    all_docs = []

    for q in queries:
        docs = asyncio.run(mcp_search_notes(q))
        all_docs.extend(docs)

    return {"docs": all_docs}


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

    Answer clearly.
    """

    answer = safe_generate(prompt)

    new_history = history + [
        f"User: {query}",
        f"Assistant: {answer}"
    ]

    return {"answer": answer,  "query": query, "docs": docs, "history": new_history}
def rerank(state):
    docs = state.get("docs", [])
    query = state.get("query", "")

    prompt = f"""
    Select the most relevant notes for this query:

    Query: {query}

    Notes:
    {docs}

    Return top 3.
    """

    text = safe_generate(prompt)
    return {"docs": text.split("\n")}

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

    Reply ONLY YES or NO.
    """

    text = safe_generate(prompt)

    return {"is_good": "YES" in text.upper(),  "query": state.get("query", ""), "docs": docs, "answer": answer}


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
    Break this question into 2-3 smaller search queries:
    {query}

    Return as a list.
    """

    text = safe_generate(prompt)

    queries = text.split("\n")
    return {"queries": queries}


def decision(state):
    return "good" if state["is_good"] else "bad"

# ---------------- GRAPH ----------------

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("plan", plan)
    graph.add_node("decide_tool", decide_tool)
    graph.add_node("retrieve", retrieve)
    graph.add_node("rerank", rerank)
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
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "generate")
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