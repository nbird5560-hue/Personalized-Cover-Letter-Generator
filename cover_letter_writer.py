from llm import ask_llm
def write_cover_letter(
        resume,
        style_profile,
        job_description
):
    prompt = f"""
Use the writing style below

STYLE:

{style_profile}

RESUMES:

{resume}

JOB DESCRIPTION:

{job_description}

In the job description, ignore information irrelevant to the role.

Write a professional cover letter.

Use the provided writing style.

Only reference experiences, projects, and skills supported by the resume.

Focus on experiences and projects over education.

Limit usage of 'With a ..."

Use two spaces "  " after periods ".".
"""
    return ask_llm(prompt)