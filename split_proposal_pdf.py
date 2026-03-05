import fitz  # pymupdf
import os
import re

# Configuration
INPUT_PDF = "proposal.pdf"
OUTPUT_DIR = "output"
CHAPTER_DIR = os.path.join(OUTPUT_DIR, "chapters")
GOAL_DIR = os.path.join(OUTPUT_DIR, "detailed_goals")

# Chapter titles as identified from the Google Doc tabs (and likely headers)
CHAPTER_TITLES = [
    "제안서",
    "프롬프트 예시",
    "To-dos",
    "기획회의",
    "일정",
    "이메일",
    "제안서 예시_",
    "rfp",
    "1. 연구필요성"
]

# Patterns for 17 Specific Goals
# We look for "세부목표 X" or "연구 X" where X is 1 to 17.
# Or "1-1.", "1-2." ... depending on actual content format.
# Based on common structures, we'll look for:
# "세부목표 1", "세부목표 2" ... and "연구 1", "연구 2" ... trying to map 17 items.
# The user said "17 specific goals and researches" (세부 목표와 총 연구가 17개).
# We will treat them as a single list of 17 items if possible, or try to detect them.
# Let's assume pattern: "세부목표 <number>" or "연구 <number>"

def ensure_dirs():
    os.makedirs(CHAPTER_DIR, exist_ok=True)
    os.makedirs(GOAL_DIR, exist_ok=True)

def split_pdf():
    if not os.path.exists(INPUT_PDF):
        print(f"Error: {INPUT_PDF} not found. Please place the file in {os.getcwd()}")
        return

    doc = fitz.open(INPUT_PDF)
    total_pages = len(doc)
    print(f"Opened {INPUT_PDF} with {total_pages} pages.")

    # 1. Analyze pages to find start pages for Chapters and Goals
    # structure: {title: start_page_index}
    chapter_starts = {}
    goal_starts = {}

    print("Analyzing document structure...")
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        # Check for Chapters
        for title in CHAPTER_TITLES:
            if title not in chapter_starts and title in text:
                # Heuristic: Title should be near the top or distinct? 
                # For now, just first occurrence.
                chapter_starts[title] = page_num
                print(f"Found Chapter '{title}' at page {page_num+1}")

        # Check for Goals (1 to 17)
        # Use simple regex for "세부목표 N" or "연구 N"
        # Adjust matching based on exact document content
        matches = re.findall(r"(세부목표|연구)\s*(\d+)", text)
        for type_, num_str in matches:
            num = int(num_str)
            key = f"{type_} {num}"
            if num <= 17 and key not in goal_starts:
                goal_starts[key] = page_num
                print(f"Found '{key}' at page {page_num+1}")

    # 2. Extract Chapters
    # Sort starting pages to define ranges
    sorted_chapters = sorted(chapter_starts.items(), key=lambda x: x[1])
    for i, (title, start_page) in enumerate(sorted_chapters):
        # End page is start of next chapter, or end of doc
        if i < len(sorted_chapters) - 1:
            end_page = sorted_chapters[i+1][1] - 1
        else:
            end_page = total_pages - 1
        
        # Validate range
        if start_page > end_page:
             # Logic implies overlap or single page
             end_page = start_page

        out_name = f"{i+1:02d}_{title.replace(' ', '_').replace('/', '-')}.pdf"
        out_path = os.path.join(CHAPTER_DIR, out_name)
        
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
        new_doc.save(out_path)
        print(f"Saved Chapter: {out_path} (Pages {start_page+1}-{end_page+1})")

    # 3. Extract Goals
    # Similar logic for goals
    sorted_goals = sorted(goal_starts.items(), key=lambda x: x[1])
    for i, (title, start_page) in enumerate(sorted_goals):
        # Warning: Goals might be nested in chapters, so end page might be start of next Goal 
        # OR end of chapter.
        # Simple approach: Goal lasts until next Goal starts.
        if i < len(sorted_goals) - 1:
            end_page = sorted_goals[i+1][1] - 1
        else:
            # Last goal goes until end of doc (roughly)
            end_page = total_pages - 1
            
        out_name = f"{title.replace(' ', '_')}.pdf"
        out_path = os.path.join(GOAL_DIR, out_name)
        
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
        new_doc.save(out_path)
        print(f"Saved Goal: {out_path} (Pages {start_page+1}-{end_page+1})")

if __name__ == "__main__":
    ensure_dirs()
    split_pdf()
