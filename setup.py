from pathlib import Path
from config import extract_text_from_dir
from llm import ask_llm
from config import (Chimes, printss)
from style_analyzer import create_style_profile
from pick import pick

paths = ["writing_samples", "resumes"]
uses = ["your example cover letters", "your résumé"]
cwd = Path.cwd()
# Loop through both lists simultaneously
for folder, description in zip(paths, uses):
    target_path = Path("data") / folder
    
    if not target_path.exists():
        target_path.mkdir(parents=True)
        print(f"Populate {cwd}\\{target_path} with {description}.\n")

input("After populating these folders, Press Enter to continue setup")

# Internal Resume Building
def collapse_resumes():
    resumes = extract_text_from_dir(Path("./data/resumes"))
    prompt = f"""

Create a single, unified résumé from the selection of résumés given.

Fancy formatting can be removed.

User's name, street address, and phone number should not be included in the output.

Ensure all skills across all résumés are included in the unified résumé.

RESUMES:
{resumes}
"""
    response = ask_llm(prompt, "qwen3:4b")
    with open("data/collapsed_resume.txt", 'w') as f:
        f.write(response)
    return response

# Résumé Collapsing
selected, resume_index = pick(["Yes", "No"], "(Re)Compile résumés?")
if resume_index == 0:
    printss("Collapsing Résumés... This make take a few minutes")
    collapse_resumes()
    printss("Résumés Collapsed")
Chimes.progress_chime()

# Writing Style Analyzation
selected, style_index = pick(["Yes", "No"], "(Re)Create user writing style profile?")
if style_index == 0:
    printss("Analyzing Writing Style... This make take a few minutes")
    create_style_profile()
    printss("Style Profile Created")


Chimes.ending_chime()