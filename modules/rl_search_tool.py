# modules/rl_search_tool.py

from rl_search import rl_weighted_search

def rl_search_cli():
    print("🔎 RL-Enhanced Search Tool")

    while True:
        query = input("\nEnter search query (or 'exit'): ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        results = rl_weighted_search(query)
        if not results:
            print("😕 No results found.")
            continue

        print(f"\n🎯 Top Results for: '{query}'")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. 🆔 {r['id']}")
            print(f"   📘 Chapter: {r['metadata']['chapter_id']}")
            print(f"   ✍️ Author: {r['metadata']['author']} | Type: {r['metadata']['version_type']}")
            print(f"   🧠 RL Feedback: {len(r['metadata'].get('notes', ''))} notes")
            print(f"   🔍 Preview:\n   {r['text']}\n{'-'*50}")

if __name__ == "__main__":
    rl_search_cli()
