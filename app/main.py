from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import io
import os

from app.embedder import embed_text
from app.endee_client import search_similar_jobs, check_health
from app.llm_feedback import get_match_feedback

app = FastAPI(title="AI Job Matcher API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeText(BaseModel):
    text: str
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "AI Job Matcher API is running!"}

@app.get("/health")
def health():
    endee_ok = check_health()
    return {"api": "ok", "endee": "ok" if endee_ok else "error"}

@app.post("/match/text")
def match_resume_text(resume: ResumeText):
    """Match a resume (as text) against all job descriptions in Endee."""
    vector = embed_text(resume.text)
    results = search_similar_jobs(vector, top_k=resume.top_k)
    
    matches = []
    for hit in results.get("results", []):
        job = hit.get("payload", {})
        score = hit.get("score", 0)
        
        try:
            feedback = get_match_feedback(resume.text, job, score)
        except Exception:
            feedback = "AI feedback unavailable."
        
        matches.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "skills": job.get("skills"),
            "score": round(score * 100, 1),
            "feedback": feedback
        })
    
    return {"matches": matches}

@app.post("/match/pdf")
async def match_resume_pdf(file: UploadFile = File(...)):
    """Match a PDF resume against all job descriptions."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")
    
    content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")
    
    vector = embed_text(text)
    results = search_similar_jobs(vector, top_k=5)
    
    matches = []
    for hit in results.get("results", []):
        job = hit.get("payload", {})
        score = hit.get("score", 0)
        
        try:
            feedback = get_match_feedback(text, job, score)
        except Exception:
            feedback = "AI feedback unavailable."
        
        matches.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "skills": job.get("skills"),
            "score": round(score * 100, 1),
            "feedback": feedback
        })
    
    return {"matches": matches, "resume_preview": text[:300] + "..."}