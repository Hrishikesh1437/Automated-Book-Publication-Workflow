# pipeline.py

from scraper import fetch_chapter
from ai_writer import spin_from_file
from ai_reviewer import review_from_file
from editor import run_editor_loop
from chromadb_store import store_version

import os

def run_full_pipeline(chapter_url: str, chapter_id: str):
    print("🔗 Fetching original text...")
    fetch_chapter(chapter_url, chapter_id)

    input_path = f"data/raw/{chapter_id}.txt"
    spun_path = f"data/spun/{chapter_id}_spun.txt"
    review_path = f"data/reviews/{chapter_id}_review.txt"
    final_path = f"data/final/{chapter_id}_final.txt"

    print("🌀 Running AI writer...")
    spin_from_file(input_path, spun_path)

    print("🔍 AI reviewing spun version...")
    review_from_file(spun_path, review_path)

    print("👨‍💻 Launching human-in-the-loop editor...")
    run_ai_editor_pipeline(spun_path, review_path, "data/drafts/", final_path)

    print("💾 Storing final version in ChromaDB...")
    with open(final_path, "r", encoding="utf-8") as f:
        final_text = f.read()

    store_version(
        version_text=final_text,
        chapter_id=chapter_id,
        version_type="final",
        author="AI+Human",
        notes="Final approved version after editing loop"
    )

    print("✅ Pipeline complete!")

# Test run
if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter = "chapter1"
    run_full_pipeline(url, chapter)
