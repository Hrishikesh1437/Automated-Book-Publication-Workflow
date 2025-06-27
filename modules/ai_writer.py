from dotenv import load_dotenv
import os
import google.generativeai as genai
from pathlib import Path

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def spin_chapter(text: str, style: str = "modern and engaging", chapter_title: str = "Chapter") -> str:
    """
    Uses Gemini to creatively rewrite a chapter.
    """
    prompt = f"""
    Rewrite the following chapter titled "{chapter_title}" in a {style} tone.
    Make it more immersive and easier to read for a modern audience.
    Avoid changing the core events or characters, but improve the language and flow.

    --- BEGIN CHAPTER ---
    {text}
    --- END CHAPTER ---
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f" Error during AI generation: {e}")
        return ""


def spin_from_file(input_path: str, output_path: str = None, style: str = "modern and engaging") -> str:
    """
    Loads a chapter from a .txt file, spins it using Gemini, and optionally saves the result.
    """
    chapter_title = Path(input_path).stem.replace("_", " ").title()

    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    
    if "\n\n" in raw:
        title, text = raw.split("\n\n", 1)
    else:
        title, text = chapter_title, raw

    print(f" Spinning '{title}'...")

    spun = spin_chapter(text, style=style, chapter_title=title)

    if not spun:
        print(" Spinning failed.")
        return ""

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{title} (Spun)\n\n{spun}")
        print(f" Spun chapter saved to: {output_path}")

    return spun


if __name__ == "__main__":
    input_file = "data/raw/chapter1.txt"
    output_file = "data/spun/chapter1_spun.txt"
    spin_from_file(input_file, output_file)
