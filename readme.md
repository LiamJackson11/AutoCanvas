<div align="center">

# AutoCanvas

**A local, private AI that reads your Canvas assignments, solves them, and submits — with your approval.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20%2F%20Local-black?style=flat-square)](https://ollama.com)
[![Canvas LMS](https://img.shields.io/badge/Canvas-LMS-e66000?style=flat-square)](https://instructure.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-blueviolet?style=flat-square)](#)

</div>

---

AutoCanvas connects your school's Canvas LMS to a **locally-running AI model** (via [Ollama](https://ollama.com)). It scans your active courses, downloads assignment files (Google Docs, PDFs, DOCX), generates answers in your writing style, and shows you a preview before asking permission to submit — nothing goes to Canvas without your explicit `y`.

Everything runs **on your own machine**. No data is sent to the cloud.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup & Configuration](#setup--configuration)
- [Running AutoCanvas](#running-autocanvas)
- [Submission Confirmation](#submission-confirmation)
- [Live Dashboard](#live-dashboard)
- [Changing Models](#changing-models)
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
         ┌─ Preview shown in terminal ──────────┐
         │  Submit this to Canvas? [y/n]        │
         └──────────────────────────────────────┘
                      │
            y ────────┴──────── n
            │                   │
     Submitted to Canvas    Saved locally only
```

1. The bot fetches all active courses from Canvas
2. For each assignment it finds downloadable files (Google Docs, PDFs, DOCX links, Canvas attachments)
3. Text is extracted and sent to your local AI model
4. The completed answer is saved as a `.docx` in `Completed_Homework/`
5. **You are shown a preview and asked to confirm** before anything is submitted to Canvas

---

## Requirements

> AutoCanvas runs entirely on your local machine. It is **not** compatible with mobile devices or school-managed Chromebooks.

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11, macOS 12+, or Linux |
| **Python** | 3.10 or newer |
| **GPU (recommended)** | NVIDIA RTX 30/40-series, 8 GB+ VRAM |
| **GPU (minimum)** | GTX 1060+ or Apple M1/M2/M3 (8 GB unified memory) |
| **CPU-only** | Works, but will be slow — use a small model like `llama3.2` |
| **Disk** | ~5 GB free for the AI model |

---

## Installation

### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version.
2. **Windows:** On the installer's first screen, check **"Add Python to PATH"** before clicking Install.
3. Verify it works — open a terminal and run:

```bash
python --version
```

---

### Step 2 — Install Ollama (the local AI engine)

1. Go to [ollama.com](https://ollama.com) and download the installer for your OS.
2. Install and launch Ollama. On Windows you'll see its icon appear in the system tray.
3. Open a terminal and pull the default model:

```bash
ollama pull mistral-nemo
```

> **Low-end hardware?** Pull `llama3.2` instead — it needs less VRAM. See [Changing Models](#changing-models).

---

### Step 3 — Download AutoCanvas

**Option A — Clone with Git:**
```bash
git clone https://github.com/LiamJackson11/AutoCanvas.git
cd AutoCanvas
```

**Option B — Download ZIP:**
1. Click the green **Code** button on this page → **Download ZIP**
2. Extract the ZIP and open the extracted folder in a terminal

---

### Step 4 — Install Python Dependencies

Inside the project folder, run:

```bash
pip install -r requirements.txt
```

This installs everything AutoCanvas needs automatically.

---

## Setup & Configuration

Run the interactive setup wizard:

```bash
python setup.py
```

The wizard will ask for:

| Prompt | What to enter |
|--------|---------------|
| **Canvas URL** | Your school's Canvas domain, e.g. `https://school.instructure.com` |
| **Canvas API Token** | A personal access token from Canvas (see below) |
| **Your name** | Used in the AI prompt so answers sound like you wrote them |
| **AI model** | Press Enter to keep the default (`mistral-nemo`) |
| **Ollama URL** | Press Enter to keep the default (`http://localhost:11434`) |

After you fill these in, the wizard tests your Canvas connection and saves everything to a `.env` file.

---

### How to Get Your Canvas API Token

1. Log into Canvas in your browser
2. Click your **Account** avatar (top-left) → **Settings**
3. Scroll down to **Approved Integrations**
4. Click **+ New Access Token**
5. Give it a name (e.g. `AutoCanvas`) — leave the expiry date blank
6. Click **Generate Token**
7. **Copy the token now** — Canvas will never show it again

> **Keep this token private.** Anyone with it can access your Canvas account. The `.env` file is listed in `.gitignore` so it won't be pushed to GitHub.

---

## Running AutoCanvas

Launch everything from the unified menu:

```bash
python run.py
```

```
╔══════════════════════════════════════════╗
║              AutoCanvas                  ║
╚══════════════════════════════════════════╝

  1.  Run bot      — scan Canvas, solve & submit assignments
  2.  Monitor      — start the live dashboard (keeps running)
  3.  Setup        — change Canvas URL, token, name, model
  4.  Exit
```

- If setup hasn't been run yet, `run.py` will launch the wizard automatically before showing the menu.
- You can also run the bot directly: `python auto_bot.py`

---

## Submission Confirmation

AutoCanvas **will never submit to Canvas without asking you first.**

After the AI solves an assignment you'll see:

```
══════════════════════════════════════════════════════════════
  Course:      Physical Science 2025-2026
  Assignment:  AMI Day #3
  Submit as:   online_upload
  AI preview:  I think the main reason convection currents form
               in the mantle is because of heat differences...
══════════════════════════════════════════════════════════════
  Submit this to Canvas? [y/n]:
```

- **`y`** — uploads and submits the completed file to Canvas
- **`n`** — skips the submission; the completed `.docx` is still saved in `Completed_Homework/`

If multiple assignments finish at the same time, confirmations queue up one at a time so you're never rushed.

---

## Live Dashboard

The monitor generates a local HTML dashboard that auto-refreshes every 5 seconds.

Start it from the menu (option 2) or directly:

```bash
python monitor.py
```

Then open `dashboard.html` in your browser. It shows:

- Total assignments completed
- Success vs. error counts
- Per-course file breakdown
- Live log feed (last 15 lines)

---

## Changing Models

To switch AI models, re-run setup (`python setup.py`) and enter a different model name, or edit the `AI_MODEL` line in `.env` directly.

| Model | VRAM needed | Speed | Quality |
|-------|-------------|-------|---------|
| `mistral-nemo` *(default)* | ~8 GB | Fast | Great |
| `llama3.2` | ~4 GB | Fast | Good |
| `llama3.1:8b` | ~6 GB | Medium | Great |
| `deepseek-r1:8b` | ~6 GB | Medium | Excellent |

Pull any model first:
```bash
ollama pull llama3.2
```

---

## File Structure

```
AutoCanvas/
├── run.py                  # Unified launcher — start here
├── setup.py                # Interactive configuration wizard
├── auto_bot.py             # Main bot logic
├── monitor.py              # Dashboard generator
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials (auto-generated, not in Git)
├── dashboard.html          # Live dashboard (auto-generated)
├── sys_check.log           # Activity log (auto-generated)
└── Completed_Homework/     # Output folder (auto-generated)
    ├── Physical Science/
    │   └── [DONE] AMI Day 3_part1.docx
    └── English I/
        └── [DONE] Odyssey Creative Task_part1.docx
```

---

## Disclaimer

> This software is provided for research and personal productivity purposes. Use it responsibly and in accordance with your school's academic integrity policy. The authors are not responsible for any consequences arising from its use.

---

<div align="center">

Made with Python + Ollama + the Canvas API

</div>
