# AutoCanvas: The Homework Automation Suite

AutoCanvas is a localized tool designed to synchronize with your Canvas LMS account, identify pending assignments, and utilize a local Artificial Intelligence model to generate completed worksheets. 

> **Notice:** The finished files are organized into subdirectories by course name on your local machine. This script includes stealth delays to mimic human interaction speeds.

---

### Core Advantages

| Feature | Detail |
| :--- | :--- |
| **Cost** | Completely free. Uses your own computer hardware to run the AI. |
| **Privacy** | The AI runs locally. No data is sent to external AI servers. |
| **Stealth** | Emulates human typing patterns and check intervals to avoid detection. |
| **Efficiency** | Automatically skips assignments you have already completed locally. |

---

### Setup Instructions

#### 1. Install the Artificial Intelligence Framework (Ollama)
The script requires a local AI engine to process worksheet text and generate answers.
* Visit the official Ollama website and download the installer.
* Run the setup file as you would any standard application.
* **Important:** Ensure the Ollama application is running in your system tray before starting the bot.
* Open your terminal and type `ollama pull mistral-nemo` to download the required AI model.

#### 2. Download and Extract the Source Code
* Click the green **Code** button at the top of this GitHub repository.
* Select **Download ZIP**.
* Locate the file in your Downloads folder.
* **Requirement:** Right-click the file and select **Extract All**. Running the script from within a compressed (.zip) folder will cause the bot to fail.

#### 3. Install Python
The automation is built on the Python programming language. 
* Download the latest version from Python.org.
* **CRITICAL:** You must check the box labeled **Add Python to PATH** during the installation process. If this is missed, the "python" command will not be recognized by your computer.

#### 4. Configure your Canvas Access Token
The bot requires a secure "key" to view your assignments.
1. Log into your Canvas account via a web browser.
2. Navigate to **Account** > **Settings**.
3. Locate the **Approved Purposes** section and select **+ New Access Token**.
4. Copy the character string generated.
5. In your project folder, open the `.env` file with Notepad.
6. Paste your string after `CANVAS_TOKEN=` and save the file.

---

### Operational Steps

To start the automation, follow these steps exactly:

1. Open your project folder in File Explorer.
2. Click the address bar at the top of the window, type `cmd`, and press **Enter**.
3. In the command window, paste the following to install the necessary software libraries:
   `pip install canvasapi openai python-docx python-dotenv requests`
4. Execute the script by typing:
   `python auto_bot.py`

---

### Accessing Completed Work

Once the script identifies and solves an assignment, it creates a directory called `Completed_Homework`.

* **Organization:** Assignments are automatically sorted into folders named after your specific classes (e.g., Spanish 2, Physical Science).
* **File Format:** Files are saved as `.docx` (Microsoft Word) documents.
* **Duplicate Prevention:** The script checks your local folders before running. If a file already exists, the bot will skip it to save time and system resources.

---

### Troubleshooting Common Errors

| Error Message | Likely Cause | Solution |
| :--- | :--- | :--- |
| **'python' is not recognized** | Path Error | Re-install Python and ensure "Add to PATH" is checked. |
| **401 Unauthorized** | Token Error | Your Canvas Token is incorrect. Generate a new one in Settings. |
| **ConnectionRefusedError** | AI Error | Ensure Ollama is open and running in your taskbar. |
| **FileNotFound** | Extraction Error | Ensure you clicked "Extract All" on the zip file. |

---
*Disclaimer: This software is intended for research and personal organization. Users are responsible for ensuring their use of this tool complies with their specific institutional policies and academic integrity guidelines.*
