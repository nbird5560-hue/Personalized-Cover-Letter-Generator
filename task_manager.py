import subprocess
import sys
import os
from pick import pick
from config import (printss, Chimes)
import job_helpers
from job_helpers import dpt

# Establishing session as including subprocesses
os.environ["AS_SUBPROCESS"] = True

# Checking for prior aborted session
job_helpers.remediate_prior_abort()

# Transferring jobs docket to queue
job_helpers.load_job()

# Chose output type for queue
options = ['.docx', '.pdf', '.txt', 'at terminal']
selected, index = pick(options, "Pick output type: ")


# Check for completed tasks in completed docket, and if they exist, 
# allow user to choose what to do with them
job_helpers.completed_options()

with open(dpt("queue"), 'r') as f:
    queue = [line for line in f.read().splitlines() if line.strip()]

printss("Starting Job")
for item in queue:
    printss(f"{job_helpers.queue_length()} items remaining in queue")
    job_helpers.update_queue(item) # Update queue.txt and in_progress.txt
    result = subprocess.run(
        [sys.executable, "main.py", item, str(index)],
        capture_output=True,
        text = True
    )

    # Parsing subprocess outputs for file completions
    output_name = None
    for line in result.stdout.splitlines():
        if line.startswith("OUTPUT_FILE_NAME:"):
            output_name = line.split("OUTPUT_FILE_NAME:")[1].strip()
            break
        else:
            printss(line)

    if output_name:
        with open(dpt("completed"), 'a', encoding='utf-8') as f:
            f.write(f"* {output_name}\n")
        print(f"COMPLETED: {output_name}")
    else:
        print(f"Error: Could not get output name for item. Subprocess stderr:\n{result.stderr}")

job_helpers.end_job()

printss("Queue Completed")
Chimes.terminal_chime()