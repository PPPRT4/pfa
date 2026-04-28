import os
import re
from functools import lru_cache

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


def _normalize_neo4j_uri(uri: str | None) -> str:
    if not uri:
        return "bolt://localhost:7687"
    # On Linux hosts, host.docker.internal often doesn't resolve.
    return uri.replace("host.docker.internal", "localhost")


@lru_cache(maxsize=1)
def _get_driver():
    uri = _normalize_neo4j_uri(os.getenv("NEO4J_URI"))
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "neo4j_password")
    return GraphDatabase.driver(uri, auth=(username, password))


_REL_TYPE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _safe_rel_type(value: str, default: str = "RELATED_TO") -> str:
    value = (value or "").strip().upper()
    if _REL_TYPE_RE.match(value):
        return value
    return default


def save_to_neo4j(note_id, data: dict):
    driver = _get_driver()
    note_text = str(data.get("atomic_note") or data.get("content") or "").strip()
    topic = str(data.get("topic") or "Idea").strip()
    title = str(data.get("title") or "Untitled").strip()

    entities = data.get("entities") or []
    if not isinstance(entities, list):
        entities = []
    entities = [str(e).strip() for e in entities if str(e).strip()]

    relations = data.get("relations") or []
    if not isinstance(relations, list):
        relations = []

    with driver.session() as session:
        session.run(
            """
            MERGE (n:Note {id: $id})
            SET n.title = $title,
                n.text = $text,
                n.topic = $topic
            """,
            id=str(note_id),
            title=title,
            text=note_text,
            topic=topic,
        )

        for e in entities:
            session.run(
                """
                MERGE (ent:Entity {name: $name})
                WITH ent
                MATCH (n:Note {id: $id})
                MERGE (n)-[:MENTIONS]->(ent)
                """,
                name=e,
                id=str(note_id),
            )

        for r in relations:
            if not isinstance(r, dict):
                continue
            src = str(r.get("source", "")).strip()
            dst = str(r.get("target", "")).strip()
            rel_type = _safe_rel_type(str(r.get("type", "")))
            if not src or not dst:
                continue

            cypher = (
                "MATCH (a:Entity {name: $src}) "
                "MATCH (b:Entity {name: $dst}) "
                f"MERGE (a)-[:{rel_type}]->(b)"
            )
            session.run(cypher, src=src, dst=dst)