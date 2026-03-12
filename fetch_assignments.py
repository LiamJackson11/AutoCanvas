from canvasapi import Canvas
import openai 
# Replace these with your actual info
API_URL = "https://fhsd.instructure.com" # Or your school's specific URL
API_KEY = "CANVAS_TOKEN" # Get this from your Canvas account settings

canvas = Canvas(API_URL, API_KEY)

# Get your user profile
user = canvas.get_current_user()
print(f"Connected as: {user.name}")

# Fetch assignments that need a submission
assignments = user.get_todo_items()

for item in assignments:
    if hasattr(item, 'assignment'):
        print(f"--- {item.assignment['name']} ---")
        print(f"Due: {item.assignment['due_at']}")
        print(f"Description: {item.assignment['description']}") # This is the prompt for the AI

def solve_as_student(assignment_text):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You are a 14-year-old high school student. 
                Your name is test test and your in 9th grade. 
                Write the following assignment in a natural student voice.
                - Use 'I think' or 'Basically' occasionally.
                - Avoid sounding like an encyclopedia.
                - Use standard high school vocabulary (don't use words like 'plethora' or 'moreover').
                - Keep the formatting simple (no professional AI bullet points).
            """},
            {"role": "user", "content": f"Complete this assignment: {assignment_text}"}
        ]
    )

    return response.choices[0].message.content
