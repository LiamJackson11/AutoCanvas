import os
import time
import random  
import logging
import re
import requests
from dotenv import load_dotenv
from canvasapi import Canvas
from openai import OpenAI
from docx import Document

# Load environment variables
load_dotenv()

# --- 0. CONFIG FROM TYPER.PY ---
AVG_DELAY = 0.1             
STD_DEV_DELAY = 0.04        
MISTAKE_CHANCE = 0.07       

PAUSE_EVERY_MIN_SECONDS = 4
PAUSE_EVERY_MAX_SECONDS = 15
PAUSE_DURATION_MIN = 5
PAUSE_DURATION_MAX = 23

nearby_keys = {
    'q': 'wa', 'w': 'qase', 'e': 'wsdr', 'r': 'edft', 't': 'rfgy',
    'y': 'tghu', 'u': 'yhji', 'i': 'ujko', 'o': 'iklp', 'p': 'ol;',
    'a': 'qwsz', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc', 'g': 'ftyhbv',
    'h': 'gyujnb', 'j': 'huikmn', 'k': 'jiolm,', 'l': 'kop;,.',
    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn',
    'n': 'bhjm', 'm': 'njk,',
}

# --- 1. SETTINGS & CREDENTIALS ---
CANVAS_URL = "https://fhsd.instructure.com"
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
OUTPUT_DIR = "Completed_Homework"

# We use Mistral-Nemo on your 3080 Ti
AI_MODEL = "mistral-nemo"

if not CANVAS_TOKEN:
    logging.error("CRITICAL: CANVAS_TOKEN missing from .env!")
    exit()

# --- 2. INITIALIZATION (LOCAL OLLAMA) ---
canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

# This points to your 3080 Ti running Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

# --- 3. LOGGING SETUP ---
logging.basicConfig(
    filename='sys_check.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Also print to the console so you can watch it work
if not logging.getLogger().hasHandlers():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 4. CORE FUNCTIONS ---

def download_gdoc_as_docx(gdoc_url, filename):
    """Converts a Google Doc link to a direct .docx download link and saves it."""
    try:
        # Extract the document ID from the URL
        doc_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdoc_url)
        if not doc_id_match:
            return None
        
        doc_id = doc_id_match.group(1)
        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=docx"
        
        response = requests.get(export_url)
        if response.status_code == 200:
            filepath = os.path.join(OUTPUT_DIR, f"TEMP_{filename}.docx")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        return None
    except Exception as e:
        logging.error(f"Failed to download doc: {e}")
        return None

