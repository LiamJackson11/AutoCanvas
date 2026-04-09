import os
import time
import html
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_FILE = str(BASE_DIR / "sys_check.log")
HW_DIR = str(BASE_DIR / "Completed_Homework")
HTML_FILE = str(BASE_DIR / "dashboard.html")

def get_log_summary():
    """Reads the last few lines of the log file and counts errors/successes."""
    if not os.path.exists(LOG_FILE):
        return [], 0, 0
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Get the last 15 lines for the live feed
    recent_logs = lines[-15:] if len(lines) > 15 else lines
    
    # Quick stats
    full_text = "".join(lines)
    success_count = full_text.count("[SUCCESS]")
    error_count = full_text.count("ERROR") + full_text.count("CRITICAL")
    
    return recent_logs, success_count, error_count

def get_homework_stats():
    """Scans the output directory and tallies completed files per course."""
    if not os.path.exists(HW_DIR):
        return {}
        
    stats = {}
    for item in os.listdir(HW_DIR):
        item_path = os.path.join(HW_DIR, item)
        if os.path.isdir(item_path):
            # Count the .docx files inside the course folder
            files = [f for f in os.listdir(item_path) if f.endswith('.docx')]
            stats[item] = len(files)
            
    return stats

def generate_html(recent_logs, success_count, error_count, hw_stats):
    """Generates the HTML file with a Bento Grid and Dark Glassmorphism UI."""
    
    # Format the homework stats into HTML list items
    courses_html = ""
    total_files = 0
    for course, count in hw_stats.items():
        courses_html += f"<div class='course-item'><span>{html.escape(course)}</span><span class='badge'>{count} files</span></div>"
        total_files += count

    if not courses_html:
        courses_html = "<div class='log-line'>No courses processed yet...</div>"

    # Format the logs into HTML
    logs_html = "".join([f"<div class='log-line'>{html.escape(line.strip())}</div>" for line in recent_logs])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="5"> <title>Bot Live Monitor</title>
        <style>
            :root {{
                --bg: #0f172a;
                --text: #e2e8f0;
                --glass-bg: rgba(255, 255, 255, 0.03);
                --glass-border: rgba(255, 255, 255, 0.05);
                --accent: #38bdf8;
                --success: #34d399;
                --danger: #f87171;
            }}
            body {{
                margin: 0;
                padding: 2rem;
                background-color: var(--bg);
                background-image: radial-gradient(circle at top right, rgba(56, 189, 248, 0.1), transparent 40%),
                                  radial-gradient(circle at bottom left, rgba(52, 211, 153, 0.05), transparent 40%);
                color: var(--text);
                font-family: 'Segoe UI', system-ui, sans-serif;
                min-height: 100vh;
            }}
            h1 {{ text-align: center; font-weight: 600; margin-bottom: 2rem; letter-spacing: 1px; }}
            
            /* Bento Grid Layout */
            .bento-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            .bento-wide {{ grid-column: 1 / -1; }}
            
            /* Glassmorphism Cards */
            .glass-card {{
                background: var(--glass-bg);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--glass-border);
                border-radius: 24px;
                padding: 24px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                display: flex;
                flex-direction: column;
            }}
            .glass-card h2 {{
                margin-top: 0;
                font-size: 1.2rem;
                color: var(--accent);
                border-bottom: 1px solid var(--glass-border);
                padding-bottom: 10px;
                margin-bottom: 15px;
            }}
            
            /* Stats Styling */
            .stat-number {{ font-size: 3rem; font-weight: bold; margin: 10px 0; }}
            .text-success {{ color: var(--success); }}
            .text-danger {{ color: var(--danger); }}
            
            /* Lists & Logs */
            .course-item {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }}
            .badge {{
                background: rgba(255,255,255,0.1);
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.85rem;
            }}
            .log-box {{
                background: rgba(0,0,0,0.3);
                border-radius: 12px;
                padding: 15px;
                flex-grow: 1;
                font-family: 'Consolas', monospace;
                font-size: 0.85rem;
                overflow-y: auto;
                max-height: 300px;
            }}
            .log-line {{ padding: 3px 0; color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.02); }}
            
            /* Scrollbar */
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: transparent; }}
            ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>Bot Activity Dashboard</h1>
        
        <div class="bento-grid">
            <div class="glass-card">
                <h2>Total Homework Done</h2>
                <div class="stat-number">{total_files}</div>
                <p>Files successfully generated and saved.</p>
            </div>
            
            <div class="glass-card">
                <h2>Health Check</h2>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Successful Turns</div>
                        <div class="stat-number text-success">{success_count}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Errors Logged</div>
                        <div class="stat-number text-danger">{error_count}</div>
                    </div>
                </div>
            </div>
            
            <div class="glass-card">
                <h2>Course Breakdown</h2>
                <div style="overflow-y: auto; max-height: 200px; padding-right: 10px;">
                    {courses_html}
                </div>
            </div>
            
            <div class="glass-card bento-wide">
                <h2>Live Terminal Output (Last 15 lines)</h2>
                <div class="log-box">
                    {logs_html}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    print(f"Starting dashboard generator... Outputting to {HTML_FILE}")
    print("Keep this script running to continuously update the dashboard.")
    
    while True:
        try:
            recent_logs, success_count, error_count = get_log_summary()
            hw_stats = get_homework_stats()
            
            generate_html(recent_logs, success_count, error_count, hw_stats)
            
            # Wait 5 seconds before pulling data and regenerating again
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\nShutting down dashboard generator.")
            break
        except Exception as e:
            print(f"Error generating dashboard: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()