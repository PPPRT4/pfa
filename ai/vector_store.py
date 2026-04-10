import chromadb
from chromadb.utils import embedding_functions

EMBED_MODEL = "all-MiniLM-L6-v2"

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path="./chroma_db")
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
        _collection = _client.get_or_create_collection(
            name="notes",
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def add_note_to_vector_store(note_id: int, content: str, topic: str = "") -> None:
    col = _get_collection()
    col.upsert(
        ids=[str(note_id)],
        documents=[content],
        metadatas=[{"topic": topic, "note_id": note_id}]
    )


def search_notes(query: str, n_results: int = 3) -> list[dict]:
    col = _get_collection()
    count = col.count()
    if count == 0:
        return []
    n = min(n_results, count)
    results = col.query(
        query_texts=[query],
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )
    output = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        output.append({
            "note_id": meta.get("note_id"),
            "content": doc,
            "topic": meta.get("topic", ""),
            "score": round(1 - dist, 4)
        })
    return output