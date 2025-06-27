import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

DATA_DIR = "data/raw"
SCREENSHOT_DIR = "data/screenshots"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

async def fetch_chapter(url: str, chapter_name: str = "chapter1") -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, "lxml")

    
    body_div = soup.find("div", class_="mw-parser-output")

    
    paragraphs = []
    title = None
    started = False
    for element in body_div.find_all(["h2", "h3", "p", "div", "b"]):
        if element.name in ["h2", "h3", "b"] and not title:
            title = element.get_text(strip=True).upper()
        if element.name == "p":
            text = element.get_text(strip=True)
            if text:
                paragraphs.append(text)

    chapter_text = "\n\n".join(paragraphs)

    
    txt_path = os.path.join(DATA_DIR, f"{chapter_name}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{chapter_text}")

    print(f" Saved cleaned chapter to: {txt_path}")
    return {"title": title, "text": chapter_text}

async def capture_screenshot(url: str, chapter_name: str = "chapter1"):
    output_path = os.path.join(SCREENSHOT_DIR, f"{chapter_name}.png")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
    print(f" Screenshot saved to: {output_path}")


if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    chapter = "chapter1"
    asyncio.run(capture_screenshot(url, chapter))
    result = asyncio.run(fetch_chapter(url, chapter))
    print(f"TITLE:\n{result['title']}\n\nEXCERPT:\n{result['text'][:500]}")
