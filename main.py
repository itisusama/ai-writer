import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("GENAI_API_KEY")
prompt_blurb = "Write a suspenseful thriller novel blurb under 100 to 120 words. This blurb should not contain the book title and character name. It should keep on readers guessing what will happen."

if not api_key:
    raise ValueError("API key not found. Set GENAI_API_KEY in your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
blurb = model.generate_content(f'{prompt_blurb}')

# Define the file name
file_name = "blurb.md"

# Extract generated text
generated_text = blurb.text

# Write to the file (append mode)
with open(file_name, "a") as file:
    file.write(generated_text + "\n\n")  # Add extra newlines for readability

print(f"Blurb appended to {file_name}.")

# Generate the chapter outline
prompt_chapters = (
    f'"{generated_text}" From this following blurb, you have to find the chapters '
    f"and provide the summary for each chapter in about 100 words. "
    f'Use the format "Chapter #: Name of the chapter." End the line, then write its summary.'
)

outline = model.generate_content(f'{prompt_chapters}')
generated_outline = outline.text

# Save the outline to outline.md
outline_file_name = "outline.md"
with open(outline_file_name, "a") as file:
    file.write(generated_outline + "\n\n")

print(f"Outline appended to {outline_file_name}.")

# Function to parse the outline and extract chapters
def parse_outline(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regex to match chapters
    chapter_pattern = re.compile(r"(Chapter \d+):\s*(.*?)\.\s*(.*?)\n", re.DOTALL)
    matches = chapter_pattern.findall(content)
    
    chapters = []
    for match in matches:
        chapter_number = match[0]
        chapter_name = match[1]
        chapter_summary = match[2].strip()
        chapters.append({
            "number": chapter_number,
            "name": chapter_name,
            "summary": chapter_summary
        })
    
    return chapters

# Function to save chapters as individual markdown files
def save_chapters(chapters, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for chapter in chapters:
        chapter_filename = f"{chapter['number'].lower().replace(' ', '-')}.md"
        chapter_path = os.path.join(output_dir, chapter_filename)
        
        content = f"# {chapter['name']}\n\n{chapter['summary']}"
        
        with open(chapter_path, 'w') as file:
            file.write(content)
        print(f"Saved: {chapter_path}")

# Main execution
input_file = "outline.md"
output_directory = "story"

chapters = parse_outline(input_file)
save_chapters(chapters, output_directory)
