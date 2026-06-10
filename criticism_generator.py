from llm import ask_llm

def revise_cover_letter(cover_letter, job_description, resume):
    prompt = """
You are a hiring manager for the company receiving this cover letter.
Review the provided cover letter against the job description and resume, then rewrite it to remediate weaknesses.

CRITICAL INSTRUCTIONS:
- Do not address the user in your response.
- Only reference experiences, projects, and skills supported by the resume.
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

"""
    final_prompt = prompt.format(
        cl=cover_letter.strip(), 
        jd=job_description, 
        res=resume
    )
    output = ask_llm(final_prompt)
    return output
