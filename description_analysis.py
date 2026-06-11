from llm import ask_llm

def analyze_job_description(description, resume):

    prompt = f"""Analyze this job description and my resume. 
Provide a bulleted list of the top 3 overlapping skills I should highlight,
and what hook I should use for the opening paragraph.
 
JOB DESCRIPTION:
{description}

RESUME:
{resume}

 """
    return ask_llm(prompt, model="deepseek-r1:8b")