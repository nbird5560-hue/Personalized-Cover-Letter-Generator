from llm import ask_llm
def write_cover_letter(
        resume,
        style_profile,
        writing_strategy
):
    prompt = f"""
Use the writing style below

STYLE:

{style_profile}

RESUMES:

{resume}

WRITING STRATEGY:

{writing_strategy}

------------------

Based on the writing strategy:

Write a professional cover letter.

Use the provided writing style.

Only reference experiences and projects, supported by the resume.  Skills may be inferred.

Focus on experiences and projects over education.

Limit usage of 'With a ..."

Use two spaces "  " after periods ".".

Avoid overly enthusiastic corporate clichés.

Keep it under 300 words."
"""
    return ask_llm(prompt, model="qwen3:4b")