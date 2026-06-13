from pathlib import Path
from config import extract_text_from_dir
from llm import ask_llm
from config import (Chimes, printss)
from style_analyzer import create_style_profile
from pick import pick
from config import printss

paths = ["writing_samples", "resumes", "process"]
uses = ["your example cover letters", "your résumé", None]
cwd = Path.cwd()

for folder, description in zip(paths, uses):
    target_path = Path("data") / folder
    
    if not target_path.exists():
        target_path.mkdir(parents=True)
        
    if not description is None:
        print(f"Populate {cwd}\\{target_path} with {description}.\n")
    else:
        processes = ["job", "queue", "in_progress", "completed"]
        for p in processes:
            file_path = target_path / f"{p}.txt"
            if not file_path.exists(): 
                with open(file_path, 'w') as f:
                    f.write('')

printss("File Structure Setup Complete")

input("Populated the 'resumes' and 'writing_samples folders under the data subdirectory, then press Enter to continute.")

# Internal Resume Building
def collapse_resumes():
    resumes = extract_text_from_dir(Path("./data/resumes"))
    prompt = f"""

Your job is to create a single, unified résumé from the selection of résumés provided.

Details about each project or experience should be collected, collated, and amalgamated in the output.

Fancy formatting around names or titles can be removed.

User's name, street address, and phone number should not be included in the output.

Ensure all skills across all résumés are included in the output.

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