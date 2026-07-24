# strategy_mapper.py
from pydantic import BaseModel, Field, model_validator
from typing import List, Literal
from llm import ask_llm
import config
from jd_parser import ParsedJobDescription
import logging

class ProofPoint(BaseModel):
    jd_duty: str = Field(
        description="Target responsibility from the job description."
    )
    resume_evidence: str = Field(
        description="quote or metric from the resume that proves capability."
    )
    match_confidence: Literal["STRONG_MATCH", "TRANSFERABLE_SKILL", "WEAK_MATCH"] = Field(
        description="Assess how directly the resume quote supports the job duty."
    )
    mapping_narrative: str = Field(
        description="1-2 sentences explaining how this specific experience directly addresses the target duty."
    )

    @model_validator(mode='after')
    def log_match_confidence(self) -> ProofPoint:
        """Automatically logs match quality upon validation"""
        log_msg = (
            f"MATCH CONFIDENCE [{self.match_confidence}]:--"
            f"Mapped Duty: {self.jd_duty} |" 
            f"Resume Match: {self.resume_evidence}"
        )
        
        if self.match_confidence == "WEAK_MATCH":
            logging.warning(log_msg)
        else:
            logging.info(log_msg)
        return self


class WritingStrategy(BaseModel):
    company_hook: str = Field(
        description="Reason why the candidate's specific background fits the company's core pain point."
    )
    proof_points: List[ProofPoint] = Field(
        min_length=2, 
        max_length=2, 
        description="Top 2 strongest grounded proof points."
    )
    missing_skill_warnings: List[str] = Field(
        default=[],
        description="Key job requirements that the candidate lacks on their resume. Use this to avoid making false assertions."
    )

class SkillComparison(BaseModel):
    skills: List[str] = Field(
        min_length=3,
        max_length=5,
        description="Top 3-5 skills or proficiencies required by job description that are supported by the user's resume"
    )



def generate_strategy(parsed_jd: ParsedJobDescription, resume_text: str) -> WritingStrategy:
    MAPPER_SYSTEM_PROMPT = """You are a precision talent analyst.
Map the target job requirements to the candidate's resume.

[CRITICAL GROUNDING RULES]
1. `resume_evidence` MUST be directly drawn and supported from the resume.
2. If the candidate lacks direct experience for a requirement, mark confidence as 'TRANSFERABLE_SKILL' or 'WEAK_MATCH'—DO NOT invent or exaggerate experience.
3. If a key JD skill is completely missing from the resume, log it in `missing_skill_warnings`.
"""
    
    user_prompt = f"""
[PARSED JOB DESCRIPTION]
Title: {parsed_jd.job_title} at {parsed_jd.company_name}
Core Responsibilities: {parsed_jd.core_responsibilities}
Tools & Skills Required: {parsed_jd.required_tools_and_skills}
Core Pain Point: {parsed_jd.key_pain_point}

[RESUME]
{resume_text}
"""
    return ask_llm(
        prompt=user_prompt,
        system_prompt=MAPPER_SYSTEM_PROMPT,
        model=config.JD_DEFAULT_MODEL,
        temp=0.1,
        response_model=WritingStrategy
    )

def match_skills(parsed_jd: ParsedJobDescription, resume_text: str) -> SkillComparison:
    SKILLS_MATCHER_SYSTEM_PROMPT = """You are a precision talent analyst.
Map required skills and compentencies to the candidate's resume

[CRITICAL RULES]
1. Matched skills and proficiencies must be supported by candidate's resume.
2. Skills / proficiencies more relevant to the job description should be prioritized. 
"""

    user_prompt = f"""
[PARSED JOB DESCRIPTION]
{parsed_jd}

[RESUME]
{resume_text}
"""
    return ask_llm(
        system_prompt=SKILLS_MATCHER_SYSTEM_PROMPT,
        prompt=user_prompt,
        model=config.JD_DEFAULT_MODEL,
        temp=0.1,
        response_model=SkillComparison
    )


