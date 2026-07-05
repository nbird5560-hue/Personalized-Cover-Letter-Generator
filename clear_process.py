from job_helpers import dpt, wipe_file
import sys
from pathlib import Path
import os
from pick import pick
import re

arg_len = len(sys.argv)


if arg_len == 1:
    arg = sys.argv[0]# Should be string
    files = os.listdir(dpt(None))
    options = ["--Clear All--"]
    options.extend(files)
    options.append("--Exit--")


    to_clear = ""
    close_cases = ['--Exit--', '--Clear All--']
    while True:
        selected, index = pick(options, "Clear which file?")
        to_clear = options[index]
        to_clear = re.sub(r'\..+$','', to_clear)
        match to_clear:
            case "--Exit--":
                exit()
            case "--Clear All--":
                for item in to_clear-close_cases:
                    wipe_file(item)
                    exit()
            case _:
                wipe_file(to_clear)
        
        
else:
    args = [x.lower().strip() for x in sys.argv[1:]]

    if "all" in args:
        args = os.listdir(dpt(None))
    for item in args:
        path = Path(dpt(item))
        if path.exists():
            wipe_file(item)