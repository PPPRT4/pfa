import os
import re
from functools import lru_cache
from neo4j import GraphDatabase
from dotenv import load_dotenv


load_dotenv()

ALLOWED_RELATIONS = {"RELATED_TO", "DEPENDS_ON", "PART_OF"}


def normalize_uri(uri: str | None):
    return (uri or "bolt://localhost:7687").replace(
        "host.docker.internal", "localhost"
    )


@lru_cache(maxsize=1)
def get_driver():
    return GraphDatabase.driver(
        normalize_uri(os.getenv("NEO4J_URI")),
        auth=(
            os.getenv("NEO4J_USERNAME", "neo4j"),
            os.getenv("NEO4J_PASSWORD", "neo4j_password"),
        ),
    )


def safe_rel_type(rel: str) -> str:
    rel = (rel or "").upper().strip()
    return rel if rel in ALLOWED_RELATIONS else "RELATED_TO"


def save_to_neo4j(note_id: str, payload: dict):
    driver = get_driver()

    title = payload.get("title", "Untitled")
    text = payload.get("atomic_note", "")
    topic = payload.get("topic", "Idea")

    entities = payload.get("entities", []) or []
    relations = payload.get("relations", []) or []

    with driver.session() as session:

        # NOTE NODE
        session.run(
            """
            MERGE (n:Note {id: $id})
            SET n.title = $title,
                n.text = $text,
                n.topic = $topic
            """,
            id=str(note_id),
            title=title,
            text=text,
            topic=topic,
        )

        # ENTITIES
        for e in entities:
            session.run(
                """
                MERGE (ent:Entity {name: $name})
                WITH ent
                MATCH (n:Note {id: $id})
                MERGE (n)-[:MENTIONS]->(ent)
                """,
                name=str(e),
                id=str(note_id),
            )

        # RELATIONS
        for r in relations:
            if not isinstance(r, dict):
                continue

            src = r.get("source")
            dst = r.get("target")
            rel = safe_rel_type(r.get("type"))

            if not src or not dst:
                continue

            session.run(
                f"""
                MATCH (a:Entity {{name: $src}})
                MATCH (b:Entity {{name: $dst}})
                MERGE (a)-[:{rel}]->(b)
                """,
                src=str(src),
                dst=str(dst),
            )



def search_graph(query: str, limit: int = 5):
    """
    Simple graph search:
    - matches notes by title
    - matches entities by name
    - returns connected context
    """

    driver = get_driver()

    cypher = """
    MATCH (n:Note)
    WHERE toLower(n.title) CONTAINS toLower($q)
       OR toLower(n.text) CONTAINS toLower($q)

    OPTIONAL MATCH (n)-[:MENTIONS]->(e:Entity)
    OPTIONAL MATCH (e)-[r]->(e2:Entity)

    RETURN n.title AS title,
           n.text AS text,
           collect(DISTINCT e.name) AS entities,
           collect(DISTINCT type(r)) AS relations
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(cypher, q=query, limit=limit)

        docs = []
        for record in result:
            text = f"""
Title: {record["title"]}
Text: {record["text"]}
Entities: {record["entities"]}
Relations: {record["relations"]}
"""
            docs.append(text.strip())

        return docs