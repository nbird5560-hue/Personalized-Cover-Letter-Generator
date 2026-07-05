import subprocess
import os
import sys

def launch_ahk_script(script_name="script.ahk"):
    # 1. Get the absolute path to your AHK script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ahk_script_path = os.path.join(current_dir, script_name)
    
    # 2. Define the path to the AHK v2 executable
    # If AHK v2 is installed globally, "AutoHotkey64.exe" or "AutoHotkey.exe" is usually in PATH.
    # Alternatively, provide the absolute path (e.g., r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe")
    ahk_executable = "AutoHotkey64.exe" 
    
    print(f"Launching {script_name} from virtual environment...")
    
    try:
        # Popen runs it in the background as a subprocess
        process = subprocess.Popen(
            [ahk_executable, ahk_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"AHK script is now running in the background. (PID: {process.pid})")
        return process
        
    except FileNotFoundError:
        print("Error: Could not find the AutoHotkey executable.", file=sys.stderr)
        print("Please ensure AutoHotkey v2 is installed and added to your system PATH,", file=sys.stderr)
        print("or hardcode the absolute path to AutoHotkey64.exe in this script.", file=sys.stderr)
        return None

launch_ahk_script("auxiliary/SaveJobLink.ahk")