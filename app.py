import streamlit as st
import base64
from utils import (
    extract_text_from_pdf, create_resume_pdf,
    get_domain_recommendation, get_learning_resources,
    get_job_preparation_guide, get_skill_gap, optimize_resume
)
# Display header/banner image
st.image(
    "https://raw.githubusercontent.com/your-username/your-repo/main/assets/bg.png",
    use_container_width=True
)


# App title
st.title("🚀 Career Agent AI")


# ✅ Page Config
st.set_page_config(page_title="Career AI Agent", layout="wide")

# ✅ Background Image Setup
def get_base64_of_image(image_file):
    with open(image_file, "rb") as img:
        return base64.b64encode(img.read()).decode()

image_path = r"C:\Users\Yashvanth\OneDrive\Pictures\AI-in-Career-Counseling_2.jpg"
base64_image = get_base64_of_image(image_path)

# ✅ Global CSS Styling
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: #f0f2f5; /* Light grey background */
        background-size: cover;
        background-position: center;
    }}
    h1, h2, h3, h4 {{
        color: dark blue !important;   /* Dark blure for All Headers */
        font-weight: bold;
    }}
    label[data-testid="stWidgetLabel"] {{
        color: #222222 !important;   /* Dark Grey Input Labels */
        font-weight: bold;
    }}
    .section-card {{
        background-image: url(https://irp.cdn-website.com/47428ebb/dms3rep/multi/The+Benefits+of+Glutathione+IV+Therapy-+A+Comprehensive+Guide.png);
        padding: 20px;
        border-radius: 12px;
        margin: 15px auto;
        width: 85%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# ✅ Sidebar Navigation
import streamlit as st

# --- Sidebar Background Image ---
sidebar_bg = """
    <style>
    [data-testid="stSidebar"] {
        background-color: skyblue; /* Fallback color */
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    </style>
"""
st.markdown(sidebar_bg, unsafe_allow_html=True)

# --- Sidebar Navigation ---
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📌 Career Tools", "📄 Resume Optimizer", "ℹ️ About"]
)

st.write(f"### Selected Page: {page}")


# ----------------- 🏠 Landing Page -----------------
if page == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🎯 Career AI Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>AI-powered Career Guidance, Resume Optimizer & Skill Gap Analyzer</p>", unsafe_allow_html=True)

# ----------------- 📌 Career Tools -----------------
elif page == "📌 Career Tools":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("Step 1: Domain Recommendation")
    skills = st.text_input("Enter your skills:", placeholder="Python, SQL, Communication")
    interests = st.text_input("Enter your interests:", placeholder="Data Science, Web Development")

    if st.button("Get Domain Recommendation"):
        if skills and interests:
            domain = get_domain_recommendation(skills, interests)
            st.success(f"✅ Recommended Domain: **{domain}**")
            resources = get_learning_resources(domain)
            st.subheader("📚 Recommended Learning Resources")
            for r in resources:
                st.markdown(f"🔗 **[{r.get('title','Resource')}]({r.get('link','#')})**")
    st.markdown('</div>', unsafe_allow_html=True)

    # Step 2: Job Preparation
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("Step 2: Job Preparation")
    job_title = st.text_input("Enter job title:", placeholder="Data Analyst")
    if st.button("Generate Job Prep Guide"):
        if job_title:
            guide = get_job_preparation_guide(job_title)
            st.subheader(f"📌 {job_title} Preparation Guide")
            st.write(guide)
    st.markdown('</div>', unsafe_allow_html=True)

    # Step 3: Skill Gap
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("Step 3: Skill Gap Analysis")
    target_job = st.text_input("Target job:", placeholder="Data Scientist")
    current_skills = st.text_input("Your current skills:", placeholder="Python, SQL, Excel")
    if st.button("Analyze Skill Gap"):
        if target_job and current_skills:
            gap_report = get_skill_gap(target_job, current_skills)
            st.subheader("📌 Skill Gap Report")
            st.write(gap_report)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- 📄 Resume Optimizer -----------------
elif page == "📄 Resume Optimizer":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("📄 Resume Optimizer")

    uploaded_resume = st.file_uploader("Upload Resume (PDF):", type=["pdf"])
    job_description = st.text_area("Paste Job Description:")

    if st.button("Optimize Resume"):
        if uploaded_resume and job_description:
            resume_text = extract_text_from_pdf(uploaded_resume)
            optimized = optimize_resume(job_description, resume_text)
            st.subheader("✅ Optimized ATS Resume")
            st.text_area("Preview", optimized, height=350)
            pdf_file = create_resume_pdf(optimized)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇ Download Optimized Resume (PDF)", f, file_name="optimized_resume.pdf")
        else:
            st.warning("⚠️ Please upload resume & job description.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- ℹ️ About -----------------
elif page == "ℹ️ About":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.header("ℹ️ About Career AI Agent")
    st.write("""
    ✅ AI-powered Career Recommendations – Get personalized job and career suggestions based on your skills, interests, and career goals. The AI analyzes your profile to suggest roles that fit you best and guide you towards long-term success.

✅ Smart Skill Gap Analysis & Learning Resources – Identify exactly which skills you need for your dream job. The platform provides curated online courses, tutorials, and certifications to help you bridge gaps and stay industry-ready.

✅ ATS-friendly Resume Builder – Instantly generate professional, ATS-optimized resumes designed to pass applicant tracking systems. Customize your resume to match job descriptions and stand out to recruiters.

✅ Real-time Job Market Insights – Get updates on trending job roles, in-demand skills, and hiring patterns to make informed career decisions. Stay ahead of the competition with data-driven insights.

✅ Personalized Career Growth Roadmap – Receive a clear step-by-step plan to achieve your career goals, including skill upgrades, project recommendations, and job application strategies.

✅ Interview Preparation Assistance – Access AI-generated mock interview questions, answers, and tips based on your desired role to boost your confidence and performance.

✅ Portfolio & Project Guidance – Learn how to create a strong portfolio with relevant projects, case studies, and achievements to showcase your skills effectively.

✅ Continuous Career Support – The platform evolves with your progress, offering updated recommendations, new skill paths, and job suggestions as you grow in your career.

    """)
    st.markdown('</div>', unsafe_allow_html=True)