def extract_text_from_docx(filepath):
    """Reads all text from a Word document."""
    doc = Document(filepath)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def ai_fill_worksheet(worksheet_text):
    """Sends the worksheet to AI to fill in the blanks and answer questions."""
    prompt = f"""
    You are a 16-year-old high school student. 
    Your name is Liam Jackson and you are in 9th grade (so put your name as Liam Jackson on the assignment).
    Here is a worksheet or assignment document. 
    Your job is to read it, find the questions or the blank spaces (like ______), 
    and fill them in with the correct answers. 
    
    IMPORTANT: Return the ENTIRE completed document text so I can copy-paste it. 
    Keep your vocabulary to a 9th-grade level. Make it sound natural.
    
    Worksheet Text:
    {worksheet_text}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=AI_MODEL,
        temperature=0.8
    )
    return response.choices[0].message.content


def create_completed_docx(course_name, filename, content):
    """Creates a new Word document inside a folder named after the course."""
    # 1. Clean the course name for Windows folder rules
    safe_course = "".join([c for c in course_name if c.isalnum() or c==' ']).strip()
    course_folder = os.path.join(OUTPUT_DIR, safe_course)

    # 2. Create the folder if it doesn't exist yet
    if not os.path.exists(course_folder):
        os.makedirs(course_folder)
        logging.info(f"Created new folder for course: {safe_course}")

    # 3. Create the document
    doc = Document()
    content = content.replace("```markdown", "").replace("```", "")
    
    for line in content.split('\n'):
        doc.add_paragraph(line)
        
    # 4. Save inside the course-specific folder
    final_path = os.path.join(course_folder, f"[DONE] {filename}.docx")
    doc.save(final_path)
    return final_path


def find_gdoc_links(html_description):
    """Scans the assignment HTML for any Google Doc URLs."""
    if not html_description:
        return []
    
    # Standard Google Doc ID pattern
    pattern = r'https://docs\.google\.com/document/d/[a-zA-Z0-9_-]+'
    links = re.findall(pattern, html_description)
    
    # Remove duplicates to avoid processing the same doc twice
    return list(set(links))


def download_gdoc_as_docx(gdoc_url, assignment_name):
    """Converts a Google Doc link to a download link and saves the file."""
    try:
        doc_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdoc_url)
        if not doc_id_match:
            return None
        
        doc_id = doc_id_match.group(1)
        # Force Google to export as a Word file
        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=docx"
        
        response = requests.get(export_url)
        if response.status_code == 200:
            # Clean name for the file system
            safe_name = "".join([c for c in assignment_name if c.isalnum() or c==' ']).strip()
            filepath = os.path.join("Completed_Homework", f"TEMP_{safe_name}.docx")
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        return None
    except Exception as e:
        logging.error(f"Download failed: {e}")
        return None


def main():
    logging.info("System Check: Initializing...")
    
    # 1. Stealth Delay
    start_wait = random.randint(10, 60)
    logging.info(f"Stealth delay: waiting {start_wait}s before scanning...")
    time.sleep(start_wait)
    
    try:
        user = canvas.get_current_user()
        courses = user.get_favorite_courses()
    except Exception as e:
        logging.error(f"Failed to connect to Canvas: {e}")
        return

    # Create the output folder if it's missing
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

        for course in courses:
            logging.info(f"--- Scanning Course: {course.name} ---")
            time.sleep(random.uniform(5.5, 10.0)) 
        
            # We add per_page=100 to grab everything in one big chunk
            assignments = list(course.get_assignments(per_page=100))
            
            if not assignments:
                logging.info(f"  -> No assignments found at all for {course.name}")
            continue

        for assignment in assignments:
                try:
                    # Check if you already submitted it
                    submission = assignment.get_submission(user.id)
                    if submission.workflow_state != 'unsubmitted':
                        # This skips anything already graded or turned in
                        continue

                    description = getattr(assignment, 'description', "") or ""
                    # If there's no description, don't even bother
                    if not description:
                        continue

                    safe_name = "".join([c for c in assignment.name if c.isalnum() or c==' ']).strip()
                    
                    # --- NEW CHECK: Skip if we already generated a file for this ---
                    safe_course = "".join([c for c in course.name if c.isalnum() or c==' ']).strip()
                    expected_filepath = os.path.join(OUTPUT_DIR, safe_course, f"[DONE] {safe_name}.docx")
                    
                    if os.path.exists(expected_filepath):
                        logging.info(f"  [SKIP] Already finished locally: {assignment.name}")
                        continue
                    # ---------------------------------------------------------------

                    # Step 1: Find the Links
                    gdoc_links = find_gdoc_links(description)
                    
                    if not gdoc_links:
                        # We only log this if we're actively looking for docs
                        continue
                    
                    # Step 2: Download
                    gdoc_url = gdoc_links[0]
                    logging.info(f"  [FOUND] Downloading template for: {assignment.name}")
                    temp_filepath = download_gdoc_as_docx(gdoc_url, safe_name)
                    
                    if temp_filepath:
                        # Step 3: AI Solve
                        logging.info(f"  [AI] Solving worksheet: {assignment.name}...")
                        worksheet_text = extract_text_from_docx(temp_filepath)
                        completed_text = ai_fill_worksheet(worksheet_text)
                        
                        # Step 5: Save the finished file (added course.name here)
                        final_file = create_completed_docx(course.name, safe_name, completed_text)
                        logging.info(f"[SUCCESS] Saved to folder: {course.name} -> {final_file}")
                        
                        # Cleanup
                        if os.path.exists(temp_filepath):
                            os.remove(temp_filepath)
                    
                    # Wait between assignments so it looks human
                    time.sleep(random.uniform(12.0, 25.0))

                except Exception as inner_e:
                    logging.warning(f"Skipping assignment {getattr(assignment, 'name', 'Unknown')} due to error: {inner_e}")
                    continue

                except Exception as e:
                    logging.error(f"Error in {course.name}: {e}")
                continue

    logging.info("Scan Complete. Check the 'Completed_Homework' folder.")

if __name__ == "__main__":
    main()
    logging.info("========================================")
    logging.info("SCAN COMPLETE: All courses processed.")
    logging.info("========================================")
    print("\nSuccess! Check your folders for the new work.")