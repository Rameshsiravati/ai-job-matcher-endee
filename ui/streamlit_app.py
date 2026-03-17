import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Job Matcher",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Job Description Matcher")
st.markdown("*Powered by Endee Vector Database + Semantic Search*")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Your Resume")
    
    input_method = st.radio("Input method:", ["Paste Text", "Upload PDF"])
    
    resume_text = ""
    
    if input_method == "Paste Text":
        resume_text = st.text_area(
            "Paste your resume here:",
            height=300,
            placeholder="Python developer with 3 years of experience in machine learning, FastAPI, and Docker..."
        )
    else:
        uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"])
    
    top_k = st.slider("Number of matches to return", 1, 6, 3)
    
    search_btn = st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True)

with col2:
    st.subheader("How It Works")
    st.markdown("""
    1. **Your resume** is converted to a vector embedding using Sentence Transformers
    2. **Endee Vector DB** does lightning-fast similarity search across all job descriptions  
    3. **Top matches** are returned by cosine similarity score
    4. **Gemini AI** explains why you match and what skills to improve
    """)
    
    st.info("💡 The vector search finds semantic matches — not just keyword matches. 'ML Engineer' will match 'Deep Learning Developer' too!")

st.divider()

if search_btn:
    with st.spinner("Searching for matches in Endee..."):
        try:
            if input_method == "Paste Text" and resume_text:
                response = requests.post(
                    f"{API_URL}/match/text",
                    json={"text": resume_text, "top_k": top_k}
                )
            elif input_method == "Upload PDF" and uploaded_file:
                response = requests.post(
                    f"{API_URL}/match/pdf",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                )
            else:
                st.warning("Please enter your resume text or upload a PDF.")
                st.stop()
            
            data = response.json()
            matches = data.get("matches", [])
            
            if not matches:
                st.warning("No matches found. Make sure Endee is running and jobs are ingested.")
            else:
                st.success(f"Found {len(matches)} matching jobs!")
                
                for i, match in enumerate(matches):
                    score = match['score']
                    color = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                    
                    with st.expander(f"{color} #{i+1} — {match['title']} at {match['company']} | Match: {score}%", expanded=(i==0)):
                        col_a, col_b = st.columns([1, 2])
                        
                        with col_a:
                            st.metric("Match Score", f"{score}%")
                            st.write(f"📍 **Location:** {match['location']}")
                            st.write(f"🛠️ **Skills:** {match['skills']}")
                        
                        with col_b:
                            st.write("**🤖 AI Feedback:**")
                            st.info(match['feedback'])
        
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the API. Make sure the FastAPI server is running on port 8000.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

