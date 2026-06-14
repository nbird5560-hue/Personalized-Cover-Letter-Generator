import subprocess
import sys
import os
from pick import pick
from config import (printss, Chimes)

os.environ["AS_SUBPROCESS"] = True

def update_queue(item):
    with open("data/process/queue.txt", 'r') as f1:
        new_contents = f1.read().replace(item, '').strip('\n')
    with open("data/process/queue.txt", 'w') as f1:
        f1.write(new_contents)
    with open("data/process/in_progress.txt",'w') as f2:
        f2.write(item)

def load_job():
    with open("data/process/job.txt", 'r+') as f1:
        contents = f1.read()
        f1.seek(0)
        f1.truncate()
    with open("data/process/queue.txt", 'w') as f2:
        f2.write(contents)

def end_job():
    with open("data/process/queue.txt", 'w') as f1:
        f1.write("")
    with open("data/process/in_progress.txt", 'w') as f2:
        f2.write("")

def queue_length():
    with open("data/process/queue.txt", 'r') as f:
        return len(f.read().splitlines())


# Transferring jobs docket to queue
load_job()

# Chose output type for queue
options = ['.docx', '.pdf', '.txt', 'at terminal']
selected, index = pick(options, "Pick output type: ")

# Choice to clear completed.txt
selected, overwrite_index = pick(["No","Yes"],"Overwrite existing completed.txt?")
if overwrite_index:
    with open("data/process/completed.txt", 'w') as f:
        f.write("")

with open("data/process/queue.txt", 'r') as f:
    queue = [line for line in f.read().splitlines() if line.strip()]

printss("Starting Job")
for item in queue:
    printss(f"{queue_length()} items remaining in queue")
    update_queue(item) # Update queue.txt and in_progress.txt
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
        with open("data/process/completed.txt", 'a', encoding='utf-8') as f:
            f.write(f"* {output_name}\n")
        print(f"COMPLETED: {output_name}")
    else:
        print(f"Error: Could not get output name for item. Subprocess stderr:\n{result.stderr}")

end_job()

printss("Queue Completed")
Chimes.terminal_chime()