"""
seed_langsmith.py
──────────────────
Creates a LangSmith evaluation dataset for the second-brain RAG agent.

Dataset name : "second_brain_eval_v1"
Each example : {
    "input":            user question,
    "expected_output":  gold answer derived from the notes,
    "metadata": {
        "source_note_ids": [...],   # which notes answer this question
        "topic":           str,
        "difficulty":      "easy" | "medium" | "hard",
        "eval_type":       "factual" | "multi-hop" | "reasoning" | "no-answer"
    }
}

Evaluation types covered
─────────────────────────
- factual      : single-hop fact retrieval
- multi-hop    : requires combining ≥2 notes
- reasoning    : requires inference on top of retrieved info
- no-answer    : question out-of-scope (tests hallucination resistance)

Requirements
─────────────
    pip install langsmith python-dotenv

Environment variables (or .env file)
─────────────────────────────────────
    LANGSMITH_API_KEY  = ls__...
    LANGSMITH_PROJECT  = second-brain        (optional, for tracing)
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client

sys.path.insert(0, os.path.dirname(__file__))
from notes_data import NOTES_BY_ID

load_dotenv()

DATASET_NAME = "second_brain_eval_v1"


# ── Evaluation examples ────────────────────────────────────────────────────────
# Format: (question, gold_answer, source_note_ids, topic, difficulty, eval_type)

EVAL_EXAMPLES = [
    # ── FACTUAL ──────────────────────────────────────────────────────────────
    (
        "What finally helped understand the Transformer architecture?",
        (
            "After struggling with RNNs and losing track of long sequences, reading about "
            "Transformers and self-attention made things click — even during an exhausted "
            "late-night study session."
        ),
        ["tech-001"],
        "Technology", "easy", "factual",
    ),
    (
        "What tool resolved the messy and slow embedding storage problem?",
        (
            "After staying late and trying different approaches, switching to ChromaDB made "
            "the embedding storage feel clean and manageable."
        ),
        ["tech-002"],
        "Technology", "easy", "factual",
    ),
    (
        "How did understanding Neo4j finally come together?",
        (
            "After hours of confusion mixing up nodes and relationships while mentally drained, "
            "it clicked by thinking of personal notes as connected ideas rather than tables."
        ),
        ["tech-003"],
        "Technology", "easy", "factual",
    ),
    (
        "What turned out to be the root cause of the broken RAG pipeline?",
        (
            "After a long and tiring debugging night where quitting almost happened, the issue "
            "was traced to the chunking strategy — not the model itself."
        ),
        ["tech-004"],
        "Technology", "easy", "factual",
    ),
    (
        "What made LangGraph finally click after the stressful transition from LangChain?",
        (
            "The turning point was fixing persistence between nodes. Once state was properly "
            "persisting across graph nodes, the overall system became much clearer."
        ),
        ["tech-005"],
        "Technology", "easy", "factual",
    ),
    (
        "What tool helped make sense of inconsistent LLM evaluation results?",
        (
            "LangSmith helped track and understand evaluation failures when running assessments "
            "on the LLM system and seeing inconsistent results."
        ),
        ["tech-008"],
        "Technology", "easy", "factual",
    ),
    (
        "What insight came from reading about the Silk Road during a low-energy day?",
        (
            "Even while fatigued, studying the Silk Road helped build an understanding of how "
            "ideas and goods shaped early globalization."
        ),
        ["hist-004"],
        "History", "easy", "factual",
    ),
    (
        "What personal observation came from experimenting with Zettelkasten while tired?",
        (
            "Even while exhausted, trying Zettelkasten for the first time showed that linking "
            "ideas helped organize AI notes more effectively."
        ),
        ["prod-001"],
        "Productivity", "easy", "factual",
    ),
    (
        "What did the PARA system help with when feeling overwhelmed?",
        (
            "When AI projects felt overwhelming, PARA helped structure everything into projects, "
            "areas, and resources — bringing a sense of order."
        ),
        ["prod-002"],
        "Productivity", "easy", "factual",
    ),
    (
        "What was noticed about focus during mentally drained deep work sessions?",
        (
            "Even when mentally drained, 3–4 hours of real focus was still achievable by "
            "removing distractions during deep work sessions."
        ),
        ["prod-003"],
        "Productivity", "easy", "factual",
    ),
    (
        "What personal lesson came from a night of poor sleep during the study period?",
        (
            "A single sleep-deprived night made it clear that sleep is critical for focus "
            "and memory — performance dropped noticeably without it."
        ),
        ["health-001"],
        "Health", "easy", "factual",
    ),
    (
        "What broader pattern was noticed while thinking about compound interest late at night?",
        (
            "Small consistent efforts compound over time — a principle that applies equally "
            "to learning and to money."
        ),
        ["econ-001"],
        "Economics", "easy", "factual",
    ),
    (
        "What cognitive bias was noticed while debugging AI systems?",
        (
            "A tendency to ignore evidence that contradicts existing assumptions while debugging "
            "AI systems — especially pronounced when tired."
        ),
        ["psych-001"],
        "Psychology", "easy", "factual",
    ),
    (
        "What did reading about mRNA vaccines inspire during a late exhausted night?",
        (
            "Reading about mRNA vaccines while already exhausted sparked the realization that "
            "cells can essentially be programmed like software."
        ),
        ["sci-002"],
        "Science", "easy", "factual",
    ),
    (
        "What did the Docker Compose setup experience teach about debugging infrastructure?",
        (
            "After exhausting retries with services failing to start, the fix came from carefully "
            "checking logs and tracking down network issues between containers."
        ),
        ["tech-006"],
        "Technology", "easy", "factual",
    ),

    # ── MULTI-HOP ────────────────────────────────────────────────────────────
    (
        "How did frustrations with NLP and vector databases connect during the early learning phase?",
        (
            "Struggling with RNNs and long-sequence problems led to discovering Transformers and "
            "self-attention. Around the same time, messy embedding storage problems led to "
            "discovering ChromaDB — both breakthroughs happened during exhausting late-night sessions "
            "and together formed the foundation for building a RAG pipeline."
        ),
        ["tech-001", "tech-002"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "How did the RAG debugging experience and the LangGraph transition relate to each other?",
        (
            "Debugging the RAG pipeline was a frustrating late-night experience that eventually "
            "revealed a chunking strategy issue. That foundation fed into the stressful transition "
            "to LangGraph, where fixing state persistence between nodes brought clarity — both "
            "experiences involved pushing through confusion to find a structural root cause."
        ),
        ["tech-004", "tech-005"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "How did the LangGraph agent work connect to the evaluation anxiety documented later?",
        (
            "Building the LangGraph agent was stressful, especially debugging state transitions. "
            "That same system was later evaluated using LangSmith, which surfaced inconsistent "
            "results that caused anxiety — but ultimately LangSmith's tracing made the failures "
            "understandable and traceable."
        ),
        ["tech-005", "tech-008"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "What connections exist between how note-taking systems were tried during difficult moments?",
        (
            "Both Zettelkasten and PARA were first tried during overwhelmed or exhausted states. "
            "Zettelkasten helped link AI ideas even while fatigued, while PARA helped create "
            "structural order when projects felt unmanageable. Together they addressed both "
            "the micro (linking ideas) and macro (organizing projects) levels of knowledge management."
        ),
        ["prod-001", "prod-002"],
        "Productivity", "medium", "multi-hop",
    ),
    (
        "How did CRISPR confusion and mRNA vaccine reading relate as back-to-back science learning experiences?",
        (
            "CRISPR initially felt too abstract and required multiple revisits while tired before "
            "the Cas9 DNA-cutting mechanism made sense. Shortly after, reading about mRNA vaccines "
            "while already exhausted actually felt inspiring — it reframed biology as programmable, "
            "similar to software. Both experiences showed that persistence through fatigue can "
            "eventually yield genuine insight."
        ),
        ["sci-001", "sci-002"],
        "Science", "medium", "multi-hop",
    ),
    (
        "How did the asyncio confusion and Docker fatigue reflect broader patterns in late-night engineering work?",
        (
            "Both the asyncio struggles (accidentally blocking the event loop) and the Docker Compose "
            "setup problems (container networking failures) happened during exhausted sessions and "
            "were resolved only by careful, methodical investigation — checking logs for Docker, "
            "and learning gather and to_thread for async Python. Both illustrate that infrastructure "
            "and concurrency bugs require patience that is hardest to maintain when tired."
        ),
        ["tech-007", "tech-006"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "How did first-principles thinking during debugging connect to noticing cognitive biases?",
        (
            "When stuck debugging, breaking the problem into basics helped cut through frustration "
            "and tiredness. This connects to the separately noticed pattern of ignoring contradictory "
            "evidence when tired — first-principles thinking is essentially a deliberate countermeasure "
            "to that confirmation bias, forcing a rebuild from facts rather than assumptions."
        ),
        ["phil-001", "psych-001"],
        "Philosophy", "hard", "multi-hop",
    ),

    # ── REASONING ────────────────────────────────────────────────────────────
    (
        "Based on the notes, what patterns emerge about how breakthroughs happen during exhausting learning sessions?",
        (
            "Across multiple notes, breakthroughs consistently came not by stopping when tired, but "
            "by pushing through with a shift in approach: Transformers clicked after giving up on RNNs, "
            "ChromaDB resolved the vector DB mess after trying many alternatives, and the RAG bug was "
            "found only after a long night of persistence. The pattern suggests that fatigue narrows "
            "focus, and breakthroughs often require reframing the problem rather than working harder "
            "on the wrong approach."
        ),
        ["tech-001", "tech-002", "tech-004"],
        "Technology", "hard", "reasoning",
    ),
    (
        "What does the notes history suggest about the relationship between tiredness and learning quality?",
        (
            "The notes repeatedly document learning happening during exhausted or stressed states — "
            "Transformers, CRISPR, Silk Road, Zettelkasten. In some cases (mRNA vaccines, compound "
            "interest) insights were still meaningful. However, the sleep deprivation note explicitly "
            "identifies poor sleep as damaging focus and memory. The implication is that incidental "
            "tiredness during study is survivable, but chronic sleep deprivation actively degrades "
            "the quality of learning and should be treated as a priority."
        ),
        ["health-001", "tech-001", "sci-002"],
        "Health", "hard", "reasoning",
    ),
    (
        "Based on the notes, how does the experience of building the second-brain system reflect the principles being learned?",
        (
            "There is a direct meta-connection: the notes document learning about RAG, vector databases, "
            "LangGraph, and LangSmith while simultaneously building a second-brain system using those "
            "exact tools. Struggles with chunking, state persistence, and evaluation all became "
            "first-hand experience that reinforced the theoretical understanding. The Zettelkasten and "
            "PARA notes add another layer — the organizational systems being studied were adopted "
            "to manage the very notes being taken about the project."
        ),
        ["tech-004", "tech-005", "tech-008", "prod-001", "prod-002"],
        "Technology", "hard", "reasoning",
    ),
    (
        "What does the pattern of late-night realizations in the notes suggest about when deep insights tend to occur?",
        (
            "Many of the most significant insights in the notes — compound interest compounding like "
            "learning, cells programmable like software, information systems mirroring the printing press — "
            "occurred during tired, late-night reading rather than structured study. This aligns with "
            "the deep work note, which found that real focus is possible even when drained if distractions "
            "are removed. The pattern suggests that low-stimulation, late-night contexts may reduce "
            "filtering and allow more cross-domain connections to surface."
        ),
        ["econ-001", "sci-002", "hist-001", "prod-003"],
        "Psychology", "hard", "reasoning",
    ),

    # ── NO-ANSWER (out of scope / tests hallucination resistance) ─────────────
    (
        "What is the recommended daily protein intake for muscle building?",
        (
            "The notes do not contain specific nutritional guidance or protein intake recommendations. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "What is the current state of quantum computing hardware?",
        (
            "The notes mention confusion while learning about qubits conceptually, but do not contain "
            "information about the current state of quantum hardware. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "What did Aristotle say about virtue ethics?",
        (
            "The notes do not contain any information about Aristotle or virtue ethics. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "What is the best way to negotiate a salary raise?",
        (
            "The notes do not contain information about salary negotiation. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "Can you summarise the plot of a recent science fiction novel?",
        (
            "The notes do not contain any book summaries or fiction content. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
]


# ── Seeding ────────────────────────────────────────────────────────────────────

def build_examples(eval_examples: list) -> list[dict]:
    examples = []
    for (question, gold_answer, source_ids, topic, difficulty, eval_type) in eval_examples:
        examples.append({
            "inputs": {"question": question},
            "outputs": {"answer": gold_answer},
            "metadata": {
                "source_note_ids": source_ids,
                "topic": topic,
                "difficulty": difficulty,
                "eval_type": eval_type,
            },
        })
    return examples


def seed():
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "LANGSMITH_API_KEY not set. "
            "Get yours at https://smith.langchain.com → Settings → API Keys"
        )

    client = Client(api_key=api_key)
    examples = build_examples(EVAL_EXAMPLES)

    # Delete existing dataset to allow idempotent re-runs
    existing = [d for d in client.list_datasets() if d.name == DATASET_NAME]
    if existing:
        client.delete_dataset(dataset_id=existing[0].id)
        print(f"Deleted existing dataset '{DATASET_NAME}'.")

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "Evaluation dataset for the second-brain RAG agent. "
            "Contains factual, multi-hop, reasoning, and out-of-scope questions "
            "derived from a personal diary-style notes corpus covering Technology, "
            "Science, History, Productivity, Health, Philosophy, Economics, and Psychology."
        ),
    )
    print(f"Created dataset '{DATASET_NAME}' (id={dataset.id}).")

    # Batch-create examples
    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        metadata=[e["metadata"] for e in examples],
        dataset_id=dataset.id,
    )

    print(f"Added {len(examples)} examples.")
    return dataset


def print_summary():
    by_type: dict[str, int] = {}
    by_diff: dict[str, int] = {}
    for _, _, _, _, diff, etype in EVAL_EXAMPLES:
        by_type[etype] = by_type.get(etype, 0) + 1
        by_diff[diff]  = by_diff.get(diff, 0) + 1

    print("\n── Dataset summary ──────────────────────────")
    print(f"  Total examples: {len(EVAL_EXAMPLES)}")
    print("  By eval_type:")
    for k, v in sorted(by_type.items()):
        print(f"    {k:12s}: {v}")
    print("  By difficulty:")
    for k, v in sorted(by_diff.items()):
        print(f"    {k:8s}: {v}")


if __name__ == "__main__":
    print_summary()
    dataset = seed()
    print(f"\nDataset URL: https://smith.langchain.com/datasets/{dataset.id}")