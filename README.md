# Autonomous Assignment Processing Pipeline
**A localized AI-driven automation suite for Canvas LMS integration.**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NVIDIA](https://img.shields.io/badge/nvidia-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)

---

## System Overview
This project provides an end-to-end solution for synchronizing Canvas LMS assignments with local Large Language Models (LLMs). It automates the extraction of Google Doc templates, performs local inference using NVIDIA hardware, and organizes completed outputs into structured directories.



## Core Functionalities
| Feature | Implementation |
| :--- | :--- |
| **API Integration** | Bi-directional communication with Canvas LMS REST API. |
| **Local Inference** | High-performance execution via Ollama (Mistral-Nemo/Llama 3.1). |
| **Data Extraction** | Regex-based Google Doc link harvesting and DOCX conversion. |
| **File Management** | Automatic directory stratification based on Course ID/Name. |
| **Stealth Logic** | Randomized request intervals and simulated typing latency. |

## Technical Requirements
### Hardware
* **GPU:** NVIDIA RTX 30-series or 40-series (12GB+ VRAM recommended).
* **RAM:** 16GB+ (DDR5 preferred for high-speed context swapping).

### Software
* **Ollama Runtime:** Required for local model hosting.
* **Python 3.10+:** Required for script execution.

## Installation and Deployment

### 1. Model Preparation
Initialize the local inference engine by pulling the required model weights:
```bash
ollama pull mistral-nemo
2. Dependency Installation
Install the required Python modules via pip:

Bash
pip install canvasapi openai python-docx python-dotenv requests
3. Environment Configuration
Create a .env file in the project root. Ensure the CANVAS_URL matches your institution's specific subdomain:

Code snippet
CANVAS_URL=https://<INSTITUTION>.instructure.com
CANVAS_TOKEN=YOUR_API_ACCESS_TOKEN
Operational Workflow
The execution follows a linear pipeline to ensure data integrity:

Scanning: The script queries the Canvas API for unsubmitted assignments.

Parsing: Assignment descriptions are parsed for valid document links.

Inference: The 12B parameter model processes the worksheet text locally.

Finalization: A formatted .docx is generated and saved to the course-specific subdirectory.

Security and Privacy
Zero-Cloud Traffic: All AI processing is performed on the local GPU; no prompt data is transmitted to third-party providers.

Metadata Scrubbing: It is recommended to clear document metadata prior to final upload.

Token Protection: Ensure the .env file is included in your .gitignore to prevent credential exposure.

This software is intended for research and workflow automation. Users must adhere to their institution's academic honesty policies.
