from llm import ask_llm
from config import extract_text_from_dir
from pathlib import Path
import unicodedata
import re

def create_style_profile():
    samples = extract_text_from_dir(Path("./data/writing_samples"))[:6000]# Remediating input overflow
    prompt = f"""You are an expert copywriter. Your task is to analyze the text provided below and generate a prompt for another LLM.

STEP 1: Analyze these writing samples for:
- Tone and Formality
- Vocabulary and Sentence Structure
- Common Habits

WRITING SAMPLES:
{samples}

-----------

STEP 2: Based on your analysis, create instructions to be read by an LLM for creating similar writing style to draft a cover letter.

Do not make the prompt overly constraining.

Do not say "Okay", do not explain your thinking. Output ONLY the final generated prompt.

"""

    response = ask_llm(prompt, "qwen3:4b")

    with open("data/profile.txt", 'w') as f:
        f.write(response)
    return response