from config import nsep
from pick import pick

def dpt(filename: str) -> str:
    return "data/process/" + filename + ".txt"

def wipe_file(filename: str):
    with open(dpt(filename), 'w') as f:
        f.write("")

def update_queue(item):
    with open(dpt("queue"), 'r+') as f1:
        new_contents = f1.read().replace(item, '').strip('\n')
        f1.seek(0)
        f1.truncate()
        f1.write(new_contents)
    with open(dpt("in_progress"),'w') as f2:
        f2.write(item)

def load_job():
    with open(dpt("job"), 'r+') as f1:
        contents = f1.read()
        f1.seek(0)
        f1.truncate()
    with open(dpt("queue"), 'w') as f2:
        f2.write(contents)

def end_job():
    wipe_file("queue")
    wipe_file("in_progress")
    
def queue_length():
    with open(dpt("queue"), 'r') as f:
        return len(f.read().splitlines())

def remediate_prior_abort():
    with open(dpt("queue"), 'r') as f1:
        queue = f1.read()
    with open(dpt("in_progress"), 'r') as f2:
        in_progress = f2.read()
    if queue or in_progress:
        with open(dpt("job"), 'r+') as f3:
            job = f3.read()
            f3.seek(0)
            f3.truncate()
        selected, abort_index = pick(
            ["Pick up from where last session left off", "Send unfinished cover letters to end of queue", "Delete unfinished cover letters"],
            "System detects previous session was prematurely aborted.  Chose how to proceed:"
            )
        
        match abort_index:
            case 0:
                new_contents = nsep(in_progress, queue, job) 
            case 1:
                new_contents = nsep(job, in_progress, queue)
            case 2:
                new_contents = job

        #print(new_contents) # Debugging

        with open(dpt("job"), "w") as f3:
            f3.write(new_contents)
        
        wipe_file("queue")
        wipe_file("in_progress")

def completed_options():
    with open(dpt("completed"), 'r') as f:
        items = [line for line in f.read().splitlines() if line.strip()]
        fl = f"First:\n{items[0]}\nLast:\n{items[len(items)-1]}"

    if items:
        selected, index = pick(["No", "Yes"], "Output log of previous job(s) detected:\n" + fl + "\n Clear log?")
        if index:
            wipe_file("completed")


import subprocess
import time
import urllib.request

def ensure_ollama_running():
    print("Checking Ollama status...")
    try:
        # Check if the Ollama server is already responding
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        print("Ollama is already running.")
    except Exception:
        print("Ollama is not running. Spinning it up now...")
        try:
            # Launch Ollama as a background process (detached)
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW # Windows-specific flag
            )
            # Give the server a few seconds to fully initialize
            time.sleep(4) 
            print("Ollama started successfully.")
        except FileNotFoundError:
            print("Error: 'ollama' command not found. Is it installed and added to your PATH?")