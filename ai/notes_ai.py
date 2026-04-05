from sentence_transformers import SentenceTransformer
import chromadb

# Setup
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("notes")

def ajouter_note(id, texte):
    vecteur = model.encode(texte).tolist()
    collection.add(documents=[texte], embeddings=[vecteur], ids=[id])
    print(f"✅ Note ajoutée : {texte}")

def chercher_notes(question, nb_resultats=3):
    vecteur = model.encode(question).tolist()
    resultats = collection.query(query_embeddings=[vecteur], n_results=nb_resultats)
    print(f"\n🔍 Recherche : '{question}'")
    for doc in resultats["documents"][0]:
        print(f"  → {doc}")