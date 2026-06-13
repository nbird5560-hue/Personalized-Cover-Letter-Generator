from ollama import chat
from pick import pick
from config import Chimes
import inspect
from pathlib import Path
import re
import unicodedata

def ask_llm(prompt: str, model: str = None):

    if not model:
        models = ["gemma3:4b", "gemma4:e4b", "qwen3:4b", "llama3:8b"]
        Chimes.input_chime()
        selected, index = pick(models, "Pick LLM Model")
        model = models[index]

    response = chat(
        model=model,
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



    return clean_xml_string(raw_content)

def clean_xml_string(text):
    if not isinstance(text, str):
        return text
    # Keep standard printables, tabs, newlines, carriage returns, and valid Unicode ranges
    # Strips out null bytes (\x00) and unsupported control characters
    illegal_xml_re = re.compile(
        r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufeff\ufffe\uffff]'
    )
    return illegal_xml_re.sub('', text)