import streamlit as st
import pdfplumber
import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Extract Text
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text


# -----------------------------
# Skill Extraction
# -----------------------------
def extract_skills(text, skill_list):
    found_skills = []
    for skill in skill_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills


# -----------------------------
# Experience Extraction
# -----------------------------
def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    if matches:
        return max([int(m[0]) for m in matches])
    return 0


# -----------------------------
# Weighted Scoring
# -----------------------------
def weighted_score(resume_skills, jd_weights):
    score = 0
    total_weight = sum(jd_weights.values())
    
    for skill, weight in jd_weights.items():
        if skill in resume_skills:
            score += weight
            
    return round((score / total_weight) * 100, 2)


# -----------------------------
# Semantic Similarity
# -----------------------------
def semantic_score(resume_text, jd_text):
    jd_embedding = model.encode([jd_text])
    resume_embedding = model.encode([resume_text])
    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]
    return round(similarity * 100, 2)


# -----------------------------
# UI
# -----------------------------
st.title("Advanced AI Resume Matching System")

jd_text = st.text_area("Enter Job Description")

uploaded_files = st.file_uploader("Upload Multiple Resumes", type=["pdf"], accept_multiple_files=True)

# Skill Dictionary
skill_list = [
    "Python", "SQL", "Machine Learning", "NLP",
    "Django", "Java", "MySQL", "Pandas",
    "TensorFlow", "Power BI", "Data Science"
]

if st.button("Analyze Resumes"):

    if jd_text and uploaded_files:

        results = []

        # Extract JD Skills
        jd_skills = extract_skills(jd_text, skill_list)

        # Assign weights automatically
        jd_weights = {skill: 1 for skill in jd_skills}

        for file in uploaded_files:

            resume_text = extract_text_from_pdf(file)

            resume_skills = extract_skills(resume_text, skill_list)

            exp_years = extract_experience(resume_text)

            skill_score = weighted_score(resume_skills, jd_weights)

            semantic_similarity = semantic_score(resume_text, jd_text)

            final_score = round((skill_score * 0.6) + (semantic_similarity * 0.4), 2)

            results.append({
                "Candidate": file.name,
                "Skill Score (%)": skill_score,
                "Semantic Match (%)": semantic_similarity,
                "Experience (Years)": exp_years,
                "Final Score (%)": final_score
            })

        df = pd.DataFrame(results)
        df = df.sort_values(by="Final Score (%)", ascending=False)

        st.success("Ranking Completed")
        st.dataframe(df)

        st.bar_chart(df.set_index("Candidate")["Final Score (%)"])

    else:
        st.warning("Please enter JD and upload resumes.")