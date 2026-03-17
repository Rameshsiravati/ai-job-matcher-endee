import requests

ENDEE_URL = "http://localhost:8080"
INDEX_NAME = "job_descriptions"
VECTOR_DIM = 384

def create_index():
    """Create the Endee index for job descriptions."""
    payload = {
        "name": INDEX_NAME,
        "dimension": VECTOR_DIM,
        "metric": "cosine"
    }
    response = requests.post(f"{ENDEE_URL}/api/v1/index/create", json=payload)
    return response.json()

def upsert_job(job_id: str, vector: list, metadata: dict):
    """Store a job description vector in Endee."""
    payload = {
        "vectors": [
            {
                "id": job_id,
                "values": vector,
                "payload": metadata
            }
        ]
    }
    response = requests.post(
        f"{ENDEE_URL}/api/v1/index/{INDEX_NAME}/upsert",
        json=payload
    )
    return response.json()

def search_similar_jobs(query_vector: list, top_k: int = 5):
    """Find the top-k most similar job descriptions."""
    payload = {
        "vector": query_vector,
        "top_k": top_k,
        "with_payload": True
    }
    response = requests.post(
        f"{ENDEE_URL}/api/v1/index/{INDEX_NAME}/search",
        json=payload
    )
    return response.json()

def check_health():
    response = requests.get(f"{ENDEE_URL}/api/v1/health")
    return response.status_code == 200