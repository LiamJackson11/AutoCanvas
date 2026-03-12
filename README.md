# AutoCanvas: The Homework Automation Guide

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![License](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

AutoCanvas is a localized automation framework designed to bridge the gap between [Canvas LMS](https://fhsd.instructure.com) and local Large Language Models (LLMs). It autonomously identifies pending assignments, extracts content from linked Google Docs, and utilizes a private AI instance to generate completed versions of your worksheets.

> **Privacy Guarantee:** Unlike web-based AI tools, AutoCanvas processes all assignment data on your local hardware. No academic data is transmitted to third-party servers.

---

### 1. Pre-Flight Checklist
Before beginning the setup, ensure your system meets these hardware requirements for smooth AI performance:
* **GPU:** NVIDIA RTX 30-series or 40-series (8GB+ VRAM recommended).
* **RAM:** 16GB Minimum.
* **Storage:** 10GB of free space for AI model weights.
* **Browser:** Any modern browser logged into your school Canvas account.

---

### 2. Full Installation Guide

#### Phase A: The AI Engine (Ollama)
The "brain" of this project runs on **Ollama**, which allows your graphics card to think without an internet connection.
1. Visit [Ollama.com](https://ollama.com/download/windows) and download the installer.
2. Run the application and follow the on-screen prompts.
3. Once the llama icon appears in your taskbar, open your **Command Prompt (CMD)** and type:
```diff
+ ollama pull mistral-nemo
This will download approximately 7GB of data. Do not close the window until it reaches 100%.Phase B: Python EnvironmentThe script is written in Python. Without it, your computer won't know how to read the bot's instructions.Download the latest version from Python.org.Important: When the installer opens, you MUST check the box at the bottom that says "Add Python to PATH".Click "Install Now."Phase C: Project SetupDownload the code from this repository using the Code > Download ZIP button.Extraction: Locate the file in your Downloads. Right-click it and select Extract All. This creates a regular folder you can actually work in.The Secret Key: * Navigate to your Canvas Settings.Click + New Access Token.Give it a name (e.g., "Bot") and click Generate.Open the .env file in the project folder with Notepad and paste the key after the = sign.3. How to Execute the BotOpen the project folder you just extracted.In the folder's top address bar, type cmd and hit Enter.Initialize Dependencies: Copy and paste this line into the black window:pip install canvasapi openai python-docx python-dotenv requestsLaunch: Start the automation by typing:Diff+ python auto_bot.py
4. Detailed Feature BreakdownDynamic Folder OrganizationThe bot doesn't just dump files everywhere. It reads your Canvas data and builds a clean directory structure:Completed_Homework/Physical Science/ -> [DONE] Worksheet_1.docxSpanish 2/ -> [DONE] Vocab_Practice.docxIntelligent Duplicate DetectionTo save you from hitting your GPU too hard, the bot performs a Local File Hash Check. If it sees a file with the same name already exists in your "Completed" folder, it skips it instantly, allowing it to find new work much faster.Stealth & Detection AvoidanceRandomized Intervals: The bot waits between 10 and 25 seconds between assignments to mimic a human browsing a page.Humanized AI: The prompt is hard-coded to use 9th-grade vocabulary and a "student persona" to ensure the writing style doesn't trigger AI detectors that look for overly professional "corporate" talk.5. Common TroubleshootingIssueRoot CauseResolutionConnectionRefusedErrorOllama is closedClick the Ollama icon in your Start Menu to wake it up.ModuleNotFoundErrorMissing librariesRe-run the pip install command from step 3.Empty FoldersAssignment TypeThe bot currently only looks for assignments with Google Doc links in the description.Rate LimitedCanvas ProtectionThe bot will automatically pause and retry; no action needed.Disclaimer: This software is intended for research, organizational assistance, and personal study. Users are solely responsible for adhering to their school's Academic Integrity Policy.
