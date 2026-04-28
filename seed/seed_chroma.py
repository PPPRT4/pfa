from sentence_transformers import SentenceTransformer
import chromadb
from notes_data import NOTES

# ── model ─────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2")

# ── chroma client ─────────────────────
client = chromadb.HttpClient(host="localhost", port=8010)
collection = client.get_or_create_collection("notes")

def seed():
    print("Seeding ChromaDB...")

    texts = [note["content"] for note in NOTES]
    embeddings = model.encode(texts).tolist()

    ids = [note["id"] for note in NOTES]
    metadatas = [
        {
            "title": note["title"],
            "topic": note["topic"],
            "tags": ",".join(note["tags"]),
            "created_at": note["created_at"]
        }
        for note in NOTES
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Inserted {len(NOTES)} notes into ChromaDB")

if __name__ == "__main__":
    seed()