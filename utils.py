import os
from groq import Client
from PyPDF2 import PdfReader
from fpdf import FPDF

# Initialize Groq client using environment variable
import streamlit as st
from groq import Client

client = Client(api_key=st.secrets["GORK_API_KEY"])


# ---------------- Text Extraction from PDF ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# ---------------- Create PDF from text ----------------
def create_resume_pdf(text, output_file="optimized_resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(output_file)
    return output_file

# ---------------- Domain Recommendation ----------------
def get_domain_recommendation(skills, interests):
    prompt = f"Suggest the best career domain for someone with skills: {skills} and interests: {interests}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------- Learning Resources ----------------
def get_learning_resources(domain):
    prompt = f"Provide 5 top online learning resources for the career domain: {domain}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    # Parse as list if comma-separated
    resources = []
    for line in response.choices[0].message.content.split("\n"):
        if line.strip():
            parts = line.split("-")
            if len(parts) == 2:
                resources.append({"title": parts[0].strip(), "link": parts[1].strip()})
    return resources

# ---------------- Job Preparation Guide ----------------
def get_job_preparation_guide(job_title):
    prompt = f"Create a step-by-step job preparation guide for the role: {job_title}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------- Skill Gap Analysis ----------------
def get_skill_gap(target_job, current_skills):
    prompt = f"Analyze skill gap for becoming a {target_job}. Current skills: {current_skills}. Suggest missing skills and learning roadmap."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------- Resume Optimizer ----------------
def optimize_resume(job_description, resume_text):
    prompt = f"Optimize this resume text to match the job description.\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content



