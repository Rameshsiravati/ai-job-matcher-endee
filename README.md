# ai-job-matcher-endee
#  AI Job Description Matcher — Built with Endee Vector Database

An AI-powered semantic job matching system that finds the best job openings for your resume using vector similarity search and LLM-generated feedback.


## System Design

User Resume → Sentence Transformers (embeddings) → Endee Vector DB (similarity search) → Gemini AI (feedback) → Streamlit UI

## Why Endee?

Endee is used as the core vector database for this project:
- **Index storage**: All job description vectors (384-dim) are stored in an Endee index
- **Similarity search**: Resume vectors are matched against stored job vectors using cosine similarity
- **Metadata filtering**: Job metadata (title, company, location, skills) stored as Endee payloads
- **Docker-based**: Endee runs as a Docker container on port 8080, making it portable and production-ready

##  Features

- Upload PDF resume or paste text
- Semantic search (not keyword search) — finds conceptual matches
- Match score with visual indicators  
- AI-powered feedback per job (what matches, what to improve)
- REST API with Swagger docs at /docs

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Vector DB | **Endee** (Docker) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Backend API | FastAPI |
| LLM Feedback | Google Gemini 1.5 Flash |
| Frontend | Streamlit |

##  Setup Instructions

### Prerequisites
- Docker Desktop installed
- Python 3.10+
- Gemini API key (free at aistudio.google.com)

### 1. Start Endee
```bash
docker run --ulimit nofile=100000:100000 -p 8080:8080 -v ./endee-data:/data --name endee-server endeeio/endee-server:latest
```

### 2. Clone and install
```bash
git clone https://github.com/Rameshsiravati/ai-job-matcher-endee.git
cd ai-job-matcher-endee
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  
```

### 3. Ingest jobs into Endee
```bash
python scripts/ingest_jobs.py
```

### 4. Run the application
```bash

uvicorn app.main:app --reload --port 8000

 
streamlit run ui/streamlit_app.py
```

Open http://localhost:8501 