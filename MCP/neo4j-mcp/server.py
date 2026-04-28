from fastmcp import FastMCP
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("neo4j-knowledge-graph")

# -----------------------------
# Neo4j Driver
# -----------------------------
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(
        os.getenv("NEO4J_USER", "neo4j"),
        os.getenv("NEO4J_PASSWORD", "password")
    )
)

# -----------------------------
# TOOL 1: Create Note
# -----------------------------
@mcp.tool()
def create_note(note_id: str, text: str, topic: str = "Idea"):
    """Create a note node"""
    with driver.session() as session:
        session.run("""
        MERGE (n:Note {id: $id})
        SET n.text = $text,
            n.topic = $topic
        """, id=note_id, text=text, topic=topic)

    return {"status": "ok", "note_id": note_id}


# -----------------------------
# TOOL 2: Add Entity
# -----------------------------
@mcp.tool()
def add_entity(note_id: str, entity: str):
    """Link entity to note"""
    with driver.session() as session:
        session.run("""
        MERGE (e:Entity {name: $entity})
        WITH e
        MATCH (n:Note {id: $id})
        MERGE (n)-[:MENTIONS]->(e)
        """, entity=entity, id=note_id)

    return {"status": "ok", "entity": entity}


# -----------------------------
# TOOL 3: Add Relation
# -----------------------------
@mcp.tool()
def add_relation(src: str, relation: str, dst: str):
    """Create relation between entities"""
    with driver.session() as session:
        session.run(f"""
        MERGE (a:Entity {{name: $src}})
        MERGE (b:Entity {{name: $dst}})
        MERGE (a)-[:{relation}]->(b)
        """, src=src, dst=dst)

    return {"status": "ok", "relation": relation}


# -----------------------------
# TOOL 4: Query Graph
# -----------------------------
@mcp.tool()
def query_graph(entity: str):
    """Get neighborhood of an entity"""
    with driver.session() as session:
        result = session.run("""
        MATCH (e:Entity {name: $entity})-[r]-(n)
        RETURN e.name AS entity, type(r) AS relation, n.name AS connected
        """, entity=entity)

        return [record.data() for record in result]


# -----------------------------
# TOOL 5: Multi-hop expansion
# -----------------------------
@mcp.tool()
def expand_graph(entity: str, depth: int = 2):
    """Multi-hop graph traversal"""
    with driver.session() as session:
        result = session.run("""
        MATCH (e:Entity {name: $entity})-[*1..2]-(n)
        RETURN DISTINCT n.name AS node
        """, entity=entity)

        return [r["node"] for r in result]


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    mcp.run()