from llm import ask_llm

def analyze_job_description(description, resume):

    prompt = f"""Analyze this job description and my resume. 
Provide a bulleted list of the top 3 overlapping skills I should highlight in a cover letter,
and what hook I should use for the opening paragraph.

Your output should only be an output following the above instructions, formatted such that it is readable by an LLM.

Do not address the user in your output.
 
JOB DESCRIPTION:
{description}

RESUME:
{resume}

 """
    return ask_llm(prompt, model="deepseek-r1:8b")