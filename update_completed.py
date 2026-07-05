from utils import nsep
from pick import pick
from job_helpers import (dpt, wipe_file)


def get_contents(filename: str) -> list[str]:
    with open(dpt(filename), 'r') as f:
        contents = [line for line in f.read().splitlines() if line.strip()]
        contents.insert(len(contents), "Clear All")
        contents.insert(len(contents), "Exit")
    return contents


def run_selection(contents):
    remove = ""
    while remove != "Exit":
        selected, index = pick(contents, "Remove which job? 'Exit' to quit, 'Clear All' to clear all.")
        remove = contents[index]

        if remove == "Clear All":
            wipe_file(contents)
            exit()
        else:
            contents = [item for item in contents if item != remove]
    
    if "Clear All" in contents:
        contents.remove("Clear All")


    with open(dpt("completed"), 'w') as f:
        f.write(nsep(*contents))

contents = get_contents("completed")
run_selection(contents)