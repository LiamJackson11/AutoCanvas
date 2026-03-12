# AutoCanvas: The Homework Automation guide

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![License](https://img.shields.io/badge/Status-Active-brightgreen)

AutoCanvas is a localized tool designed to synchronize with your [Canvas LMS](https://fhsd.instructure.com) account, identify pending assignments, and utilize a local Artificial Intelligence model to generate completed worksheets. 

> **Important:** The finished files are organized into subdirectories by course name on your local machine.

---

### Core Advantages

| Feature | Detail |
| :--- | :--- |
| **Cost** | Completely free. Uses your own computer hardware to run the AI. |
| **Privacy** | The AI runs locally. No data is sent to external AI servers. |
| **Stealth** | Emulates human typing patterns and check intervals to avoid detection. |

---

### Setup Instructions

#### 1. Install the Artificial Intelligence Framework
The script requires a local AI engine to process worksheet text and generate answers.
* Download and install [Ollama for Windows](https://ollama.com/download/windows).
* Once installed, open your Command Prompt and run this command to download the "brain":
```diff
+ ollama pull mistral-nemo
2. Download and Extract the Source CodeClick the Code button at the top of this page and select Download ZIP.Requirement: Right-click the file in your Downloads and select Extract All.3. Install PythonThe automation is built on the Python programming language.Download the latest installer.CRITICAL: You must check the box labeled "Add Python to PATH" during installation.4. Configure your Canvas Access TokenLog into your Canvas Account.Navigate to Account > Settings.Select + New Access Token.In your project folder, open the .env file with Notepad and paste your key:Diff+ CANVAS_TOKEN=your_token_here_12345
Operational StepsTo start the automation:Open your project folder.Click the address bar at the top, type cmd, and press Enter.Install the software libraries:pip install canvasapi openai python-docx python-dotenv requestsExecute the script:Diff+ python auto_bot.py
Accessing Completed WorkOnce the script identifies and solves an assignment, it creates a directory called Completed_Homework.Organization: Sorted by class name (e.g., Spanish 2, Physical Science).Duplicate Prevention: If a file already exists, the bot will skip it automatically.Troubleshooting Common ErrorsErrorSolution'python' not recognizedRe-install Python and check the "Add to PATH" box.401 UnauthorizedYour Canvas Token is incorrect or expired.Connection ErrorEnsure Ollama is open in your Windows Taskbar.Disclaimer: This software is intended for research and personal organization. Users are responsible for ensuring their use of this tool complies with institutional policies.
