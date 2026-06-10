# llm.py
from ollama import chat
from pick import pick
from config import Chimes
import inspect
from pathlib import Path

def ask_llm(prompt: str):
    models = ["gemma3:4b", "gemma4:e4b"]

    # Setup exception
    caller_file_abs = Path(inspect.stack()[1].filename).resolve()
    project_root = Path.cwd().resolve()
    try:
        relative_path = caller_file_abs.relative_to(project_root)
    except ValueError:
        # Fallback if the caller is outside of the project root directory
        print(f"Caller is outside project root: {caller_file_abs}")

    if str(relative_path) == "setup.py":
        ask_llm.model_chosen = "gemma3:4b"
    
    if not hasattr(ask_llm, "model_chosen"):
        Chimes.input_chime()
        selected, index = pick(models, "Pick LLM Model")
        ask_llm.model_chosen = models[index]

    response = chat(
        model=getattr(ask_llm, "model_chosen"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False
    )

    try:
        # Version handling for ollama output
        if isinstance(response, dict):
            raw_content = response["message"]["content"]
        else:
            raw_content = response.message.content
            
    except (KeyError, AttributeError) as e:
        print(f"ERROR parsing Ollama response: {e}")
        print(f"Raw response structure was: {response}")
        return ""

    return raw_content