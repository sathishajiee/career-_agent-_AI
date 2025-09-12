import os
import streamlit as st
from groq import Client
from PyPDF2 import PdfReader
from fpdf import FPDF

# ----------------- Groq Client -----------------
def get_groq_client():
    """
    Returns a Groq client using the API key stored in Streamlit secrets or environment variables.
    """
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("🚨 Missing GROQ_API_KEY. Please add it to .streamlit/secrets.toml or set as environment variable.")
        return None
    return Client(api_key=api_key)

# ----------------- PDF Text Extraction -----------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# ----------------- Create PDF from Text -----------------
def create_resume_pdf(text, filename="optimized_resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# ----------------- Career & Domain Functions -----------------
def get_domain_recommendation(skills, interests):
    client = get_groq_client()
    if not client:
        return "❌ API key missing. Cannot generate domain recommendation."
    prompt = f"Suggest the best career domain for someone with skills: {skills} and interests: {interests}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

def get_learning_resources(domain):
    client = get_groq_client()
    if not client:
        return []
    prompt = f"Provide 5 top learning resources (title & link) for the career domain: {domain}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    resources = []
    for line in response.choices[0].message["content"].split("\n"):
        if line.strip():
            parts = line.split(" - ")
            if len(parts) == 2:
                resources.append({"title": parts[0].strip(), "link": parts[1].strip()})
    return resources

def get_job_preparation_guide(job_title):
    client = get_groq_client()
    if not client:
        return "❌ API key missing. Cannot generate job preparation guide."
    prompt = f"Provide a detailed preparation guide for the job: {job_title}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

def get_skill_gap(target_job, current_skills):
    client = get_groq_client()
    if not client:
        return "❌ API key missing. Cannot generate skill gap analysis."
    prompt = f"Analyze the skill gap for someone with current skills: {current_skills} aiming for job: {target_job}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

def optimize_resume(job_description, resume_text):
    client = get_groq_client()
    if not client:
        return "❌ API key missing. Cannot optimize resume."
    prompt = f"Optimize the following resume to match this job description:\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()
