# modules/chromadb_store.py

import os
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
import uuid

# Setup ChromaDB storage location
CHROMA_PATH = "data/chroma_db"
os.makedirs(CHROMA_PATH, exist_ok=True)

# ✅ Updated ChromaDB client setup (no more Settings)
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Collection for storing chapter versions
collection = client.get_or_create_collection(name="book_versions")


def store_version(version_text: str, chapter_id: str, version_type: str, author: str, notes: str = "") -> str:
    """
    Store a version of a chapter in ChromaDB with metadata and embeddings.
    """
    version_id = str(uuid.uuid4())
    embedding = embedding_model.encode(version_text).tolist()

    metadata = {
        "chapter_id": chapter_id,
        "version_type": version_type,  # e.g., spun, edited, final
        "author": author,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }

    collection.add(
        documents=[version_text],
        embeddings=[embedding],
        ids=[version_id],
        metadatas=[metadata]
    )

    print(f"✅ Stored version: {version_id} (type: {version_type})")
    return version_id


def search_versions(query: str, top_k: int = 3):
    """
    Perform semantic search over stored versions.
    """
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    matches = []
    for i in range(len(results["ids"][0])):
        matches.append({
            "id": results["ids"][0][i],
            "score": results["distances"][0][i],
            "metadata": results["metadatas"][0][i],
            "text": results["documents"][0][i][:500] + "..."
        })

    return matches


def list_all_versions():
    """
    List metadata of all stored versions.
    """
    all_data = collection.get()
    print("\n📜 All Stored Versions:")
    for i, meta in enumerate(all_data["metadatas"]):
        print(f"{i+1}. ID: {all_data['ids'][i]}")
        print(f"   Chapter: {meta['chapter_id']}")
        print(f"   Type: {meta['version_type']} | Author: {meta['author']}")
        print(f"   Time: {meta['timestamp']}")
        print(f"   Notes: {meta.get('notes', '')}")
        print("-" * 50)


def delete_all_versions():
    """
    Clear the entire collection (dev only).
    """
    client.delete_collection("book_versions")
    print("⚠️ All versions deleted from ChromaDB.")


# ✅ Example CLI Test
if __name__ == "__main__":
    example_text = "This is a test version of Chapter 1 after review."
    version_id = store_version(example_text, "chapter1", "edited", "AI+Human", "test entry")

    print("\n🔍 Search result for 'reviewed chapter':")
    results = search_versions("reviewed chapter")
    for r in results:
        print(f"\n📄 ID: {r['id']}")
        print(f"Score: {r['score']:.4f}")
        print(f"Metadata: {r['metadata']}")
        print(f"Text Preview: {r['text']}")
