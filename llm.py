# llm.py
from ollama import chat
from pick import pick
from config import Chimes
from pydantic import BaseModel
from typing import Type, Optional, Union
import re

def ask_llm(
    prompt: str, 
    model: str = None, 
    temp: float = 0.5, 
    response_model: Optional[Type[BaseModel]] = None
) -> Union[str, BaseModel]:

    if temp is not None:
        if temp >= 1 or temp < 0:
            raise ValueError("Value of Temp argument must be in [0, 1).")

    if not model:
        models = ["gemma3:4b", "gemma4:e4b", "qwen3:4b", "deepseek-r1:8b"]
        Chimes.input_chime()
        selected, index = pick(models, "Pick LLM Model")
        model = models[index]

    # Set up the default chat arguments
    chat_kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": temp,
            "num_predict": 1024,  # Ensures the model can finish writing without hitting an EOF cutoff
            "num_ctx": 8192,      # Gives plenty of memory for large Resumes + Job Descriptions
            "repeat_penalty": 1.1, # Prevents the model from getting stuck in looping logic
        }
    }

    # CRITICAL: If a Pydantic model is provided, force Ollama to output strict JSON
    if response_model:
        chat_kwargs["format"] = response_model.model_json_schema()

    response = chat(**chat_kwargs)
    
    try:
        if isinstance(response, dict):
            raw_content = response["message"]["content"]
        else:
            raw_content = response.message.content
            
    except (KeyError, AttributeError) as e:
        print(f"ERROR parsing Ollama response: {e}")
        return ""

    cleaned_content = clean_xml_string(raw_content)

    # If structured output was requested, validate it safely
    if response_model:
        try:
            return response_model.model_validate_json(cleaned_content)
        except Exception as json_err:
            print("\n[!] LLM Output Truncated or Invalid JSON. Raw output was:")
            print(cleaned_content)
            print(f"[!] Validation Error: {json_err}")
            
            # Fallback: Return an empty instance of your schema so main.py doesn't crash
            # This allows your loop/logic to continue or retry safely.
            return response_model(
                salutation="Dear Hiring Manager,",
                body_paragraphs=["[Generation failed due to LLM timeout/context cutoff. Please try again.]"],
                sign_off="Sincerely,\n[Your Name]"
            )

    return cleaned_content


def clean_xml_string(text):
    if not isinstance(text, str):
        return text
    illegal_xml_re = re.compile(
        r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufeff\ufffe\uffff]'
    )
    return illegal_xml_re.sub('', text)