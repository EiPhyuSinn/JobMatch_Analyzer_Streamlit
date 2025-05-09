import streamlit as st
from matcher import matcher

# Optional: extract text from PDF
import PyPDF2

# --- Page config ---
st.set_page_config(page_title="Resume Matcher", layout="centered")

# --- Custom CSS styling ---
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.5rem;
        color: #4a90e2;
        margin-bottom: 1.5rem;
    }
    .stTextArea label, .stFileUploader label {
        font-weight: bold;
        font-size: 1.1rem;
        color: #333;
    }
    .circle-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Header ---
st.markdown("<div class='title'>🎯 Resume vs Job Description Matcher</div>", unsafe_allow_html=True)

# --- Input fields ---
job_desc = st.text_area("💼 Job Description", height=200)
uploaded_file = st.file_uploader("📁 Upload Resume (TXT or PDF)", type=["txt", "pdf"])

resume_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        resume_text = uploaded_file.read().decode("utf-8")

if st.button("🔍 Match Now"):
    if not job_desc or not resume_text:
        st.warning("Please provide both job description and resume.")
    else:
        score = matcher(resume_text, job_desc)
        st.success(f"✅ Match Score: {score}%")

        # Fancy colored circle progress
        st.markdown(f"""
            <div class="circle-container">
                <svg width="180" height="180">
                    <defs>
                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style="stop-color:#00c9ff;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#92fe9d;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <circle cx="90" cy="90" r="75" stroke="#eee" stroke-width="15" fill="none"/>
                    <circle cx="90" cy="90" r="75" stroke="url(#grad)" stroke-width="15" fill="none"
                        stroke-dasharray="{score * 4.71}, 999" transform="rotate(-90 90 90)" />
                    <text x="90" y="100" font-size="26" text-anchor="middle" fill="#333">{score}%</text>
                </svg>
            </div>
        """, unsafe_allow_html=True)
