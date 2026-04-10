import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")

from ai.vector_store import search_notes, add_note_to_vector_store
from ai.note_analyzer import analyze_note_with_langchain

EVAL_NOTES = [
    {"content": "LangChain is a framework for building LLM applications.", "expected_topic": "Research"},
    {"content": "Neo4j stores data as nodes and relationships.", "expected_topic": "Research"},
    {"content": "I need to buy groceries tomorrow.", "expected_topic": "Task"},
    {"content": "I have a doctor appointment next Monday.", "expected_topic": "Reminder"},
    {"content": "What if we used embeddings to cluster user feedback?", "expected_topic": "Idea"},
]

EVAL_QUERIES = [
    {"query": "LangChain framework", "expected_in_results": "LangChain"},
    {"query": "graph database nodes", "expected_in_results": "Neo4j"},
    {"query": "doctor appointment", "expected_in_results": "doctor"},
]


def populate_chroma_for_eval():
    print("\n[*] Peuplement de Chroma avec les notes de test...")
    for i, item in enumerate(EVAL_NOTES):
        result = analyze_note_with_langchain(item["content"])
        add_note_to_vector_store(9000 + i, item["content"], result["topic"])
    print("[OK] Chroma peuple !")


def evaluate_classification():
    print("\n" + "="*50)
    print("EVALUATION 1 -- Classification des notes")
    print("="*50)
    correct = 0
    for item in EVAL_NOTES:
        result = analyze_note_with_langchain(item["content"])
        predicted = result["topic"]
        expected = item["expected_topic"]
        status = "[OK]" if predicted == expected else "[FAIL]"
        if predicted == expected:
            correct += 1
        print(f"{status} Attendu: {expected:10} | Predit: {predicted:10} | '{item['content'][:40]}...'")
    accuracy = correct / len(EVAL_NOTES) * 100
    print(f"\n>> Accuracy classification: {accuracy:.0f}% ({correct}/{len(EVAL_NOTES)})")
    return accuracy


def evaluate_rag():
    print("\n" + "="*50)
    print("EVALUATION 2 -- RAG (recherche semantique)")
    print("="*50)
    correct = 0
    for item in EVAL_QUERIES:
        results = search_notes(item["query"], n_results=3)
        found = any(
            item["expected_in_results"].lower() in r["content"].lower()
            for r in results
        )
        status = "[OK]" if found else "[FAIL]"
        if found:
            correct += 1
        top = results[0]["content"][:50] if results else "No results"
        print(f"{status} Query: '{item['query']:25}' | Top result: '{top}...'")
    recall = correct / len(EVAL_QUERIES) * 100
    print(f"\n>> RAG Recall@3: {recall:.0f}% ({correct}/{len(EVAL_QUERIES)})")
    return recall


def run_evaluation():
    print("\nSECOND BRAIN -- RAPPORT D'EVALUATION")
    print("="*50)
    populate_chroma_for_eval()
    acc = evaluate_classification()
    recall = evaluate_rag()
    print("\n" + "="*50)
    print("RESUME FINAL")
    print("="*50)
    print(f"  Classification accuracy : {acc:.0f}%")
    print(f"  RAG Recall@3            : {recall:.0f}%")
    overall = (acc + recall) / 2
    print(f"  Score global            : {overall:.0f}%")
    if overall >= 80:
        print("\n[OK] Systeme performant !")
    elif overall >= 60:
        print("\n[!!] Systeme correct, des ameliorations possibles.")
    else:
        print("\n[KO] Systeme a ameliorer.")


if __name__ == "__main__":
    run_evaluation()