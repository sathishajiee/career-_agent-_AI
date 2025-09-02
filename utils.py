import os, json, tempfile
from groq import Groq
from dotenv import load_dotenv
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# 🔹 Load environment variables from .env (local dev)
load_dotenv()

# 🔹 Get API key (works for both local & Streamlit Cloud)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ Missing GROQ_API_KEY. Please set it in .env (local) or in Streamlit Secrets (cloud).")

# 🔹 Initialize Groq client
client = Groq(api_key=api_key)

# ✅ Career Suggestions
def get_career_suggestions(job_title):
    prompt = f"Suggest key skills, learning roadmap and interview preparation steps for a {job_title}."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ✅ Resume Optimization
def optimize_resume(job_description, resume_text):
    prompt = f"Optimize the following resume for this job description:\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

# ✅ Domain Recommendation
def get_domain_recommendation(skills, interests):
    prompt = f"Based on these skills: {skills} and interests: {interests}, suggest the best career domain. Give only the domain name."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ✅ Learning Resources
def get_learning_resources(domain):
    prompt = f"Suggest 5 best YouTube or Coursera resources for mastering {domain}. Provide output in JSON like: [{{'title':'Course','link':'https://...'}}]"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    try:
        resources = json.loads(content)
        # ✅ Ensure all links are valid clickable URLs
        for r in resources:
            if not r.get("link", "").startswith("http"):
                query = r['title'].replace(" ", "+")
                r["link"] = f"https://www.youtube.com/results?search_query={query}"
        return resources

    except:
        # ✅ Fallback: split lines and convert into clickable YouTube links
        resources = []
        for line in content.split("\n"):
            if line.strip():
                query = line.strip().replace(" ", "+")
                resources.append({
                    "title": line.strip(),
                    "link": f"https://www.youtube.com/results?search_query={query}"
                })
        return resources

# ✅ Job Preparation Guide
def get_job_preparation_guide(job_title):
    prompt = f"Create a preparation guide for {job_title} including skills, roadmap, interview tips, and projects."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ✅ Skill Gap Analysis
def get_skill_gap(job_title, current_skills):
    prompt = f"""
    Job Title: {job_title}
    Current Skills: {current_skills}

    1️⃣ List essential skills required for this job.
    2️⃣ Compare with current skills.
    3️⃣ Show missing skills.
    4️⃣ Give a step-by-step learning roadmap to cover missing skills.
    Output in clean bullet points.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ✅ Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    file_bytes = uploaded_file.read()
    if not file_bytes or len(file_bytes) == 0:
        return "⚠️ Error: Empty PDF file uploaded or could not read file."

    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text if text.strip() else "⚠️ No text found in PDF."

# ✅ Generate Optimized Resume PDF
def create_resume_pdf(optimized_text):
    pdf_path = "optimized_resume.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width/2, height-80, "ATS-Friendly Resume")

    # Body Content
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)

    # Split content into lines
    y = height - 120
    for line in optimized_text.split("\n"):
        if y < 50:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 11)
        c.drawString(60, y, line.strip())
        y -= 15

    c.save()
    return pdf_path

# ✅ Generate ATS Resume Template
def generate_ats_resume(data, output_file="ATS_Resume.pdf"):
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, data.get("name", "Your Name"))

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Email: {data.get('email', 'your@email.com')}")
    c.drawString(100, 705, f"Phone: {data.get('phone', '+91 XXXXX XXXXX')}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 670, "Summary")
    c.setFont("Helvetica", 12)
    c.drawString(100, 655, data.get("summary", "Add a professional summary."))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 620, "Skills")
    y = 605
    for skill in data.get("skills", []):
        c.drawString(100, y, f"- {skill}")
        y -= 15

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y-20, "Projects")
    y -= 35
    for project in data.get("projects", []):
        c.drawString(100, y, f"- {project}")
        y -= 15

    c.save()
    return output_file

# ✅ Generate Modern CV Template
def generate_modern_cv(data, output_file="Modern_CV.pdf"):
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, 750, data.get("name", "Your Name"))

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Email: {data.get('email', 'your@email.com')}")
    c.drawString(50, 705, f"Phone: {data.get('phone', '+91 XXXXX XXXXX')}")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 670, "Skills")
    y = 655
    for skill in data.get("skills", []):
        c.drawString(50, y, f"• {skill}")
        y -= 15

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y-20, "Projects")
    y -= 35
    for project in data.get("projects", []):
        c.drawString(50, y, f"• {project}")
        y -= 15

    c.save()
    return output_file
