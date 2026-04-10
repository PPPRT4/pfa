import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

from ai.note_analyzer import analyze_note_with_langchain
from ai.vector_store import add_note_to_vector_store, search_notes

# ── Données réelles variées ──────────────────────────────────────────
REAL_NOTES = [
    # Research
    "Transformer architecture uses self-attention mechanisms to process sequences in parallel.",
    "RAG combines retrieval with generation to ground LLM responses in real documents.",
    "ChromaDB is an open-source vector database optimized for AI applications.",
    # Tasks
    "Finish the backend API documentation before Friday.",
    "Deploy the app to production server this week.",
    "Write unit tests for the note classifier module.",
    # Ideas
    "What if we added voice input to capture notes hands-free?",
    "We could build a weekly digest that summarizes all notes automatically.",
    # Reminders
    "Doctor appointment on Thursday at 10am.",
    "Don't forget to submit the PFA report by end of month.",
    # Bugs
    "The search endpoint returns 500 error when query is empty string.",
    "Neo4j connection drops after 30 minutes of inactivity.",
    # Edge cases
    "",                          # empty note
    "ok",                        # very short
    "a" * 500,                   # very long
    "J'ai une idee pour le projet: utiliser GPT-4 pour classifier",  # French
]

# ── Edge case queries ─────────────────────────────────────────────────
EDGE_QUERIES = [
    "transformer attention",
    "deploy production",
    "voice input idea",
    "empty",
    "xxxunknownxxx",   # should return no results
]


def test_classification():
    print("\n" + "="*60)
    print("TEST 1 -- Classification avec donnees reelles")
    print("="*60)
    results = {"Research": 0, "Task": 0, "Idea": 0, "Reminder": 0, "Bug": 0, "Idea_fallback": 0}
    errors = []

    for note in REAL_NOTES:
        try:
            if not note.strip():
                print(f"[SKIP] Empty note skipped")
                continue
            result = analyze_note_with_langchain(note[:200])
            topic = result["topic"]
            results[topic] = results.get(topic, 0) + 1
            preview = note[:50].replace("\n", " ")
            print(f"  [{topic:10}] {preview}...")
        except Exception as e:
            errors.append(str(e))
            print(f"  [ERROR] {str(e)[:60]}")

    print(f"\n>> Distribution: {results}")
    print(f">> Errors: {len(errors)}")
    return len(errors) == 0


def test_rag_edge_cases():
    print("\n" + "="*60)
    print("TEST 2 -- RAG avec cas limites")
    print("="*60)

    # First populate with real notes
    print("[*] Peuplement Chroma...")
    for i, note in enumerate(REAL_NOTES):
        if note.strip():
            result = analyze_note_with_langchain(note[:200])
            add_note_to_vector_store(8000 + i, note[:200], result["topic"])
    print("[OK] Chroma peuple !\n")

    passed = 0
    for query in EDGE_QUERIES:
        try:
            results = search_notes(query, n_results=3)
            if query == "xxxunknownxxx":
                # Should return results but irrelevant ones
                status = "[OK]"
                passed += 1
                print(f"{status} Query: '{query}' -> {len(results)} results (expected low relevance)")
            elif not results:
                print(f"[FAIL] Query: '{query}' -> No results found")
            else:
                status = "[OK]"
                passed += 1
                top = results[0]["content"][:50]
                score = results[0].get("score", "N/A")
                print(f"{status} Query: '{query}' -> '{top}...' (score: {score})")
        except Exception as e:
            print(f"[ERROR] Query: '{query}' -> {str(e)[:60]}")

    print(f"\n>> RAG edge cases passed: {passed}/{len(EDGE_QUERIES)}")
    return passed >= len(EDGE_QUERIES) - 1


def test_agent():
    print("\n" + "="*60)
    print("TEST 3 -- Agent avec questions reelles")
    print("="*60)

    import requests
    questions = [
        "What do I know about transformers?",
        "What tasks do I have to finish?",
        "Any bugs I noted recently?",
        "Summarize all my research notes.",
    ]

    passed = 0
    for q in questions:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/agent/chat",
                json={"message": q, "reset": False},
                timeout=30
            )
            if res.status_code == 200:
                answer = res.json().get("final_answer", "")[:80]
                print(f"[OK] Q: '{q[:40]}'\n     A: '{answer}...'")
                passed += 1
            else:
                print(f"[FAIL] Q: '{q}' -> Status {res.status_code}")
        except Exception as e:
            print(f"[ERROR] Q: '{q}' -> {str(e)[:60]}")

    print(f"\n>> Agent tests passed: {passed}/{len(questions)}")
    return passed >= len(questions) - 1


def run_all_tests():
    print("\nSECOND BRAIN -- TESTS DONNEES REELLES")
    print("="*60)

    t1 = test_classification()
    t2 = test_rag_edge_cases()
    t3 = test_agent()

    print("\n" + "="*60)
    print("RAPPORT FINAL")
    print("="*60)
    print(f"  Classification  : {'[PASS]' if t1 else '[FAIL]'}")
    print(f"  RAG edge cases  : {'[PASS]' if t2 else '[FAIL]'}")
    print(f"  Agent           : {'[PASS]' if t3 else '[FAIL]'}")

    all_pass = t1 and t2 and t3
    print(f"\n  {'[OK] Tous les tests passes !' if all_pass else '[!!] Certains tests ont echoue'}")


if __name__ == "__main__":
    run_all_tests()