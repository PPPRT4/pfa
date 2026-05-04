"""Quick manual smoke-test for the LangGraph agent.

This file is often run directly from the `Langgraph_agent/scripts` folder.
When run that way, the repository root isn't on `sys.path`, which breaks
absolute imports like `Langgraph_agent.*`.
"""

from __future__ import annotations

try:
    # Preferred when executed as a module: `python -m Langgraph_agent.scripts.test_agent`
    from ..langgraph_agent import build_graph  # type: ignore
except Exception:  # pragma: no cover
    # Fallback when executed as a script: `python Langgraph_agent/scripts/test_agent.py`
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo_root))

    from Langgraph_agent.langgraph_agent import build_graph


if __name__ == "__main__":
    app = build_graph()

    # Initial input state
    initial_state = {
        "query": "does my mom hates anything?",
        "history": []
    }

    # Run the graph
    result = app.invoke(initial_state)

    # Print outputs
    print("\n=== FINAL ANSWER ===\n")
    print(result.get("answer"))

    print("\n=== MODE ===\n")
    print(result.get("mode"))

    print("\n=== QUERIES (if planning used) ===\n")
    print(result.get("queries"))

    print("\n=== DOCS USED ===\n")
    print(result.get("docs"))

    print("\n=== HISTORY ===\n")
    print(result.get("history"))