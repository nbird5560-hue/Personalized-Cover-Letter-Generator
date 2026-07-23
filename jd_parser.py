# jd_parser.py
from pydantic import BaseModel, Field
from typing import List
from llm import ask_llm
import config

class ParsedJobDescription(BaseModel):
    job_title: str = Field(description="Exact job title from the posting.")
    company_name: str = Field(description="Name of the hiring company.")
    core_responsibilities: List[str] = Field(
        description="Top 3-5 concrete daily duties or operational responsibilities (exclude benefit/company info)."
    )
    required_tools_and_skills: List[str] = Field(
        description="Specific software, languages, certifications, or technical methods required."
    )
    key_pain_point: str = Field(
        description="The primary operational problem or strategic goal this position is hired to solve."
    )

JD_PARSER_SYSTEM_PROMPT = """You are a job description parser. 
Your goal is to extract core operational duties and technical requirements from scraped text while ignoring all benefits, EEOC disclaimers, company perks, and marketing boilerplate."""

def parse_job_description(raw_scraped_text: str) -> ParsedJobDescription:
    user_prompt = f"Scraped Job Posting Text:\n{raw_scraped_text}"
    return ask_llm(
        prompt=user_prompt,
        system_prompt=JD_PARSER_SYSTEM_PROMPT,
        model=config.JD_DEFAULT_MODEL,
        temp=0.1,  # Low temperature for strict extraction
        response_model=ParsedJobDescription
    )