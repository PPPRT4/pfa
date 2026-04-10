from langgraph.graph import StateGraph, START, END
from ai.notes_ai import chercher_notes
from google import genai
from typing import TypedDict, List, Optional


client = genai.Client()




class GraphState(TypedDict, total=False):
    query: str
    docs: List[str]
    answer: str
    is_good: bool


# ---------------- NODES ----------------

def retrieve(state):
    query = state.get("query", "")
    docs = chercher_notes(query) if query else []
    return {"docs": docs, "query": query}


def generate(state):
    query = state.get("query", "")
    docs = state.get("docs", [])

    context = "\n".join(docs)

    prompt = f"""
    You are an AI second brain assistant.

    Use ONLY these notes:
    {context}

    Question:
    {query}

    Answer clearly.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {"answer": response.text,  "query": query, "docs": docs}


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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {"is_good": "YES" in response.text.upper(),  "query": state.get("query", ""), "docs": docs, "answer": answer}


def rewrite(state):
    query = state.get("query", "")

    prompt = f"""
    Improve this query for better search:
    {query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {"query": response.text}


# ---------------- GRAPH ----------------

def decision(state):
    return "good" if state["is_good"] else "bad"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_node("evaluate", evaluate)
    graph.add_node("rewrite", rewrite)

    graph.set_entry_point("retrieve")


    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    #graph.add_edge("generate", "evaluate")

    #graph.add_conditional_edges(
     #   "evaluate",
      #  decision,
       # {
        #    "good": "__end__",
         #   "bad": "rewrite"
        #}
    #)

    #graph.add_edge("rewrite", "retrieve")

    return graph.compile()