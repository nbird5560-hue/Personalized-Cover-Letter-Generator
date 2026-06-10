from style_analyzer import create_style_profile
from cover_letter_writer import write_cover_letter
from job_loader import load_job_description
from criticism_generator import revise_cover_letter
from pathlib import Path
from fpdf import FPDF
from config import (printss, load_resume, load_writing_samples, Chimes)
from output_file_creation import choose_output_type
from llm import ask_llm
import time
import sys

start_time = time.time()
# Loading resume
printss("Loading Resume")


if Path("data/collapsed_resume.txt").is_file():
    with open("data/collapsed_resume.txt", 'r') as f:
        resume = f.read()
else:
    sys.exit("Populate ./data/resumes with your résumés, then (re)run setup.py.")


# Creating style profile
if Path("data/profile.txt").is_file():
    with open("data/profile.txt", 'r', encoding='utf-8') as f:
        style = f.read()
else:
    sys.exit("Populate ./data/writing_samples with examples of your cover letters, then (re)run setup.py.")


# Loading Job Description
printss("Loading job description")
job = load_job_description()
printss("Job description loaded")

printss("Initializing cover letter creation")   
letter = write_cover_letter(
    resume,
    style,
    job[0]
)
printss("Ending cover letter creation")
Chimes.progress_chime()

printss("Revising Cover Letter")
criticism = revise_cover_letter(
    letter,
    job[0],
    resume
)
printss("Internal processes ended")
# Timing
end_time = time.time()
execution_time = (end_time - start_time)/60
print(f"Script executed in {execution_time:.4f} minutes\n")
Chimes.ending_chime()

# Output type
choose_output_type(criticism, job[1], job[2])