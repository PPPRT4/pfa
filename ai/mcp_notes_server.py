from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer
import chromadb

mcp = FastMCP("notes-server")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("notes")


@mcp.tool()
def search_notes(query: str, k: int = 3):
    """Search notes using semantic similarity"""
    vector = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[vector],
        n_results=k
    )

    return results["documents"][0]


@mcp.tool()
def add_note(id: str, text: str, topic: str):
    vector = model.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[vector],
        ids=[id],
        metadatas=[{"topic": topic}]
    )
    return "added"


if __name__ == "__main__":
    mcp.run()