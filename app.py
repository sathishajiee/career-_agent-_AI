import streamlit as st
from utils import (
    extract_text_from_pdf, create_resume_pdf,
    get_domain_recommendation, get_learning_resources,
    get_job_preparation_guide, get_skill_gap, optimize_resume
)

# ----------------- Page Config & Styles -----------------
st.set_page_config(page_title="Career AI Agent", layout="wide")

st.image(
    "https://raw.githubusercontent.com/your-username/your-repo/main/assets/bg.png",
    use_container_width=True
)

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f5;
    }
    h1, h2, h3, h4 {
        color: darkblue !important;
        font-weight: bold;
    }
    label[data-testid="stWidgetLabel"] {
        color: #222222 !important;
        font-weight: bold;
    }
    .section-card {
        padding: 20px;
        border-radius: 12px;
        margin: 15px auto;
        width: 85%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    [data-testid="stSidebar"] {
        background-color: skyblue;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Sidebar Navigation -----------------
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📌 Career Tools", "📄 Resume Optimizer", "ℹ️ About"]
)

st.write(f"### Selected Page: {page}")

# ----------------- Home -----------------
if page == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🎯 Career AI Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>AI-powered Career Guidance, Resume Optimizer & Skill Gap Analyzer</p>", unsafe_allow_html=True)

# ----------------- Career Tools -----------------
elif page == "📌 Career Tools":
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

    st.header("Step 2: Job Preparation")
    job_title = st.text_input("Enter job title:", placeholder="Data Analyst")
    if st.button("Generate Job Prep Guide"):
        if job_title:
            guide = get_job_preparation_guide(job_title)
            st.subheader(f"📌 {job_title} Preparation Guide")
            st.write(guide)

    st.header("Step 3: Skill Gap Analysis")
    target_job = st.text_input("Target job:", placeholder="Data Scientist")
    current_skills = st.text_input("Your current skills:", placeholder="Python, SQL, Excel")
    if st.button("Analyze Skill Gap"):
        if target_job and current_skills:
            gap_report = get_skill_gap(target_job, current_skills)
            st.subheader("📌 Skill Gap Report")
            st.write(gap_report)

# ----------------- Resume Optimizer -----------------
elif page == "📄 Resume Optimizer":
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

# ----------------- About -----------------
elif page == "ℹ️ About":
    st.header("ℹ️ About Career AI Agent")
    st.write("""
✅ AI-powered Career Recommendations – Personalized job & career suggestions.
✅ Skill Gap Analysis – Identify missing skills & learning roadmap.
✅ ATS Resume Optimizer – Create professional resumes matching job descriptions.
✅ Job Market Insights – Trending roles & skills.
✅ Interview Preparation Assistance – AI-generated mock questions & tips.
✅ Portfolio & Project Guidance – Showcase skills effectively.
    """)






