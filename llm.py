from ollama import chat
from pick import pick
from config import Chimes
import re

def ask_llm(prompt: str, model: str = None, temp: float = 0.5):

    if not temp is None:
        if temp >= 1 or temp < 0:
            raise ValueError("Value of Temp argument must be in [0, 1).")

    if not model:
        models = ["gemma3:4b", "gemma4:e4b", "qwen3:4b", "deepseek-r1:8b"]
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
        stream=False,
        options={
            "temperature": temp
        }
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