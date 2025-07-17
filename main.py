import streamlit as st
import pdfplumber
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# PDF reader
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# GPT analyzer
def analyze_resume(resume, job_description):
    if not resume or not job_description:
        return "⚠️ Missing resume or job description."

    prompt = f"""
You are an expert career advisor. Analyze this resume for the job description below.

1. Match % between resume and job
2. Strengths (aligned skills and experience)
3. Weaknesses or missing areas
4. 3 resume improvement tips
5. ATS-friendliness score (1–10)

Resume:
{resume}

Job Description:
{job_description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Using the latest model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# --- Streamlit UI ---
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and job description (PDF or text) to get an AI-powered match analysis.")

# Create two columns for resume and job description
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")
    resume_option = st.radio("Resume Input:", ["Upload PDF", "Paste Text"], key="resume_option")
    
    if resume_option == "Upload PDF":
        uploaded_resume_pdf = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_pdf")
        resume_text = ""
        if uploaded_resume_pdf:
            resume_text = extract_text_from_pdf(uploaded_resume_pdf)
    else:
        resume_text = st.text_area("Paste Resume Text Here", height=200, key="resume_text")

with col2:
    st.subheader("💼 Job Description")
    job_option = st.radio("Job Description Input:", ["Upload PDF", "Paste Text"], key="job_option")
    
    if job_option == "Upload PDF":
        uploaded_job_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="job_pdf")
        job_description = ""
        if uploaded_job_pdf:
            job_description = extract_text_from_pdf(uploaded_job_pdf)
    else:
        job_description = st.text_area("Paste Job Description Here", height=200, key="job_text")

st.markdown("---")

if st.button("🔍 Analyze Resume", use_container_width=True):
    if resume_text and job_description:
        with st.spinner("Analyzing your resume against the job requirements..."):
            result = analyze_resume(resume_text, job_description)
            st.success("✅ Analysis Complete!")
            st.markdown(result)
    else:
        st.warning("Please provide both resume and job description content.")