# cover_letter_generator.py
from pydantic import BaseModel, Field, field_validator
from typing import List
import re
from llm import ask_llm
import config
from strategy_mapper import WritingStrategy

# Define the structured layout for your cover letters
class CoverLetterSchema(BaseModel):
    salutation: str = Field(description="A formal generic greeting line, e.g., 'Dear Hiring Team,'")
    opening_paragraph: str = Field(description="Opening paragraph with an engaging hook. State the position you are applying to and a reason why you are excited about the role.")
    middle_paragraphs: List[str] = Field(
        min_length=2,
        max_length=2,
        description="Two middle body paragraphs. Highlight on the two most job-description-related accomplishments, experiences, or projects and explain how the user's unique skills can help the employer solve their current challenges."
    )
    skills_paragraph: str = Field(description="Without a preface, provide 2-3 sentences about skills the user has related to the job description, supported by the skills tag. Simply state the candidates skills and proficiencies without mentioning specific projects. (e.g. 'I am proficient in R, Python, and SQL, and have experience designing experiements to drive business decisions.', 'I am a strong communicator, and pride myself in being able to communicate complex material to technical and nontechnical audiences alike.')")
    closing_paragraph: str = Field(description="A final paragraph assuring the reader of the user's ability to work for the hiring company and thanking the reader for considering the user's application.  Do not label the paragraph. Include no sign off in this section.")
    valediction: str = Field(default="Sincerely,", description="Formal sign-off phrase, e.g., 'Sincerely,' or 'Best regards,'")
    candidate_name: str = Field(description="Full name of the applicant extracted from the resume.")
    
    @classmethod
    def _clean_text(cls, text: str) -> str:
        text = text.replace("\u2014", ", ")
        text = re.sub(r'\.[ \t]+', '. ', text)
        return text
    
    # Programmatic cleanup    
    @field_validator("opening_paragraph", "middle_paragraphs", "skills_paragraph", "closing_paragraph", mode="after")
    @classmethod
    def enforce_formatting_constraints(cls, value: any) -> any:
        if isinstance(value, list):
            return [cls._clean_text(p) for p in value]
        return cls._clean_text(value)

    # Helper property to seamlessly compile the object back into a text string
    @property
    def full_text(self) -> str:
        body_sections = [
            self.opening_paragraph,
            *self.middle_paragraphs,
            self.skills_paragraph,
            self.closing_paragraph
        ]
        body = "\n\n".join(body_sections)
        return f"{self.salutation}\n\n{body}\n\n{self.valediction}\n\n{self.candidate_name}"

# Write initial cover letter
def write_cover_letter(
        resume: str,
        style_profile: str,
        strategy: WritingStrategy,
        skills: List[str]) -> CoverLetterSchema:
    
    SYSTEM_PROMPT = """You are an expert career writer drafting a tailored cover letter.

[WRITING RULES]
1. Translate the provided STRATEGIC BLUEPRINT into polished paragraphs.
2. Build middle body paragraph 1 around Proof Point 1.
3. Build middle body paragraph 2 around Proof Point 2.
4. Build skills paragraph from matched skills.
5. DO NOT make generic claims (e.g., "As someone with experience in complex datasets...").
6. Connect every claim directly to the resume evidence specified in the strategy.
"""

    user_prompt = f"""
[STRATEGIC BLUEPRINT]
Opening Hook Strategy: {strategy.company_hook}

Proof Point 1:
- Requirement: {strategy.proof_points[0].jd_duty}
- Resume Proof: {strategy.proof_points[0].resume_evidence}
- Strategic Angle: {strategy.proof_points[0].mapping_narrative}

Proof Point 2:
- Requirement: {strategy.proof_points[1].jd_duty}
- Resume Proof: {strategy.proof_points[1].resume_evidence}
- Strategic Angle: {strategy.proof_points[1].mapping_narrative}

Skills paragraph detailing candidate's proficiences and skills related to the job posting:
{skills}

[CONTEXT DATA]
STYLE PROFILE: 
{style_profile}

RESUME DATA: 
{resume}

WRITING STRATEGY: 
{strategy}
"""

    return ask_llm(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT,
        model=config.WRITER_DEFAULT_MODEL,
        temp=0.6,
        response_model=CoverLetterSchema
    )

# Revise cover letter
def revise_cover_letter(cover_letter: str, strategy: WritingStrategy, resume, skills, style_profile) -> CoverLetterSchema:
    """
    Cover letter generation second pass. Reviews, adjusts layout, and outputs a clean schema object.
    """
    SYSTEM_PROMPT = """
    [CORE RULES]
    1. Base all content strictly on the provided resume. Do not fabricate experiences.
    2. Maintain a direct, professional, and pragmatic tone. Avoid corporate clichés.
    3. Match the writing style constraints provided in the user request.   
    4. Output valid data matching the requested schema.
    """

    PROMPT = f"""
Revise the cover letter based on the following rules and data:
[REVISION RULES]
- Address the appropriate hiring team at the start.
- Sign off using the user's name from the resume.
- Do not reference sections of the schema in your output.
- Check that skills mentioned in the skills paragraph are in the skills tag.
- Ensure the skills paragraph is concise but informative.
[INPUT DATA]
<cover_letter>{cover_letter}</cover_letter>
<strategy>{strategy}</strategy>
<resume>{resume}</resume>
<skills>{skills}</skills>
<style_profile>{style_profile}</style_profile>
"""
    # Returns a validated, formatting-corrected CoverLetterSchema object
    return ask_llm(system_prompt=SYSTEM_PROMPT, prompt=PROMPT, model=config.REVISOR_DEFAULT_MODEL, temp=0.2, response_model=CoverLetterSchema)