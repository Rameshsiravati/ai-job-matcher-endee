import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.embedder import embed_text
from app.endee_client import create_index, upsert_job

def ingest_jobs():
    print("Creating Endee index...")
    result = create_index()
    print(f"Index creation: {result}")

    with open("data/sample_jobs.json", "r") as f:
        jobs = json.load(f)

    print(f"Ingesting {len(jobs)} jobs into Endee...")
    for job in jobs:
        text_to_embed = f"{job['title']} {job['description']} {' '.join(job['skills'])}"
        vector = embed_text(text_to_embed)
        
        metadata = {
            "title": job["title"],
            "company": job["company"],
            "description": job["description"],
            "skills": ", ".join(job["skills"]),
            "location": job["location"]
        }
        
        result = upsert_job(job["id"], vector, metadata)
        print(f"  Stored: {job['title']} at {job['company']}")

    print("\nAll jobs ingested into Endee successfully!")

if __name__ == "__main__":
    ingest_jobs()