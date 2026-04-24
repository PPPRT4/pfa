from fastmcp import FastMCP

from sentence_transformers import SentenceTransformer
import chromadb

# ---------------- MCP INIT ----------------
mcp = FastMCP("vector-mcp")

# ---------------- EMBEDDINGS ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- CHROMA DB ----------------
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("notes")

# ---------------- TOOL 1----------------
@mcp.tool()
def search_notes(query: str, k: int = 3):

    vector = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[vector],
        n_results=k
    )

    docs = results.get("documents", [[]])[0]

    return {
        "query": query,
        "results": docs
    }

# ---------------- TOOL 2 ----------------
@mcp.tool()
def add_note(id: str, text: str):

    vector = model.encode(text).tolist()

    collection.add(
        ids=[id],
        documents=[text],
        embeddings=[vector]
    )

    return {
        "status": "success",
        "id": id
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8005)