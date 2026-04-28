"""
seed_neo4j_personal_memory.py
──────────────────────────────
Seeds Neo4j with a PERSONAL MEMORY / LIVED EXPERIENCE graph.

This version is designed for diary-style notes:
- fatigue, stress, confusion, debugging struggles
- emotional + experiential memory instead of factual knowledge

It turns Neo4j into a "cognitive memory graph".
"""

import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# ── import personal notes ─────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from personal_notes_data import NOTES   # ✅ FIXED IMPORT

load_dotenv()

NEO4J_URI      = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


# ──────────────────────────────────────────────────────────────────────────────
# Emotion / state inference (memory-style brain layer)
# ──────────────────────────────────────────────────────────────────────────────

def infer_mood_and_energy(note):
    text = (note.get("content", "") + note.get("title", "")).lower()
    tags = set(t.lower() for t in note.get("tags", []))

    if "tired" in text or "fatigue" in tags:
        mood = "tired"
    elif "stress" in text or "overwhelmed" in tags:
        mood = "stressed"
    elif "confus" in text:
        mood = "confused"
    elif "frustrat" in text:
        mood = "frustrated"
    elif "focus" in text:
        mood = "focused"
    else:
        mood = "neutral"

    energy_map = {
        "tired": "low",
        "stressed": "low",
        "frustrated": "low",
        "confused": "medium",
        "neutral": "medium",
        "focused": "high"
    }

    return mood, energy_map[mood]


# ──────────────────────────────────────────────────────────────────────────────
# Cypher constraints (Neo4j 5 compatible)
# ──────────────────────────────────────────────────────────────────────────────

CREATE_CONSTRAINTS = [
    "CREATE CONSTRAINT note_id IF NOT EXISTS FOR (n:Note) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
    "CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE",
]


UPSERT_NOTE = """
MERGE (n:Note {id: $id})
SET n.title = $title,
    n.content = $content,
    n.topic = $topic,
    n.created_at = $created_at,
    n.mood = $mood,
    n.energy_level = $energy_level
"""

UPSERT_TOPIC = """
MERGE (t:Topic {name: $topic})
WITH t
MATCH (n:Note {id: $note_id})
MERGE (n)-[:BELONGS_TO]->(t)
"""

UPSERT_TAG = """
MERGE (tag:Tag {name: $tag})
WITH tag
MATCH (n:Note {id: $note_id})
MERGE (n)-[:TAGGED]->(tag)
"""

UPSERT_REF = """
MATCH (a:Note {id: $from_id})
MATCH (b:Note {id: $to_id})
MERGE (a)-[:REFERENCES]->(b)
"""


# ──────────────────────────────────────────────────────────────────────────────
# Seed logic
# ──────────────────────────────────────────────────────────────────────────────

def seed(driver):
    with driver.session() as session:

        print("Creating constraints...")
        for c in CREATE_CONSTRAINTS:
            session.run(c)

        print(f"Upserting {len(NOTES)} personal memory notes...")

        for note in NOTES:

            mood, energy = infer_mood_and_energy(note)

            session.run(
                UPSERT_NOTE,
                id=note["id"],
                title=note.get("title", ""),
                content=note.get("content", ""),
                topic=note.get("topic", "Unknown"),
                created_at=note.get("created_at", ""),
                mood=mood,
                energy_level=energy,
            )

            session.run(
                UPSERT_TOPIC,
                topic=note.get("topic", "Unknown"),
                note_id=note["id"]
            )

            # tags (safe)
            for tag in note.get("tags", []):
                session.run(
                    UPSERT_TAG,
                    tag=tag,
                    note_id=note["id"]
                )

        print("Creating REFERENCES edges...")

        ref_count = 0

        for note in NOTES:
            refs = note.get("references", [])

            for ref_id in refs:
                session.run(
                    UPSERT_REF,
                    from_id=note["id"],
                    to_id=ref_id
                )
                ref_count += 1

        print(f"Done: {len(NOTES)} notes, {ref_count} references.")


# ──────────────────────────────────────────────────────────────────────────────
# Verification
# ──────────────────────────────────────────────────────────────────────────────

def verify(driver):
    with driver.session() as session:

        note_count = session.run("MATCH (n:Note) RETURN count(n) AS c").single()["c"]
        topic_count = session.run("MATCH (t:Topic) RETURN count(t) AS c").single()["c"]
        tag_count = session.run("MATCH (t:Tag) RETURN count(t) AS c").single()["c"]

        mood_dist = session.run("""
            MATCH (n:Note)
            RETURN n.mood AS mood, count(*) AS c
            ORDER BY c DESC
        """).data()

        print("\n── Personal Memory Graph ─────────────")
        print(f"Notes:  {note_count}")
        print(f"Topics: {topic_count}")
        print(f"Tags:   {tag_count}")

        print("\nMood distribution:")
        for row in mood_dist:
            print(f"  {row['mood']}: {row['c']}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Connecting to Neo4j at {NEO4J_URI}...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )

    try:
        driver.verify_connectivity()
        seed(driver)
        verify(driver)
    finally:
        driver.close()