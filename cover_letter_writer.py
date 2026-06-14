from llm import ask_llm

# Write initial cover letter
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



# Revise cover letter
def revise_cover_letter(cover_letter, job_description, resume):
    prompt = """
You are a hiring manager for the company receiving this cover letter.
Review the provided cover letter against the job description and resume, then rewrite it to remediate weaknesses.

CRITICAL INSTRUCTIONS:
- Do not address the user in your response.
- Start the output with addressing the appropriate hiring manager or team.
- Only reference experiences and projects supported by the resume.  Skills can be inferred.
- Ensure there are no uses of emdash "–".
- Collect related sentences together.
- Conclude the revised letter by signing as the user's name.
- Use two spaces '  ' after periods '.'.

[INPUT DATA]
<cover_letter>
{cl}
</cover_letter>

<job_description>
{jd}
</job_description>

<resume>
{res}
</resume>

----

The output should solely a revised cover letter, without addressing the user or including headlines.
"""
    final_prompt = prompt.format(
        cl=cover_letter.strip(), 
        jd=job_description, 
        res=resume
    )
    output = ask_llm(final_prompt, "deepseek-r1:8b")
    return output