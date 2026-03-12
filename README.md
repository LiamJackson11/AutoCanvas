Instructions:
Create a new file in your C:\Canvas scanner folder.

Name it README.md.

Paste the following text into it.

Markdown
# 🎓Canvas Auto-Homework Machine

An automated pipeline that scans Francis Howell Canvas courses, downloads Google Doc worksheets, and uses a local **Mistral-Nemo (12B)** AI model to solve them.



## 🛠 Hardware Requirements
- **GPU:** NVIDIA RTX 3080 Ti (12GB VRAM recommended for Mistral-Nemo).
- **RAM:** 32GB DDR5.
- **Storage:** ~10GB for local AI models.

## 🚀 Setup Instructions

### 1. Install Local AI (Ollama)
1. Download Ollama from [ollama.com](https://ollama.com).
2. Open PowerShell and pull the model:
   ```powershell
   ollama pull mistral-nemo
2. Environment Configuration
Create a .env file in the root directory:

Code snippet
CANVAS_URL=[https://[your school].instructure.com](https://[your school].instructure.com)
CANVAS_TOKEN=your_canvas_api_token_here
Note: You do not need a GITHUB_TOKEN or OpenAI key because the AI runs locally on your 3080 Ti.

3. Python Environment
Install the required libraries:

Bash
pip install canvasapi openai python-docx python-dotenv requests
4. How to Run
Ensure the Ollama app is running in your system tray.

Run the main script:

Bash
python auto_bot.py
📁 Output Structure
The bot automatically organizes completed assignments by course name:

Plaintext
Completed_Homework/
├── Biology/
│   └── [DONE] Cell_Structure_Lab.docx
├── US_History/
│   └── [DONE] Civil_War_Notes.docx
└── Algebra_2/
🕵️‍♂️ Stealth & Safety
Local Inference: No AI traffic leaves your network. It stays on your GPU.

Human Jitter: The script includes random delays (time.sleep) to mimic human browsing behavior.

Metadata: Remember to right-click files -> Properties -> Details -> Remove Personal Information before uploading to Canvas.

⚠️ Disclaimer
This tool is for educational purposes and personal workflow automation. Always review the AI-generated answers for accuracy before submission.
