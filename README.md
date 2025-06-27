# 📚 AI-Powered Automated Book Publication Workflow

A fully automated pipeline to scrape book chapters from Wikisource, rewrite them with Gemini 1.5 Flash, refine with AI + human feedback loops, store versions with embeddings in ChromaDB, and retrieve the best edits using a Reinforcement Learning (RL) feedback system — all through an interactive Gradio interface.

---

## ✨ **Key Features**

- ✅ **Scraper**: Playwright grabs clean chapter text + screenshots from Wikisource.
- ✅ **AI Writer**: Spins raw text into new drafts using Google Gemini 1.5 Flash.
- ✅ **AI Reviewer**: Provides professional editorial feedback on style, tone, clarity.
- ✅ **Human-in-the-Loop**: Rewrite loop lets humans refine chapters until final.
- ✅ **ChromaDB**: Version control with embeddings for fast semantic search.
- ✅ **RL Feedback**: Users rate versions (1–5 stars) — best edits float to the top.
- ✅ **Gradio UI**: Single interface for scraping, editing, feedback, RL ranking.

---

## 📦 **Requirements**

- Python 3.12+
- Playwright (browsers must be installed)
- Gemini API key (set in `.env`)

Install dependencies:
```bash
pip install -r requirements.txt
```
Install Playwright browsers:
```bash

playwright install
```
Environment Setup
Create .env in the project root:
```bash
env

GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```
After all this setup just run 
```bash
python app2.py
```

🗂️ Usage Flow

1️⃣ Load & Auto Run: Paste a Wikisource URL → scrape → spin → review

2️⃣ Human Feedback Loop: Add your notes → AI rewrites → repeat until done

3️⃣ Final Save: Store version in ChromaDB, rate it ⭐⭐⭐⭐⭐ for RL feedback

4️⃣ RL Search: Search & rank best versions with hybrid semantic + RL scoring



📊 Architecture Diagram
```bash
mermaid

flowchart TD
    A[📎 Wikisource URL] --> B[🧩 Scraper (Playwright)]
    B --> C[✍️ AI Writer (Gemini Spin)]
    C --> D[🧠 AI Reviewer (Gemini Critique)]
    D --> E[🙋 Human Feedback]
    E --> F[📝 AI Editor Rewrite]
    F --> G[🗂️ ChromaDB Storage]
    G --> H[⭐ RL Feedback Loop]
    H --> I[🔍 RL-Weighted Search]
    E --> F --> E[🔁 Repeat until final]
```

## 📂 Module-wise Function Map

| 📁 Module            | 🧠 Function            | 🧾 Purpose                                      |
|---------------------|------------------------|------------------------------------------------|
| `scraper.py`        | `fetch_chapter`        | Scrape & clean text from Wikisource            |
| `ai_writer.py`      | `spin_chapter`         | Rewrite raw chapter using Gemini               |
| `ai_reviewer.py`    | `review_chapter`       | Provide AI editorial critique                  |
| `ai_editor.py`      | `rewrite_chapter`      | Rewrite using AI + human feedback              |
|                     | `review_chapter`       | Final review after editing                     |
| `chromadb_store.py` | `store_version`        | Save version with embeddings + metadata        |
|                     | `search_versions`      | Semantic search in ChromaDB                    |
|                     | `list_all_versions`    | Debug: list all stored versions                |
| `rl_selector.py`    | `add_feedback`         | Store user’s RL star rating                    |
|                     | `get_top_versions`     | Return top-ranked versions by RL score         |
| `rl_search.py`      | `rl_weighted_search`   | Hybrid semantic + RL score search              |
