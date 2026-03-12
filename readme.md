# 🤖 AutoCanvas: The Homework Automation guide

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![AI Model](https://img.shields.io/badge/AI-Mistral--Nemo-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Security](https://img.shields.io/badge/Privacy-Localized-orange)

*A local, private AI bridge between your Canvas LMS and your machine.*

</div>

---

AutoCanvas is a localized automation tool designed to bridge the gap between your school's Canvas LMS account and local Large Language Models (LLMs). It autonomously scans your courses, identifies assignments containing Google Doc templates, and utilizes a private AI instance to generate completed versions of your worksheets.

---

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Configuration (.env Setup)](#-configuration-env-setup)
- [Running the Bot](#-running-the-bot)
- [Key Features](#-key-features)
- [Low VRAM Edition](#-low-vram-edition)
- [Disclaimer](#-disclaimer)

---

## 💻 System Requirements

This program runs **fully locally** on your hardware. It is compatible with **Windows, macOS, and Linux**.

> ⚠️ Cannot run on mobile devices (iOS/Android) or standard school Chromebooks.

| Mode | Hardware |
|------|----------|
| **Standard Mode** | NVIDIA RTX 30-series or 40-series (8GB+ VRAM) |
| **Lite Mode** | Older NVIDIA cards (GTX 1060+) or Integrated Graphics (Intel Iris / AMD Radeon) |
| **Apple Silicon** | Any M1, M2, or M3 chip with at least 8GB of unified memory |

---

## 🛠 Installation Guide

### Phase A — The AI Engine (Ollama)

The script requires [Ollama](https://ollama.com/) to host the AI model locally on your machine.

1. Download and install [Ollama for Windows](https://ollama.com/download/windows).
2. Confirm the **Llama icon** appears in your Windows taskbar after installation.
3. Open **Command Prompt (CMD)** and run:

```bash
ollama pull mistral-nemo
```

---

### Phase B — Python Setup

1. Visit [python.org](https://www.python.org/downloads/) and download the latest version.
2. **IMPORTANT:** During installation, check **"Add Python to PATH"** before clicking Install.

---

### Phase C — Project Preparation

1. Download this repository as a **ZIP file**.
2. **Right-click** the ZIP in your Downloads folder and select **Extract All**.
3. Open the extracted folder — this is your working project directory.

---

## ⚙️ Configuration (.env Setup)

The bot needs two things to connect: your school's Canvas URL and your private access token.

### Step 1 — Find Your School's Canvas URL

1. Log into your school Canvas account in your browser.
2. Look at the address bar and copy the base domain.

| ✅ Correct | ❌ Incorrect |
|-----------|-------------|
| `https://[your-school].instructure.com` | `https://[your-school].instructure.com/courses/12345/modules` |

---

### Step 2 — Create the `.env` File

1. Open **Notepad** and paste the following:

```env
CANVAS_URL=https://[your-school].instructure.com
CANVAS_TOKEN=your_token_here
```

2. Replace the URL with your school's link.
3. Replace `your_token_here` with the token from **Canvas → Account → Settings**.
4. Click **File → Save As**.
5. Set **"Save as type"** to `All Files (*.*)`.
6. Name the file exactly `.env` *(with the dot at the start)* and save it inside the project folder.

---

## 🚀 Running the Bot

1. Open your project folder.
2. Click the **address bar** at the top of the folder window, type `cmd`, and press **Enter**.
3. Install dependencies *(first time only)*:

```bash
pip install canvasapi openai python-docx python-dotenv requests
```

4. Launch the bot:

```bash
python auto_bot.py
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Scan** | Checks your `Completed_Homework` folder and logs `[SKIP]` for files that already exist — no duplicate work. |
| 🕵️ **Stealth Mode** | Uses randomized delays (10–25 seconds) to mimic natural human behavior. |
| 📁 **Auto-Folder** | Automatically organizes completed work into subject folders (e.g., `Spanish 2`, `Physical Science`). |

---

## ⚡ Low VRAM Edition

Struggling with performance on an older PC or laptop? Switch to the lighter `llama3.2` model:

1. Pull the smaller model:

```bash
ollama pull llama3.2
```

2. Open `auto_bot.py` in Notepad and find this line:

```python
AI_MODEL = "mistral-nemo"
```

3. Change it to:

```python
AI_MODEL = "llama3.2"
```

---

## 📄 Disclaimer

> This software is intended for research and personal organization purposes only. Please use responsibly and in accordance with your school's academic policies.
