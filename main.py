from cover_letter_writer import (write_cover_letter, revise_cover_letter)
from scraper import load_job_description
from output_file_creation import choose_output_type
from description_analysis import analyze_job_description
from config import (printss, Chimes)
import job_helpers
from pathlib import Path
import time
import sys
import math

start_time = time.time()
# Loading resume
printss("Loading Resume")

queued = 1 if len(sys.argv) >= 3 else None

if queued is None:
    job_helpers.ensure_ollama_running()

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
if queued is not None:
    print("with sys.arg")
    job = load_job_description(sys.argv[1])
else:
    print("with no sys.arg input")
    job = load_job_description()
printss("Job description loaded")

printss("Analyzing Job Description")
job_notes = analyze_job_description(job[0], resume)
Chimes.progress_chime()

printss("Writing Cover Letter")   
letter = write_cover_letter(
    resume,
    style,
    job_notes,
    job[0]
)
Chimes.progress_chime()

printss("Revising Cover Letter")
final_letter = revise_cover_letter(#revised_letter
    letter,
    job[0],
    resume,
    style
)

final_letter = final_letter.full_text

#printss("Smoothing Cover Letter")
#final_letter = smooth_cover_letter(revised_letter)

printss("Internal processes ended")
# Timing
end_time = time.time()
execution_time = (end_time - start_time)/60
minutes = math.trunc(execution_time)
seconds = math.trunc((execution_time - minutes)*60)

print(f"Script executed in {minutes} minutes and {seconds} seconds\n")
Chimes.ending_chime()

# Output type
if queued:
    output_name = choose_output_type(final_letter, job[1], job[2], int(sys.argv[2]))
else:
    output_name = choose_output_type(final_letter, job[1], job[2])

if queued:
    print(f"OUTPUT_FILE_NAME:{output_name}; URL: {job[3]}")