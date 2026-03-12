# AutoCanvas: The Homework Automation Guide

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![License](https://img.shields.io/badge/Status-Active-brightgreen)

AutoCanvas is a localized tool designed to synchronize with your [Canvas LMS](https://fhsd.instructure.com) account, identify pending assignments, and utilize a local Artificial Intelligence model to generate completed worksheets. 

> **Privacy Notice:** This tool runs entirely on your local hardware. No login credentials or assignment data are transmitted to external servers.

---

### Core Advantages

| Feature | Detail |
| :--- | :--- |
| **Cost** | Completely free. Uses your own computer hardware to run the AI. |
| **Privacy** | The AI runs locally. No data is shared with 3rd-party web AI services. |
| **Stealth** | Emulates human typing patterns and check intervals to avoid detection. |

---

### Setup Instructions

#### 1. Install the Artificial Intelligence Framework
The script requires a local AI engine (Ollama) to process worksheet text.
* Download and install [Ollama for Windows](https://ollama.com/download/windows).
* Once installed, open your Command Prompt and run this command:
```diff
+ ollama pull mistral-nemo
2. Download and Extract the Source CodeClick the Code button at the top of this page and select Download ZIP.Requirement: You must right-click the file in your Downloads and select Extract All.3. Install PythonThe automation is built on Python.Download the latest installer.CRITICAL: You must check the box labeled "Add Python to PATH" during installation.4. Configure your Canvas Access TokenLog into your Canvas Settings.Select + New Access Token.In your project folder, open the .env file with Notepad and paste your key:Diff+ CANVAS_TOKEN=your_private_token_here
Operational StepsOpen your project folder.Click the address bar at the top, type cmd, and press Enter.Install the software libraries:pip install canvasapi openai python-docx python-dotenv requestsExecute the script:Diff+ python auto_bot.py
Troubleshooting Common ErrorsErrorSolution'python' not recognizedRe-install Python and check the "Add to PATH" box.401 UnauthorizedYour Canvas Token is incorrect or expired.Connection ErrorEnsure the Ollama application is open and visible in your Windows Taskbar.
