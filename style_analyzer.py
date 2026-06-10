from llm import ask_llm
from config import extract_text_from_dir
from pathlib import Path

def create_style_profile():
    samples = extract_text_from_dir(Path("./data/writing_samples"))

    prompt = f"""
Analyze this writing.

Describe:

- Tone
- Formality
- Vocabulary
- Sentence Structure
- Common Habits

Writing:

{samples}
#Trial
Write the output formatted as a prompt for another llm writing a similar cover letter based on this writing profile.
"""
    response = ask_llm(prompt)
    with open("data/profile.txt", 'w') as f:
        f.write(response)
    return response