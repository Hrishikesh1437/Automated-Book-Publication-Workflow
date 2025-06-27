# app.py

import gradio as gr
import os
from urllib.parse import urlparse
from modules.scraper import fetch_chapter
from modules.ai_writer import spin_chapter
from modules.ai_reviewer import review_chapter
from modules.editor import rewrite_chapter, review_chapter as final_review
from modules.chromadb_store import store_version
from modules.rl_selector import RLVersionSelector
from modules.rl_search import rl_weighted_search

session = {
    "chapter_id": "",
    "chapter_title": "",
    "original": "",
    "spun": "",
    "review": "",
    "edited_versions": [],
    "final": ""
}

def extract_chapter_id(url: str) -> str:
    last = url.strip().split("/")[-1]
    return last.replace("Chapter_", "chapter").replace("chapter_", "chapter").lower()

def auto_pipeline(url: str):
    try:
        chapter_id = extract_chapter_id(url)
        session["chapter_id"] = chapter_id
        session["chapter_title"] = chapter_id.replace("_", " ").title()

        # Step 1: Scrape
        fetch_chapter(url, chapter_id)
        path = f"data/raw/{chapter_id}.txt"
        with open(path, "r", encoding="utf-8") as f:
            session["original"] = f.read()

        # Step 2: Spin
        session["spun"] = spin_chapter(session["original"], session["chapter_title"])

        # Step 3: Review
        session["review"] = review_chapter(session["spun"], session["chapter_title"])

        return session["original"], session["spun"], session["review"]
    except Exception as e:
        return "", "", f"❌ Error: {str(e)}"

def rewrite_with_feedback(human_feedback: str):
    if not human_feedback.strip():
        return "❗ Please enter feedback before rewriting.", ""

    new_version = rewrite_chapter(
        original_text=session["original"],
        ai_review=session["review"],
        human_feedback=human_feedback,
        chapter_title=session["chapter_title"]
    )

    session["edited_versions"].append(new_version)
    session["final"] = new_version

    new_review = final_review(new_version, session["chapter_title"])
    return new_version, new_review

def save_final(notes: str):
    if not session["final"]:
        return "⚠️ No final version found."

    version_id = store_version(
        version_text=session["final"],
        chapter_id=session["chapter_id"],
        version_type="final",
        author="AI+Human",
        notes=notes
    )
    return f"✅ Final version stored with ID: {version_id}"

def show_rl_weighted_versions(query: str):
    results = rl_weighted_search(query, top_k=5)

    if not results:
        return "❌ No results found."

    output = []
    for r in results:
        output.append(
            f"🆔 {r['id']}\n"
            f"📘 {r['metadata']['chapter_id']} | {r['metadata']['version_type']} | {r['metadata']['author']}\n"
            f"🧠 RL Notes: {r['metadata'].get('notes', '')}\n"
            f"📄 Preview:\n{r['text'][:300]}...\n{'-'*60}"
        )
    return "\n\n".join(output)


with gr.Blocks() as demo:
    gr.Markdown("## 📘 AI-Powered Book Editor (Auto Pipeline + Feedback Loop)")

    with gr.Tab("1️⃣ Load & Auto Run (Scraper → Spin → Review)"):
        url = gr.Textbox(label="Wikisource Chapter URL")
        run_btn = gr.Button("🚀 Run Auto Pipeline")
        original = gr.Textbox(label="Original Chapter", lines=10)
        spun = gr.Textbox(label="AI-Spun Version", lines=10)
        review = gr.Textbox(label="AI Review", lines=8)
        run_btn.click(fn=auto_pipeline, inputs=[url], outputs=[original, spun, review])

    with gr.Tab("2️⃣ Human Feedback & Rewriting Loop"):
        feedback = gr.Textbox(label="💬 Enter your feedback (edit suggestions)", lines=4)
        loop_btn = gr.Button("🔁 Apply Feedback and Rewrite")
        edited = gr.Textbox(label="Edited Version", lines=10)
        new_review = gr.Textbox(label="Updated AI Review", lines=8)
        loop_btn.click(fn=rewrite_with_feedback, inputs=[feedback], outputs=[edited, new_review])

    with gr.Tab("3️⃣ Final Save"):
        notes = gr.Textbox(label="Optional notes for this version")
        save_btn = gr.Button("💾 Save to ChromaDB")
        result = gr.Textbox(label="Save Status")
        save_btn.click(fn=save_final, inputs=[notes], outputs=[result])

    with gr.Tab("4️⃣ RL Search Results"):
        query = gr.Textbox(label="Search query (RL top scoring)")
        search_btn = gr.Button("🔍 Show Top Versions")
        rl_results = gr.Textbox(label="Top RL Versions", lines=10)
        search_btn.click(fn=search_rl, inputs=[query], outputs=[rl_results])

demo.launch()
