# AutoCanvas: The Homework Helper

This is an automated tool that logs into your Canvas, finds your assignments, and uses AI to solve them for you. It saves the finished work into folders on your computer so you can just copy-paste the answers and turn them in.

---

##  Read This First
1. **It’s Free:** You are using your own computer's power to run the AI, so you never have to pay for a subscription.
2. **It’s Private:** The school cannot see that you are using AI because it runs locally on your machine, not on a website.
3. **It’s Stealthy:** The bot "types" like a human and adds small delays so it doesn't look like a robot.

---

##  How to Set It Up (The Easy Way)

### 1. Install the "Brain" (Ollama)
The AI needs a "brain" to think. 
* Go to [Ollama.com](https://ollama.com/) and click **Download**.
* Run the installer just like any other game or app.
* Once it's installed, a little llama icon will appear in your taskbar.

### 2. Get the Code
Since you are on this page, look for the green button at the top right that says **Code**.
* Click it, then click **Download ZIP**.
* **Important:** Find that folder in your "Downloads," right-click it, and select **Extract All** (this is how you "unzip" it so it works).

### 3. Install Python
The script runs on a language called Python.
* Go to [Python.org](https://www.python.org/downloads/) and download the latest version.
* **CRITICAL:** When installing, make sure you check the box that says **"Add Python to PATH"** at the bottom of the installer. If you miss this, the bot won't work!

### 4. Setup your "Key"
The bot needs permission to see your Canvas.
1. Log into Canvas on your browser.
2. Click **Account** -> **Settings**.
3. Scroll down to **Approved Purposed** and click **+ New Access Token**.
4. Copy that long string of random letters.
5. In the bot folder, find the file named `.env` (open it with Notepad).
6. Paste your code after `CANVAS_TOKEN=` and save the file.

---

##  How to Run It
1. Open the folder where you put the code.
2. Click the bar at the top of your file window (where the folder name is), type `cmd`, and hit Enter.
3. Type this and hit Enter (it installs the last few pieces):
   `pip install canvasapi openai python-docx python-dotenv requests`
4. Type this to start the bot:
   `python auto_bot.py`

---

##  Where is my homework?
Once the bot finished, a new folder will appear called **Completed_Homework**. 
Inside, you will see folders for each of your classes (like "Algebra" or "History"). Open them up, and your finished worksheets will be waiting for you!
