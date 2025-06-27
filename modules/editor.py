# modules/ai_editor.py

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables.")

# Gemini 1.5 Flash model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


def review_chapter(text: str, chapter_title: str) -> str:
    """
    AI provides final editorial review.
    """
    prompt = f"""
You are a professional literary editor.

Review the chapter titled "{chapter_title}" and provide feedback on:
1. Clarity and flow
2. Grammar and tone
3. Style and narrative
4. Suggestions for improvement

Be concise and actionable.
--- BEGIN CHAPTER ---
{text}
--- END CHAPTER ---
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def rewrite_chapter(original_text: str, ai_review: str, human_feedback: str, chapter_title: str) -> str:
    """
    Rewrite chapter based on AI + Human feedback.
    """
    prompt = f"""
You are an AI Editor helping improve a chapter titled "{chapter_title}".

Use both:
- AI editorial suggestions
- Human editor notes

--- ORIGINAL CHAPTER ---
{original_text}

--- AI REVIEW ---
{ai_review}

--- HUMAN FEEDBACK ---
{human_feedback}

--- TASK ---
Revise the original chapter using both inputs.
Maintain characters, plot, and style. Focus on improving readability, tone, and structure.
Output only the updated chapter, no comments or explanation.
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def save_draft(text: str, folder: str, iteration: int, chapter_title: str):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{chapter_title.lower().replace(' ', '_')}_v{iteration}_{timestamp}.txt"
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def run_editor_loop(spun_path: str, ai_review_path: str, draft_folder: str, final_output_path: str):
    """
    Loop through human/AI feedback and editing until user says stop.
    Save all intermediate versions in draft folder.
    Only save final to 'final' folder when confirmed.
    """
    chapter_title = Path(spun_path).stem.replace("_", " ").title()

    # Load spun input
    with open(spun_path, "r", encoding="utf-8") as f:
        current_text = f.read()

    # Load initial AI review
    with open(ai_review_path, "r", encoding="utf-8") as f:
        ai_review = f.read()

    iteration = 1
    while True:
        print(f"\n🔁 ITERATION {iteration}")
        print("📄 Current AI Review:\n")
        print(ai_review)
        print("\n✏️ Enter human feedback (blank line to end input):\n")

        # Human feedback input
        human_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            human_lines.append(line)
        human_feedback = "\n".join(human_lines)

        # Rewrite with both AI + human feedback
        updated_text = rewrite_chapter(current_text, ai_review, human_feedback, chapter_title)

        # Review the updated version
        ai_review = review_chapter(updated_text, chapter_title)

        # Save draft version
        draft_path = save_draft(updated_text, draft_folder, iteration, chapter_title)
        print(f"💾 Draft version saved to: {draft_path}")

        print("\n🧠 Updated AI Review:\n")
        print(ai_review)

        # Ask user to continue or finalize
        print("\n✅ Do you want to make more changes? (y/n): ", end="")
        user_choice = input().strip().lower()
        if user_choice == "n":
            # Finalize and save to final output
            os.makedirs(os.path.dirname(final_output_path), exist_ok=True)
            with open(final_output_path, "w", encoding="utf-8") as f:
                f.write(f"{chapter_title} (Final Edited)\n\n{updated_text}")
            final_review_path = final_output_path.replace(".txt", "_final_review.txt")
            with open(final_review_path, "w", encoding="utf-8") as f:
                f.write(f"{chapter_title} - Final AI Review\n\n{ai_review}")
            print(f"\n🎉 Final version saved to: {final_output_path}")
            print(f"🧠 Final review saved to: {final_review_path}")
            break
        else:
            # Continue loop
            current_text = updated_text
            iteration += 1


# ✅ Run as script
if __name__ == "__main__":
    spun_file = "data/spun/chapter1_spun.txt"
    ai_review_file = "data/reviews/chapter1_review.txt"
    drafts_folder = "data/drafts/"
    final_output_file = "data/final/chapter1_final.txt"

    run_editor_loop(spun_file, ai_review_file, drafts_folder, final_output_file)
