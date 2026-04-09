<div align="center">

# AutoCanvas

**A local, private AI that reads your Canvas assignments, solves them, and submits — with your approval.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20%2F%20Local-black?style=flat-square)](https://ollama.com)
[![Canvas LMS](https://img.shields.io/badge/Canvas-LMS-e66000?style=flat-square)](https://instructure.com)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=flat-square)](#cross-platform-launching)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-blueviolet?style=flat-square)](#how-stealth-mode-works)

</div>

---

AutoCanvas connects your school's Canvas LMS to a **locally-running AI model** (via [Ollama](https://ollama.com)). It scans your active courses, downloads assignment files (Google Docs, PDFs, DOCX), generates answers in your writing style, and shows you a preview before asking permission to submit — **nothing goes to Canvas without your explicit `y`**.

Everything runs **on your own machine**. No data is ever sent to the cloud.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup & Configuration](#setup--configuration)
- [Running AutoCanvas](#running-autocanvas)
- [Submission Confirmation](#submission-confirmation)
- [How Stealth Mode Works](#how-stealth-mode-works)
- [Live Dashboard](#live-dashboard)
- [Changing Models](#changing-models)
- [Cross-Platform Launching](#cross-platform-launching)
- [File Structure](#file-structure)
- [Disclaimer](#disclaimer)

---

## How It Works

```
Canvas API ──► Scan courses & assignments
                      │
                      ▼
          Download files (Google Docs / PDF / DOCX)
                      │
                      ▼
         Local AI fills in answers (Ollama)
                      │
                      ▼
         ┌─ Rich preview panel in terminal ─────────┐
         │  Assignment: AMI Day #3                  │
         │  Course: Physical Science                │
         │  AI answer preview shown here...         │
         │                                          │
         │  Submit this to Canvas? [y/n]            │
         └──────────────────────────────────────────┘
                      │
            y ────────┴──────── n
            │                   │
     Submitted to Canvas    Saved locally only
```

1. Fetches all your active Canvas courses
2. Finds downloadable files in each assignment — Google Docs, PDFs, DOCX, and Canvas-hosted attachments
3. Extracts text and sends it to your local AI model
4. Saves the completed answer as a `.docx` in `Completed_Homework/`
5. Shows you a preview and asks for confirmation — **you decide what gets submitted**

---

## Requirements

> AutoCanvas runs entirely on your local machine. It is **not** compatible with mobile devices or school-managed Chromebooks.

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11, macOS 12+, or Linux |
| **Python** | 3.10 or newer |
| **GPU (recommended)** | NVIDIA RTX 30/40-series, 8 GB+ VRAM |
| **GPU (minimum)** | GTX 1060+, or Apple M1/M2/M3 (8 GB unified memory) |
| **CPU-only** | Works but slow — use a small model like `llama3.2` |
| **Disk** | ~5 GB free for the AI model |

---

## Installation

### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version.
2. **Windows:** On the installer's first screen, check **"Add Python to PATH"** before clicking Install.
3. Verify it works — open a terminal and run:

```bash
python --version
# or on Mac/Linux:
python3 --version
```

---

### Step 2 — Install Ollama (the local AI engine)

1. Go to [ollama.com](https://ollama.com) and download the installer for your OS.
2. Install and launch it. On Windows you'll see its icon in the system tray; on Mac it appears in the menu bar.
3. Open a terminal and pull the default model:

```bash
ollama pull mistral-nemo
```

> **Low-end hardware?** Pull `llama3.2` instead — it runs on ~4 GB VRAM. See [Changing Models](#changing-models).

---

### Step 3 — Download AutoCanvas

**Option A — Clone with Git:**
```bash
git clone https://github.com/YOUR_USERNAME/AutoCanvas.git
cd AutoCanvas
```

**Option B — Download ZIP:**
1. Click the green **Code** button → **Download ZIP**
2. Extract the ZIP and open the extracted folder in a terminal

---

### Step 4 — Install Python Dependencies

Inside the project folder, run:

```bash
pip install -r requirements.txt
```

This installs everything AutoCanvas needs in one command.

---

## Setup & Configuration

Run the interactive setup wizard:

```bash
python setup.py        # Windows
python3 setup.py       # Mac / Linux
```

Or just launch `run.py` — it runs setup automatically if no config is found.

The wizard walks you through:

| Prompt | What to enter |
|--------|---------------|
| **Canvas URL** | Your school's Canvas domain — `https://school.instructure.com` |
| **Canvas API Token** | A personal access token from Canvas settings (instructions below) |
| **Your full name** | Used in the AI prompt so answers sound like you wrote them |
| **Ollama model** | Press Enter to keep `mistral-nemo` (default) |
| **Ollama URL** | Press Enter to keep `http://localhost:11434` (default) |

Everything is saved to a `.env` file that stays on your machine and is never uploaded to GitHub.

---

### How to Get Your Canvas API Token

1. Log into Canvas in your browser
2. Click your **Account** avatar (top-left) → **Settings**
3. Scroll down to **Approved Integrations**
4. Click **+ New Access Token**
5. Name it anything (e.g. `AutoCanvas`) — leave the expiry date blank
6. Click **Generate Token**
7. **Copy the token immediately** — Canvas only shows it once

> **Keep this token private.** The `.env` file is listed in `.gitignore` and will not be pushed to GitHub.

---

## Running AutoCanvas

The easiest way to start everything is through the launcher:

```bash
python run.py        # Windows
python3 run.py       # Mac / Linux
```

Or just double-click:
- **Windows** → `start.bat`
- **Mac / Linux** → `start.sh` *(see [Cross-Platform Launching](#cross-platform-launching))*

You'll see the main menu:

```
 ╭───────────────────────────────╮
 │  AutoCanvas                   │
 │  Local AI · Private · No cloud│
 ╰───────────────────────────────╯

  1  Run Bot       Scan Canvas, solve & confirm submissions
  2  Monitor       Start the live activity dashboard
  3  Setup         Update credentials, name, or AI model
  4  Exit
```

---

## Submission Confirmation

AutoCanvas **will never submit to Canvas without asking you first.**

After the AI solves an assignment you see a preview panel:

```
 ╭──────────────── Confirm Submission ────────────────╮
 │                                                     │
 │  AMI Day #3                                         │
 │  Course:  Physical Science 2025-2026                │
 │  Type:    online_upload                             │
 │                                                     │
 │  I think the main reason convection currents form   │
 │  in the mantle is heat from Earth's core rising     │
 │  toward the crust, which causes circular movement…  │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯
  Submit this to Canvas? [y/n] (n):
```

- **`y`** — file is uploaded and submitted to Canvas
- **`n`** — submission is skipped; the completed `.docx` is still saved locally in `Completed_Homework/`

If multiple assignments finish processing at the same time, confirmation prompts queue up **one at a time** so you're never rushed.

---

## How Stealth Mode Works

AutoCanvas is designed to look like a normal student browsing Canvas, not an automated script.

| Technique | Detail |
|-----------|--------|
| **Random delays between assignments** | Waits 2–5 seconds before starting each one — mimics tabbing between assignments |
| **Random delays between courses** | Waits 10–25 seconds after finishing one course before starting the next |
| **Delay after API calls** | Short 0.5–1.5 second pause after each Canvas data fetch |
| **Download preflight pause** | 1–2.5 second pause before each file download |
| **Browser User-Agent** | All HTTP requests identify as Chrome on Windows, not Python |
| **Rate limit backoff** | If Canvas returns a 429, waits 5s → 10s → 20s before retrying |
| **Low concurrency** | Max 2 assignments processed simultaneously per course |
| **Sequential courses** | Processes one course at a time — never floods all courses at once |
| **AI naturally paces it** | Local LLM takes 30–120 seconds per assignment, creating organic gaps |

These settings are built-in and active automatically. No configuration needed.

---

## Live Dashboard

The monitor generates a local HTML page that auto-refreshes every 5 seconds.

Start it from the menu (option **2**) or directly:

```bash
python monitor.py        # Windows
python3 monitor.py       # Mac / Linux
```

Then open `dashboard.html` in your browser. It shows:

- Total assignments completed
- Success vs. error counts
- Per-course file breakdown
- Live log feed (last 15 lines)

---

## Changing Models

Re-run setup (`python setup.py`) and enter a different model name, or edit `AI_MODEL=` in `.env` directly.

Pull any model first:

```bash
ollama pull llama3.2
```

| Model | VRAM | Speed | Quality |
|-------|------|-------|---------|
| `mistral-nemo` *(default)* | ~8 GB | Fast | Great |
| `llama3.2` | ~4 GB | Fast | Good |
| `llama3.1:8b` | ~6 GB | Medium | Great |
| `deepseek-r1:8b` | ~6 GB | Medium | Excellent |

---

## Cross-Platform Launching

### Windows — double-click `start.bat`

No terminal needed. Just double-click `start.bat` in the project folder. It automatically finds Python (tries the Windows Python Launcher `py` first, then falls back to `python`) and keeps the window open if there's an error.

### macOS / Linux — run `start.sh`

The first time, make it executable:

```bash
chmod +x start.sh
```

Then launch it:

```bash
./start.sh
```

Or double-click it in Finder (macOS) — right-click → Open if your system asks for confirmation.

---

## File Structure

```
AutoCanvas/
├── start.bat               ← Windows: double-click to launch
├── start.sh                ← Mac/Linux: ./start.sh to launch
├── run.py                  ← Unified launcher & menu
├── setup.py                ← Interactive configuration wizard
├── auto_bot.py             ← Main bot logic
├── monitor.py              ← Dashboard generator
├── requirements.txt        ← Python dependencies
│
├── .env                    ← Your credentials (auto-generated, git-ignored)
├── dashboard.html          ← Live dashboard (auto-generated)
├── sys_check.log           ← Activity log (auto-generated)
│
└── Completed_Homework/     ← Output folder (auto-generated)
    ├── Physical Science/
    │   └── [DONE] AMI Day 3_part1.docx
    └── English I/
        └── [DONE] Odyssey Creative Task_part1.docx
```

---

## Disclaimer

> This software is provided for research and personal productivity purposes only. Use it responsibly and in accordance with your school's academic integrity policy. The authors are not responsible for any consequences arising from its use.

---

<div align="center">

Built with Python · [Ollama](https://ollama.com) · [Canvas API](https://canvas.instructure.com/doc/api/) · [Rich](https://github.com/Textualize/rich)

</div>
