# modules/search_tool.py

from chromadb_store import search_versions, list_all_versions

def interactive_search():
    print("🔍 Welcome to Chapter Version Search Tool")
    print("1. Search by Semantic Query")
    print("2. List All Versions")
    print("3. Exit")

    while True:
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            query = input("\n🔎 Enter your semantic search query: ").strip()
            if not query:
                print("⚠️ Query cannot be empty.")
                continue

            results = search_versions(query)
            if not results:
                print("😕 No matching results found.")
                continue

            print(f"\n🎯 Top {len(results)} Results for: '{query}'\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. 🆔 ID: {r['id']}")
                print(f"   📘 Chapter: {r['metadata']['chapter_id']}")
                print(f"   ✍️ Author: {r['metadata']['author']} | Type: {r['metadata']['version_type']}")
                print(f"   🕓 Timestamp: {r['metadata']['timestamp']}")
                print(f"   📄 Notes: {r['metadata'].get('notes', '')}")
                print(f"   🔍 Preview:\n   {r['text']}\n{'-'*60}")

        elif choice == "2":
            list_all_versions()

        elif choice == "3":
            print("👋 Exiting search tool. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    interactive_search()
