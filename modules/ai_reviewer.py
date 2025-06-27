import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables.")


genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


def review_chapter(text: str, chapter_title: str = "Chapter 1") -> str:
    """
    Uses Gemini 1.5 Flash to generate a professional editorial review of the given chapter.
    """
    prompt = f"""
You are a professional literary editor working for a top-tier publishing house.

Please critically review the rewritten chapter titled "{chapter_title}" and provide editorial feedback in the following sections:

1. **Overall Impression** – What worked, what didn’t, and how it felt overall.
2. **Clarity and Language** – Were the sentences easy to follow and expressive?
3. **Narrative Flow and Pacing** – Did the story progress naturally and stay engaging?
4. **Grammar and Syntax** – Any errors, awkward phrasing, or inconsistencies?
5. **Emotional Tone and Style** – Was the tone appropriate and the emotion clear?
6. **Historical/Cultural Authenticity** – Any mismatches or risks of anachronism?
7. **Suggestions for Improvement** – Specific, actionable, helpful feedback.

Avoid rewriting the chapter, but be detailed, honest, and constructive in critique.

--- BEGIN CHAPTER ---
{text}
--- END CHAPTER ---
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f" Review error: {e}")
        return ""


def review_from_file(input_path: str, output_path: str = None) -> str:
    """
    Reads a spun chapter from file, runs AI review, and optionally saves the feedback.
    """
    chapter_title = Path(input_path).stem.replace("_", " ").title()

    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    
    if "\n\n" in raw:
        _, text = raw.split("\n\n", 1)
    else:
        text = raw

    print(f" Reviewing '{chapter_title}' with Gemini 1.5 Flash...")

    review = review_chapter(text, chapter_title)

    if not review:
        print(" Review failed.")
        return ""

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{chapter_title} - AI Editorial Review\n\n{review}")
        print(f" Review saved to: {output_path}")

    return review



if __name__ == "__main__":
    input_file = "data/spun/chapter1_spun.txt"
    output_file = "data/reviews/chapter1_review.txt"
    review_from_file(input_file, output_file)
