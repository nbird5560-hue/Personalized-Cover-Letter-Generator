import subprocess
import sys
import os
import session_info
import datetime
from pick import pick
from config import (printss, Chimes)
import job_helpers
from job_helpers import dpt

time_1 = datetime.now()

# Establishing session as including subprocesses
os.environ["AS_SUBPROCESS"] = "True"

job_helpers.ensure_ollama_running()

# Checking for prior aborted session
job_helpers.remediate_prior_abort()

# Transferring jobs docket to queue
job_helpers.load_job()

# Chose output type for queue
options = ['.docx', '.pdf', '.txt', 'at terminal']
selected, index = pick(options, "Pick output type: ")

# Check for completed tasks in completed docket, and if they exist, 
# allow user to choose what to do with them
#job_helpers.completed_options()

with open(dpt("queue"), 'r') as f:
    queue = [line for line in f.read().splitlines() if line.strip()]
queue_length = len(queue) 
printss("Starting Job")
for item in queue:
    item.strip() # safety operations in case user manually modifies queue.txt
    item.strip("\n") 
    printss(f"{job_helpers.queue_length()} items remaining in queue")
    job_helpers.update_queue(item) # Update queue.txt and in_progress.txt
    result = subprocess.run(
        [sys.executable, "-u", "main.py", item, str(index)],
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
            if line.startswith("Script executed in"):
                print(line)
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

time_2 = datetime.now()

delta = time_2 - time_1
days = delta.days
hours = delta.seconds // 3600
minutes = (delta.seconds % 3600) // 60
seconds = delta.seconds % 60
timelist = [seconds, minutes, hours, days]
nameslist = ["seconds", "minutes", "hours", "days"]

def make_string(unit, name):
    return f"{unit} {name}, " if unit else ""

string_list= [make_string(unit, name) for unit, name in zip(timelist, nameslist)][::-1]
string = "TOTAL TIME ELAPSED: " + "".join(string_list).strip(", ")

print(string)
session_info.show()