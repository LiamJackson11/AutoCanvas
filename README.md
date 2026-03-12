# AutoCanvas: The Homework Automation Suite

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Security](https://img.shields.io/badge/Privacy-Localized-orange)

AutoCanvas is a specialized automation tool designed to bridge the gap between [Canvas LMS](https://fhsd.instructure.com) and local Large Language Models (LLMs). It autonomously scans your courses, identifies assignments containing Google Doc templates, and utilizes a private AI instance to generate completed versions of your worksheets.

> **Privacy Commitment:** This tool is 100% localized. Your Canvas token and assignment data never leave your machine. No external AI services (like ChatGPT or Gemini) are used; all processing happens on your own hardware.

---

### 1. System Requirements & Prerequisites
To ensure the AI runs efficiently on your machine, the following are recommended:
* **Graphics Card (GPU):** NVIDIA RTX 30-series or 40-series (8GB+ VRAM recommended for Mistral-Nemo).
* **Operating System:** Windows 10 or 11.
* **Storage:** 10GB of free space for the local AI "brain."

---

### 2. Comprehensive Installation Guide

#### Phase A: The AI Engine (Ollama)
The script requires [Ollama](https://ollama.com/) to host the AI model locally on your GPU.
1. Download the [Ollama for Windows Installer](https://ollama.com/download/windows).
2. Install the application and ensure the "Llama" icon is visible in your Windows taskbar.
3. Open your **Command Prompt (CMD)** and run the following command to download the model:

+ ollama pull mistral-nemo
Phase B: Python SetupVisit Python.org and download the latest version for Windows.CRITICAL: During installation, you MUST check the box that says "Add Python to PATH".Complete the installation.Phase C: Project PreparationDownload this repository as a ZIP file (Green Code button > Download ZIP).Locate the ZIP in your Downloads folder, right-click it, and select Extract All.Open the newly extracted folder.Phase D: Canvas IntegrationLog into your Canvas Settings.Scroll down to Approved Purposes and click + New Access Token.Copy the long character string (Token).Find the file named .env in your project folder, open it with Notepad, and paste your token:Diff+ CANVAS_TOKEN=your_private_token_here
3. Running the AutomationFollow these steps every time you want to scan for new homework:Open your project folder in File Explorer.Click into the address bar at the top, type cmd, and press Enter.First-time only: Install the required software libraries by pasting this:pip install canvasapi openai python-docx python-dotenv requestsStart the bot: Type the following command:Diff+ python auto_bot.py
4. Key Features & LogicIntelligent Duplicate CheckThe bot performs a "Smart Scan" before processing. It checks your Completed_Homework folder for existing filenames. If a worksheet is already finished, the bot logs [SKIP] and moves to the next item instantly.Stealth & Human SimulationTo remain undetected, the bot uses the following logic:Varied Delays: It waits between 10–25 seconds between actions to mimic human reading and navigation speeds.Persona Calibration: The AI is instructed to write as "Liam Jackson," a 9th-grade student, using age-appropriate vocabulary to avoid being flagged by professional-grade AI detectors.Automated OrganizationAll work is automatically sorted into class-specific folders:Completed_Homework/Spanish 2/Physical Science/Algebra 1/5. TroubleshootingErrorCauseResolution'python' is not recognizedPath ConfigurationRe-install Python and ensure "Add to PATH" is checked.401 UnauthorizedInvalid TokenYour Canvas Token is incorrect or has expired. Generate a new one in Settings.ConnectionRefusedOllama OfflineEnsure the Ollama app is running in your Windows taskbar.Missing Google DocLink TypeThe bot currently only supports assignments that provide a Google Doc link in the description.Disclaimer: This software is intended for research and personal organization. Users are responsible for ensuring their use of this tool complies with FHSD institutional policies and academic integrity guidelines.
