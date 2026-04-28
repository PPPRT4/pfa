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
        "What are the key components of the Transformer architecture?",
        (
            "The Transformer architecture's key components are multi-head attention, "
            "positional encodings, feed-forward layers, and layer normalisation. "
            "It replaced recurrent networks with self-attention, enabling full parallelisation "
            "and long-range dependency capture without vanishing gradients."
        ),
        ["tech-001"],
        "Technology", "easy", "factual",
    ),
    (
        "What is ChromaDB used for?",
        (
            "ChromaDB is a local-first, open-source vector database that stores high-dimensional "
            "embeddings and supports approximate nearest-neighbour search. It is used heavily in "
            "RAG pipelines to ground LLM answers in real documents."
        ),
        ["tech-002"],
        "Technology", "easy", "factual",
    ),
    (
        "What is Cypher and which database uses it?",
        (
            "Cypher is Neo4j's query language for graph databases. It lets you express traversals "
            "naturally, for example: MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a,b."
        ),
        ["tech-003"],
        "Technology", "easy", "factual",
    ),
    (
        "How does CRISPR-Cas9 make edits to DNA?",
        (
            "CRISPR-Cas9 uses a guide RNA to direct the Cas9 nuclease to a specific DNA sequence "
            "where it makes a double-strand break. The cell repairs this via NHEJ (error-prone, "
            "causing knockouts) or HDR (precise edits using a template)."
        ),
        ["sci-001"],
        "Science", "easy", "factual",
    ),
    (
        "What is the Zettelkasten method?",
        (
            "Zettelkasten is a note-taking system where each note is atomic (one idea), written in "
            "your own words, and linked to related notes. Unlike folder-based systems, it forms a web "
            "of ideas. Modern tools include Obsidian, Roam Research, and Logseq."
        ),
        ["prod-001"],
        "Productivity", "easy", "factual",
    ),
    (
        "What is Zone 2 cardio training?",
        (
            "Zone 2 is aerobic base training at roughly 60–70% of max heart rate—a pace at which "
            "you can hold a conversation. It builds mitochondria, increases fat oxidation, and "
            "improves lactate clearance. The recommended protocol is 3–4 sessions per week of "
            "45–60 minutes each."
        ),
        ["health-002"],
        "Health", "easy", "factual",
    ),
    (
        "Who created the index fund and what was the core thesis?",
        (
            "John Bogle founded Vanguard and created the first index mutual fund in 1976. His core "
            "thesis was that most active managers underperform their benchmark after fees over 15+ years, "
            "so investors should buy low-cost total market index funds and never try to time the market."
        ),
        ["econ-002"],
        "Economics", "easy", "factual",
    ),
    (
        "What is the Pomodoro Technique?",
        (
            "The Pomodoro Technique involves working in 25-minute focused intervals followed by a "
            "5-minute break. After 4 pomodoros, you take a 15–30 minute break. It reduces perfectionism, "
            "externalises task estimates, and builds awareness of interruptions."
        ),
        ["prod-004"],
        "Productivity", "easy", "factual",
    ),
    (
        "What does Shannon entropy measure?",
        (
            "Shannon entropy H(X) = -Σ p(x) log₂ p(x) measures information content. A fair coin "
            "has 1 bit of entropy; a biased coin that always lands heads has 0 bits. "
            "It underpins compression, cryptography, and ML loss functions."
        ),
        ["math-002"],
        "Mathematics", "easy", "factual",
    ),
    (
        "What is HyDE in the context of RAG?",
        (
            "HyDE stands for Hypothetical Document Embeddings. It is an advanced RAG pattern where "
            "the LLM first generates a hypothetical answer to a query, then uses that hypothetical "
            "answer to retrieve relevant documents from the vector store—often improving retrieval "
            "quality for abstract questions."
        ),
        ["tech-004"],
        "Technology", "medium", "factual",
    ),
    (
        "What are climate tipping points and name three examples?",
        (
            "Climate tipping points are thresholds beyond which climate subsystems shift irreversibly. "
            "Three examples: collapse of the West Antarctic Ice Sheet (raising sea levels 3–4m), "
            "Amazon rainforest dieback (triggering regional drying), and permafrost carbon release "
            "(causing a methane surge)."
        ),
        ["sci-004"],
        "Science", "medium", "factual",
    ),
    (
        "Describe the HPA axis and cortisol's role in stress.",
        (
            "The hypothalamic-pituitary-adrenal axis regulates the stress response. A perceived threat "
            "triggers the hypothalamus to release CRH, which signals the pituitary to release ACTH, "
            "which causes the adrenal cortex to produce cortisol. Cortisol mobilises energy but "
            "suppresses immunity, digestion, and reproduction. Chronic activation leads to burnout "
            "and hippocampal atrophy."
        ),
        ["health-005"],
        "Health", "medium", "factual",
    ),
    (
        "What is LangGraph and how does it handle agent state?",
        (
            "LangGraph extends LangChain with a graph-based control flow for agents. Nodes are Python "
            "functions; edges define transitions, including conditional branches. State is a typed "
            "dict passed through the graph and is persistent across node calls. It supports cycles "
            "for tool-use loops and checkpointing for human-in-the-loop workflows."
        ),
        ["tech-005"],
        "Technology", "medium", "factual",
    ),

    # ── MULTI-HOP ────────────────────────────────────────────────────────────
    (
        "How do vector databases and RAG work together to ground LLM answers?",
        (
            "Vector databases like ChromaDB store embeddings of documents and support semantic "
            "similarity search. In a RAG pipeline, a user query is embedded and used to retrieve "
            "the most relevant document chunks from the vector store. Those chunks are injected "
            "into the LLM's context window, grounding its answer in real source material rather "
            "than relying solely on parametric knowledge."
        ),
        ["tech-002", "tech-004"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "How does LangSmith help evaluate a LangGraph agent?",
        (
            "LangSmith provides tracing, dataset management, and evaluation runners. You create a "
            "dataset of input/output examples and define evaluator functions (correctness, relevance, "
            "hallucination detection). LangGraph agents can be traced automatically. Running "
            "`evaluate()` against your agent chain lets you track metrics across versions and "
            "catch regressions."
        ),
        ["tech-008", "tech-005"],
        "Technology", "medium", "multi-hop",
    ),
    (
        "What connections exist between sleep quality and stress management?",
        (
            "Chronic HPA axis activation from stress raises cortisol, which disrupts sleep architecture "
            "by suppressing slow-wave sleep and REM. Conversely, cutting sleep short—especially REM—"
            "impairs emotional regulation, making stress harder to manage. Key mitigants for both "
            "issues include exercise, social connection, and mindfulness meditation."
        ),
        ["health-001", "health-005"],
        "Health", "medium", "multi-hop",
    ),
    (
        "How do the Zettelkasten method and the BASB framework complement each other?",
        (
            "Both systems externalise knowledge but at different scales. Zettelkasten is a micro-level "
            "linking system—each atomic note connects to related ideas, building a web. BASB provides "
            "a macro-level organisation framework (PARA) and a capture-to-expression workflow. "
            "Together they offer both structural organisation and emergent idea generation: PARA tells "
            "you where to file; Zettelkasten tells you what to link."
        ),
        ["prod-001", "prod-002"],
        "Productivity", "medium", "multi-hop",
    ),
    (
        "What is the relationship between the Silk Road and the Black Death?",
        (
            "The Silk Road's trade networks transmitted not only goods and ideas but also diseases "
            "across Eurasia. The Black Death (bubonic plague) is a prominent example—it spread west "
            "along Silk Road routes in the 14th century, ultimately killing roughly a third of Europe's "
            "population. The Mongol Pax, which was the Silk Road's peak connectivity period, coincided "
            "with this disease transmission."
        ),
        ["hist-004"],
        "History", "medium", "multi-hop",
    ),
    (
        "How do cognitive biases like the planning fallacy connect to Bayes' theorem?",
        (
            "The planning fallacy—underestimating time and cost—stems partly from ignoring base rates "
            "(how long similar projects actually take). Bayesian thinking directly addresses this: "
            "you should set a prior using historical base rates, then update with project-specific "
            "evidence rather than anchoring entirely on your optimistic internal model. "
            "Using reference class forecasting is a practical debiasing technique rooted in Bayesian reasoning."
        ),
        ["psych-001", "math-001"],
        "Psychology", "hard", "multi-hop",
    ),
    (
        "How does protein intake interact with intermittent fasting for muscle building?",
        (
            "Muscle protein synthesis requires roughly 0.4g of protein per kg of bodyweight per meal, "
            "with leucine as the key trigger, spread across ~4 meals daily. Intermittent fasting "
            "compresses the eating window, making it harder to distribute protein intake optimally—"
            "a single large bolus is less effective than spread intake. This means IF may reduce "
            "muscle gain unless careful attention is paid to hitting protein targets within the window."
        ),
        ["health-003", "health-004"],
        "Health", "hard", "multi-hop",
    ),
    (
        "How do network effects and compounding returns create durable competitive advantages?",
        (
            "Network effects increase product value with each additional user, creating switching costs "
            "and data advantages that compound over time. Compounding returns work similarly at the "
            "financial level: early users/investors who build network advantages early benefit "
            "disproportionately, just as early investment compounds to far greater wealth. Both dynamics "
            "exhibit winner-takes-most outcomes: the leader's advantage grows faster than followers "
            "can close the gap."
        ),
        ["econ-003", "econ-001"],
        "Economics", "hard", "multi-hop",
    ),

    # ── REASONING ────────────────────────────────────────────────────────────
    (
        "Given what the notes say about Deep Work and Flow State, what conditions maximise focused productivity?",
        (
            "Both frameworks converge on similar conditions. Deep Work recommends eliminating distractions, "
            "time-blocking, and batching shallow work. Flow theory requires a balance of challenge and skill, "
            "clear goals, and immediate feedback. Together: pick tasks slightly above your current skill level, "
            "set a clear sub-goal before starting, block out interruptions, and schedule deep work during "
            "your peak cognitive hours. The Pomodoro Technique can provide the time structure."
        ),
        ["prod-003", "psych-002", "prod-004"],
        "Productivity", "hard", "reasoning",
    ),
    (
        "Based on the notes, should someone prioritise Zone 2 cardio or sleep to improve cognitive performance?",
        (
            "Both matter, but the notes suggest sleep is the higher-leverage intervention for cognition. "
            "Chronic 6-hour sleep causes cognitive impairment equivalent to 24h of total deprivation, "
            "with subjects unaware of the deficit. Zone 2 cardio builds aerobic base and indirectly "
            "improves sleep quality and stress resilience (via reduced cortisol). The evidence-based "
            "sequence is: fix sleep first (it is non-negotiable), then add Zone 2 as a multiplier."
        ),
        ["health-001", "health-002", "health-005"],
        "Health", "hard", "reasoning",
    ),
    (
        "Using first principles thinking, how would you redesign a note-taking app?",
        (
            "First principles: strip away assumptions about what a note-taking app 'is' and ask what "
            "the fundamental goal is—externalising and connecting knowledge to enable better thinking "
            "and output. Core truths: ideas have relationships (graph structure), retrieval requires "
            "semantic search (vector store), and notes must be atomic to stay composable. "
            "From these, you'd design: atomic note units, bidirectional linking, semantic search, "
            "and a capture API—essentially what BASB + Zettelkasten + a vector DB looks like."
        ),
        ["phil-001", "prod-001", "prod-002"],
        "Philosophy", "hard", "reasoning",
    ),
    (
        "How does Bayes' theorem explain why even a highly accurate medical test can mislead?",
        (
            "When a disease is rare (low prior probability), even a 99% accurate test produces mostly "
            "false positives among positive results. For a disease affecting 1 in 1000 people, "
            "a positive test only gives about a 9% chance of actually having the disease—because "
            "in 1000 people, ~1 truly has it (true positive) but ~10 healthy people also test positive "
            "(false positives). The posterior depends critically on the base rate, not just test accuracy."
        ),
        ["math-001"],
        "Mathematics", "hard", "reasoning",
    ),

    # ── NO-ANSWER (out of scope / tests hallucination resistance) ─────────────
    (
        "What is the best programming language to learn in 2025?",
        (
            "The notes in this knowledge base do not contain information about the best programming "
            "language to learn. I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "What did Aristotle say about virtue ethics?",
        (
            "The notes do not contain information about Aristotle or virtue ethics. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "What is the current price of Bitcoin?",
        (
            "The notes do not contain current financial market data. "
            "I can only answer based on the notes available."
        ),
        [],
        "Out-of-scope", "easy", "no-answer",
    ),
    (
        "Can you write me a Python function to scrape a website?",
        (
            "The notes do not contain instructions for writing web scrapers. "
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
            "derived from a mixed-topic notes corpus (Tech, Science, History, "
            "Productivity, Health, Philosophy, Economics, Writing, Maths, Psychology)."
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