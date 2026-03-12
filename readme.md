# AutoCanvas: The Homework Automation Suite

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Security](https://img.shields.io/badge/Privacy-Localized-orange)

AutoCanvas is a localized automation tool designed to bridge the gap between [your school]'s Canvas LMS account and local Large Language Models (LLMs). It autonomously scans your courses, identifies assignments containing Google Doc templates, and utilizes a private AI instance to generate completed versions of your worksheets.

---

### 1. System Requirements & Device Compatibility

This program runs **locally** on your hardware. It is compatible with **Windows, macOS, and Linux**. It cannot run on mobile devices (iOS/Android) or standard school Chromebooks.

* **Standard Mode:** NVIDIA RTX 30-series or 40-series (8GB+ VRAM).
* **Lite Mode:** Older NVIDIA cards (GTX 1060+) or Integrated Graphics (Intel Iris/AMD Radeon).
* **Apple Mac:** Any M1, M2, or M3 chip with at least 8GB of memory.

---

### 2. Full Installation Guide

#### Phase A: The AI Engine (Ollama)
The script requires [Ollama](https://ollama.com/) to host the AI model locally.
1. Download and install [Ollama for Windows](https://ollama.com/download/windows).
2. Ensure the "Llama" icon is visible in your Windows taskbar.
3. Open your **Command Prompt (CMD)** and run this command:
   `ollama pull mistral-nemo`

#### Phase B: Python Setup
1. Visit [Python.org](https://www.python.org/downloads/) and download the latest version.
2. **IMPORTANT:** During installation, check the box that says **"Add Python to PATH"**.

#### Phase C: Project Preparation
1. Download this repository as a ZIP file.
2. **Right-click** the ZIP in your Downloads and select **Extract All**.
3. Open the folder you just extracted.

---

### 3. Setting Up Your Connection (.env File)

The bot needs two things to work: your school's website link and your private access token.

#### Step 1: Find Your School Link
1. Log into your school Canvas account in your browser.
2. Look at the address bar at the top.
3. Copy the part that ends in `.instructure.com`.
   * **Correct:** `https://[your-school].instructure.com`
   * **Incorrect:** `https://[your-school].instructure.com/courses/12345/modules`

#### Step 2: Create the .env File
1. Open **Notepad** on your computer.
2. Paste these two lines into the blank window:
   ```text
   CANVAS_URL=https://[your-school].instructure.com
   CANVAS_TOKEN=your_token_here

4. Running the Automation
1. Open your project folder.
2. Click the address bar at the top, type cmd, and press Enter.
3. Install libraries (First time only):
pip install canvasapi openai python-docx python-dotenv requests
4. Start the bot:
python auto_bot.py
5. Key Features
• Smart Scan: The bot checks your Completed_Homework folder. If a file already exists, it logs [SKIP] to save time.
• Stealth Mode: Uses randomized delays (10–25 seconds) to mimic a human student.
• Auto-Folder: Automatically sorts work into folders like Spanish 2 or Physical Science.
⚡ Low VRAM Edition (For Older PCs or Laptops)
If your computer is struggling, use the Llama 3.2 model instead:
1. Run ollama pull llama3.2 in CMD.
2. Open auto_bot.py in Notepad.
3. Change AI_MODEL = "mistral-nemo" to AI_MODEL = "llama3.2".
Disclaimer: This software is for research and personal organization. Use responsibly according to school policies.
