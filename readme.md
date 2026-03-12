# AutoCanvas: The Homework Automation Suite

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Security](https://img.shields.io/badge/Privacy-Localized-orange)

AutoCanvas is a localized automation tool designed to bridge the gap between [Canvas LMS]([https://canvase.instructure.com](https://www.instructure.com/canvas/login)) and local Large Language Models (LLMs). It autonomously scans your courses, identifies assignments containing Google Doc templates, and utilizes a private AI instance to generate completed versions of your worksheets.

---

### 1. System Requirements
To ensure the AI runs efficiently, the following are recommended:
* **GPU:** NVIDIA RTX 10-series 30-series+ (8GB or 3/2GB+ VRAM).
* **OS:** Windows 10 or 11.
* **Storage:** 10GB of free space.

---

### 2. Full Installation Guide

#### Phase A: The AI Engine (Ollama)
The script requires [Ollama](https://ollama.com/) to host the AI model locally.
1. Download and install [Ollama for Windows](https://ollama.com/download/windows).
2. Ensure the "Llama" icon is visible in your Windows taskbar.
3. Open your **Command Prompt (CMD)** and run the command for your chosen model:
   
   **Standard (High Quality):** `ollama pull mistral-nemo`
   
   **Lite (Low VRAM):** `ollama pull llama3.2`

#### Phase B: Python Setup
1. Visit [Python.org](https://www.python.org/downloads/) and download the latest version.
2. **IMPORTANT:** During installation, check the box that says **"Add Python to PATH"**.

#### Phase C: Project Preparation
1. Download this repository as a ZIP file.
2. **Right-click** the ZIP in your Downloads and select **Extract All**.
3. Open the folder you just extracted.

#### Phase D: Canvas Integration
1. Go to your [Canvas Settings]([https://fhsd.instructure.com/profile/settings](https://www.instructure.com/canvas/login)).
2. Click **+ New Access Token**.
3. Open the `.env` file in the project folder with Notepad.
4. Paste your token after the `=` sign: `CANVAS_TOKEN=your_token_here`

---

### 3. Running the Automation

1. Open your project folder.
2. Click the address bar at the top, type `cmd`, and press **Enter**.
3. **Install libraries (First time only):**
   
   `pip install canvasapi openai python-docx python-dotenv requests`

4. **Start the bot:**
   
   `python auto_bot.py`

---

### 4. Key Features

* **Smart Scan:** The bot checks your `Completed_Homework` folder. If a file already exists, it logs `[SKIP]` to save time.
* **Stealth Mode:** Uses randomized delays (10–25 seconds) to mimic a human student.
* **Auto-Folder:** Automatically sorts work into folders like `Spanish 2` or `Physical Science`.

---

### 5. Troubleshooting

| Error | Solution |
| :--- | :--- |
| **'python' not recognized** | Re-install Python and check the "Add to PATH" box. |
| **401 Unauthorized** | Your Canvas Token is incorrect or expired. |
| **Connection Error** | Ensure Ollama is open in your Windows taskbar. |

---

### 6. Lite Edition (Low VRAM / Faster Processing)

If you are running on a laptop or want to save system resources for gaming, you can use the Lite Edition. This uses the **Llama 3.2 3B** model, which only requires **~3GB of VRAM**.

**To use the Lite version:**
1. Run `ollama pull llama3.2` in your command prompt.
2. Open `auto_bot.py` and change the line `AI_MODEL = "mistral-nemo"` to `AI_MODEL = "llama3.2"`.

**Model Comparison:**

| Feature | Mistral-Nemo (Standard) | Llama 3.2 (Lite) |
| :--- | :--- | :--- |
| **VRAM Usage** | ~8GB to 10GB | **~2.5GB** |
| **Speed** | Moderate | **Fast** |
| **Accuracy** | Highest | Good |
| **Ideal For** | Complex Science/Math | General Worksheets |

---
*Disclaimer: This software is for research and personal organization. Use responsibly according to school policies.*
