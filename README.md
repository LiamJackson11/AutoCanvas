🤖 Autonomous Canvas Assignment Solver
This project is a Python-based automation tool that scans Canvas LMS courses, identifies assignments containing Google Doc templates, downloads them, and utilizes a local Large Language Model (LLM) via Ollama to solve the worksheets automatically.

✨ Features
Local AI Inference: Powered by mistral-nemo (or any Ollama model). Your data never leaves your machine.

Automatic Organization: Assignments are saved in sub-folders named after their respective courses.

Stealth Mode: Includes randomized "human-like" delays and typing jitter to avoid detection.

Format Preservation: Downloads .docx files, processes text, and exports a clean, finished document.

🚀 Getting Started
1. Prerequisites
Python 3.10+

Ollama: Download here

Hardware: An NVIDIA GPU (RTX 3060 or higher) is recommended for running mistral-nemo locally.

2. Installation
Clone the repository:

Bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
Install dependencies:

Bash
pip install canvasapi openai python-docx python-dotenv requests
Pull the AI model:

Bash
ollama pull mistral-nemo
3. Configuration
Create a file named .env in the root folder and add your credentials:

Code snippet
# Your Canvas domain (e.g., https://yourshcool.instructure.com)
CANVAS_URL=https://<YOUR_SCHOOL_SUBDOMAIN>.instructure.com

# Your Canvas API Token (Generated in Canvas Settings > Approved Purposed)
CANVAS_TOKEN=your_access_token_here
🛠 Usage
Ensure Ollama is running on your system.

Execute the main script:

Bash
python auto_bot.py
Check the Completed_Homework folder for your organized, AI-solved assignments.

📝 Configuration Settings
You can tweak the "Student Voice" in auto_bot.py by adjusting these variables:

MISTAKE_CHANCE: Frequency of intentional typos.

PAUSE_DURATION: How long the bot "thinks" between actions.

AI_MODEL: Swap to llama3.1 if you have less than 10GB of VRAM.

⚖️ License & Disclaimer
This project is for educational and research purposes only. Using this tool to complete school assignments may violate your institution's Academic Integrity Policy. Use responsibly.
