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
    docs=resultats["documents"][0]
    if isinstance(docs, str):
        docs = [docs]
    for doc in docs:
        print(f"  → {doc}")
    return docs

# TEST
#ajouter_note("1", "J'ai mal à la tête")
#ajouter_note("2", "J'ai une migraine terrible")
#ajouter_note("3", "Mon chat mange du poisson")
#ajouter_note("4", "Je suis fatigué aujourd'hui")

#chercher_notes("j'ai des douleurs à la tête")