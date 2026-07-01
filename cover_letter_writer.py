# cover_letter_generator.py
from pydantic import BaseModel, Field, field_validator
from typing import List
import re
from llm import ask_llm

# Define the structured layout for your cover letters
class CoverLetterSchema(BaseModel):
    salutation: str = Field(description="The formal greeting line, e.g., 'Dear Hiring Team,'")
    body_paragraphs: List[str] = Field(description="The body content split into paragraphs.")
    sign_off: str = Field(description="The closing phrase and signature name, e.g., 'Sincerely,\nJane Doe'")

    # Programmatic cleanup: Pydantic fixes text formatting constraints automatically!
    @field_validator("body_paragraphs", mode="after")
    @classmethod
    def enforce_formatting_constraints(cls, paragraphs: List[str]) -> List[str]:
        cleaned_paragraphs = []
        for paragraph in paragraphs:
            # 1. Remove emdashes
            p = paragraph.replace("–", "-")
            # 2. Force exactly two spaces after every period (collapsing existing multi-spaces first)
            p = re.sub(r'\.\s+', '.  ', p)
            cleaned_paragraphs.append(p)
        return cleaned_paragraphs

    # Helper property to seamlessly compile the object back into a text string
    @property
    def full_text(self) -> str:
        body = "\n\n".join(self.body_paragraphs)
        return f"{self.salutation}\n\n{body}\n\n{self.sign_off}"


# Write initial cover letter
def write_cover_letter(resume, style_profile, writing_strategy, job_description) -> CoverLetterSchema:
    """
    Initial cover letter writing pass. Forces structured JSON extraction via Pydantic.
    """
    prompt = f"""
You are an expert career coach writing a tailored cover letter.
[CRITICAL INSTRUCTIONS]
1. Write a professional cover letter under 500 words based on the strategy.
2. Rely strictly on experiences and projects from the resume.
3. Projects occurring at the same time as experiences are not always related to the experience role.
4. Match the tone in the STYLE PROFILE.
5. Crucial: Do NOT use overly enthusiastic corporate clichés.
6. In your 'sign_off' data field, include ONLY a standard formal closing and your name (e.g., "Sincerely,\n[Name]"). Do not append system instructions or commentary.

[CONTEXT DATA]
STYLE PROFILE: {style_profile}
RESUME DATA: {resume}
STRATEGY: {writing_strategy}
JOB DESCRIPTION: {job_description}
"""
    # Returns a validated CoverLetterSchema object
    return ask_llm(prompt, model="qwen3:8b", temp=0.65, response_model=CoverLetterSchema)


# Revise cover letter
def revise_cover_letter(cover_letter: str, job_description, resume, writing_style) -> CoverLetterSchema:

    """
    Cover letter generation second pass. Reviews, adjusts layout, and outputs a clean schema object.
    """
    prompt = f"""
You are a hiring manager reviewing a draft cover letter against a job description and resume.
Your task is to rewrite the letter to eliminate weaknesses while adhering to structural guidelines.

[REVISION RULES]
- Address the appropriate hiring manager or team at the start.
- Sign off using the user's name from the resume.

[INPUT DATA]
<cover_letter>{cover_letter}</cover_letter>
<job_description>{job_description}</job_description>
<resume>{resume}</resume>
<writing_style>{writing_style}</writing_style>
"""
    # Returns a validated, formatting-corrected CoverLetterSchema object
    return ask_llm(prompt, "qwen3:8b", temp=0.2, response_model=CoverLetterSchema)