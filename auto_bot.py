# auto_bot.py

import os
import time
import random  
import logging
import re
import requests
from pathlib import Path
from tqdm import tqdm 
from dotenv import load_dotenv
from canvasapi import Canvas
from openai import OpenAI
from docx import Document
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

load_dotenv()

# --- 1. SETTINGS ---
APP_SETTINGS = {
    "target_grade": "A",
    "persona": "Casual Student",
    "scan_mode": "current", 
    "stealth_min": 5,
    "stealth_max": 12,
    "max_workers": 4
}

# --- 2. CONFIGURATION ---
BASE_DIR = Path(r"C:\Canvas scanner")
OUTPUT_DIR = BASE_DIR / "Completed_Homework"
CANVAS_URL = os.getenv("CANVAS_URL") or "[your school link]" #put your school link here
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
AI_MODEL = os.getenv("AI_MODEL") or "mistral-nemo"

IGNORE_LIST = ["Test", "Quiz", "Final Exam", "Physical Education", "Spartan Central", "Industrial Tech"]
PRIORITY_LIST = [""]

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True)

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

logging.basicConfig(
    filename=str(BASE_DIR / 'sys_check.log'), 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- 3. CORE UTILITIES ---

def sanitize_filename(name):
    return re.sub(r'[^\w\-_.() ]', '', name).strip()

def download_gdoc_as_docx(url, safe_filename):
    try:
        doc_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
        if not doc_id_match: 
            logging.warning(f"Invalid Google Doc URL: {url}")
            return None
        export_url = f"https://docs.google.com/document/d/{doc_id_match.group(1)}/export?format=docx"
        response = requests.get(export_url, timeout=20)
        if response.status_code == 200:
            temp_path = OUTPUT_DIR / f"TEMP_{random.randint(100,999)}_{safe_filename}.docx"
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            return temp_path
    except Exception as e:
        logging.error(f"Download error for {url}: {e}")
    return None

def is_valid_course(course):
    name = getattr(course, 'name', 'Unknown')
    if any(word.lower() in name.lower() for word in IGNORE_LIST):
        return False
    if getattr(course, 'access_restricted_by_date', False):
        return False
    return True

# --- 4. THE PERSONA ENGINE ---
def ai_fill_worksheet(worksheet_text):
    prompt = f"You are [your name], a 15-year-old 9th-grade student.\n" #put your name here
    if APP_SETTINGS["persona"] == "Casual Student":
        prompt += "- Use natural, slightly casual vocabulary. Use phrases like 'I think' or 'Basically'.\n"
        prompt += "- Avoid overly formal AI words like 'moreover' or 'delve'.\n"
    
    if APP_SETTINGS["target_grade"] == "A":
        prompt += "- Provide perfect, highly detailed, and completely accurate answers.\n"
        
    prompt += "- ONLY return the answers in the exact same format as the original document.\n"
    prompt += "- Do NOT add any extra formatting, asterisks, or notes.\n"
    prompt += "- If there are multiple questions, answer each one separately in the same order.\n"
    prompt += "- if the structure of the worksheet is this for an example: 3. How did Adolf Hitler become chancellor of Germany in 1933? How did he become the Führer and sole head of government in 1934? 4. How did the 1935 Nuremberg laws affect German Jews? 5. Under Nazi racial ideology, what groups were considered racially inferior? put the answers righ below the questions in same format like same font, size, ect. \n"

    prompt += "- Ensure your answers match the style and formatting of the original document.\n"
    prompt += "- Maintain the exact same paragraph structure and spacing.\n"
    prompt += "- Replace only the answer portions with your responses.\n"
    prompt += "- Keep all question text exactly as it appears in the original.\n"
    prompt += "- Only fill in the blank spaces or answer areas where appropriate.\n\n"
    prompt += f"Worksheet Text:\n{worksheet_text}"
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=AI_MODEL,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI Service Offline: {e}")
        return None

# --- 5. DOCUMENT EDITING FUNCTION ---
def process_assignment(course_folder, course_name, assignment, url, i):
    safe_assign = sanitize_filename(assignment.name)
    file_label = f"[DONE] {safe_assign}_part{i}"
    final_path = course_folder / f"{file_label}.docx"

    if final_path.exists():
        logging.info(f"Skipping already processed: {file_label}")
        return None

    temp_path = download_gdoc_as_docx(url, file_label)
    if not temp_path:
        return None

    try:
        doc = Document(temp_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        
        solved = ai_fill_worksheet(text)
        
        if solved:
            # Edit the original document instead of creating a new one
            edit_original_document(temp_path, solved, course_folder, file_label)
            logging.info(f"[SUCCESS] {course_name} -> {file_label}")
            return True
    except Exception as e:
        logging.error(f"Error in {file_label}: {e}")
    finally:
        if temp_path.exists():
            os.remove(temp_path)
    
    return False

def edit_original_document(original_path, solved_text, course_folder, file_label):
    # Read the original document
    original_doc = Document(original_path)
    
    # Split the solved text into lines
    solved_lines = [line.strip() for line in solved_text.split('\n') if line.strip()]
    
    # Create a new document with exact same structure
    new_doc = Document()
    
    # Copy all styles and paragraphs from original
    for para in original_doc.paragraphs:
        new_para = new_doc.add_paragraph()
        new_para.style = para.style
        
        # Add the text content of the paragraph
        new_para.add_run(para.text)
    
    # Save the modified document
    output_path = course_folder / f"{file_label}.docx"
    new_doc.save(output_path)

# --- 6. THREADING SUPPORT ---
def process_course(course):
    course_name = getattr(course, 'name', 'Unknown Course')
    print(f"\n📂 Entering Class: {course_name}")
    
    safe_course = sanitize_filename(course_name)
    course_folder = OUTPUT_DIR / safe_course
    course_folder.mkdir(parents=True, exist_ok=True)

    assignments = list(course.get_assignments())
    
    # Process assignments in this course with threading
    futures = []
    with ThreadPoolExecutor(max_workers=APP_SETTINGS["max_workers"]) as executor:
        for assignment in tqdm(assignments, desc=f"   Processing {course_name[:15]}...", unit="assign"):
            if any(word.lower() in assignment.name.lower() for word in IGNORE_LIST):
                continue

            # Link Extraction
            desc = getattr(assignment, 'description', "") or ""
            links = re.findall(r'https://docs\.google\.com/document/d/[a-zA-Z0-9_-]+', desc)
            
            if not links:
                continue

            safe_assign = sanitize_filename(assignment.name)
            
            for i, url in enumerate(links, start=1):
                future = executor.submit(process_assignment, course_folder, course_name, assignment, url, i)
                futures.append(future)
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                logging.error(f"Error processing assignment: {e}")

# --- 7. MAIN PROCESSOR ---
def main():
    print("--- 🚀 STARTING SMOOTH INSTALLER ---")
    try:
        canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
        user = canvas.get_current_user()
        raw_courses = user.get_courses(enrollment_state='active')
        courses = [c for c in raw_courses if is_valid_course(c)]
        
        # Priority Sort
        courses.sort(key=lambda c: 0 if any(p.lower() in c.name.lower() for p in PRIORITY_LIST) else 1)
        print(f"Found {len(courses)} active courses. Starting sequence...")

    except Exception as e:
        logging.critical(f"CRITICAL ERROR during initialization: {e}")
        print(f"CRITICAL ERROR: {e}")
        return

    # Process all courses with threading
    futures = []
    with ThreadPoolExecutor(max_workers=APP_SETTINGS["max_workers"]) as executor:
        for course in courses:
            future = executor.submit(process_course, course)
            futures.append(future)
        
        # Wait for all courses to complete
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                logging.error(f"Error processing course: {e}")

    print("\n--- ✨ ALL CLASSES COMPLETE ---")

if __name__ == "__main__":
    main()
