import subprocess
import sys
from pick import pick
from config import (printss, Chimes)

def update_queue(item):
    with open("data/process/queue.txt", 'r+') as f1:
        new_contents = f1.read().replace(item, '').strip('\n')
        f1.write(new_contents)    
    with open("data/process/in_progress.txt",'w') as f2:
        f2.write(item)

def load_job():
    with open("data/process/job.txt", 'r+') as f1:
        contents = f1.read()
        f1.write("")
    with open("data/process/queue.txt", 'w') as f2:
        f2.write(contents)

def end_job():
    with open("data/process/queue.txt", 'w') as f1:
        f1.write("")
    with open("data/process/in_progress.txt", 'w') as f2:
        f2.write("")


# Transferring jobs docket to queue
load_job()

# Chose output type for queue
options = ['.docx', '.pdf', '.txt', 'at terminal']
selected, index = pick(options, "Pick output type: ")

# Choice to clear completed.txt
selected, overwrite = pick(["No","Yes"],"Overwrite existing completed.txt?")
if overwrite:
    with open("data/process/completed.txt", 'w') as f:
        f.write("")

with open("data/process/queue.txt", 'r') as f:
    queue = [line for line in f.read().splitlines() if line.strip()]

printss("Starting Job")
for item in queue:
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
Chimes.progress_chime()
Chimes.ending_chime()