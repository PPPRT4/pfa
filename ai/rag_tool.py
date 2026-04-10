import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from langchain.tools import tool
from ai.vector_store import search_notes


@tool
def search_my_notes(query: str) -> str:
    """Search the user's personal notes for information relevant to the query.
    Use this tool when the user asks about something they might have noted before,
    or when you need context from their second brain."""
    results = search_notes(query, n_results=3)
    if not results:
        return "No relevant notes found."
    output = "Here are the most relevant notes:\n\n"
    for i, r in enumerate(results, 1):
        output += f"{i}. [Topic: {r['topic']}] (score: {r['score']})\n{r['content']}\n\n"
    return output