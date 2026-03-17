import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_match_feedback(resume_text: str, job: dict, score: float) -> str:
    """Generate personalized feedback for a resume-job match."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""You are a career advisor. Analyze how well this resume matches the job description.

RESUME:
{resume_text[:2000]}

JOB TITLE: {job.get('title')}
COMPANY: {job.get('company')}
JOB DESCRIPTION: {job.get('description')}
REQUIRED SKILLS: {job.get('skills')}
SIMILARITY SCORE: {score:.2%}

Provide a brief analysis (3-4 sentences) covering:
1. Why this is a {('strong' if score > 0.7 else 'moderate' if score > 0.5 else 'partial')} match
2. Key matching skills
3. One skill gap to address

Keep it concise and actionable."""

    response = model.generate_content(prompt)
    return response.text