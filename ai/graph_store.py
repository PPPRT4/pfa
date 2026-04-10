import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://4e08f10c.databases.neo4j.io"
NEO4J_USER = "4e08f10c"
NEO4J_PASSWORD = "yJAJRjQ_I9ogK3dCTLNw2bE-m6js2JDJ_0BR_dvV2Wk"
NEO4J_DATABASE = "4e08f10c"

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def get_session():
    return get_driver().session(database=NEO4J_DATABASE)


def add_note_to_graph(note_id: int, title: str, topic: str) -> None:
    with get_session() as session:
        session.run("""
            MERGE (n:Note {id: $id})
            SET n.title = $title, n.topic = $topic
            MERGE (t:Topic {name: $topic})
            MERGE (n)-[:BELONGS_TO]->(t)
        """, id=note_id, title=title, topic=topic)


def get_related_notes(topic: str) -> list[dict]:
    with get_session() as session:
        result = session.run("""
            MATCH (n:Note)-[:BELONGS_TO]->(t:Topic {name: $topic})
            RETURN n.id AS id, n.title AS title, n.topic AS topic
        """, topic=topic)
        return [dict(r) for r in result]


def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None