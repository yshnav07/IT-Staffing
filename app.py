import pdfplumber
import re

# ----------------------------
# Step 1: Extract Resume Text
# ----------------------------

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text


# ----------------------------
# Step 2: Extract Skills from Text
# ----------------------------

def extract_skills(text, skill_list):
    found_skills = []

    for skill in skill_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# ----------------------------
# Step 3: Score Resume
# ----------------------------

def score_resume(resume_skills, jd_skills):
    matched = set(resume_skills).intersection(set(jd_skills))
    score = (len(matched) / len(jd_skills)) * 100
    return matched, round(score, 2)


# ----------------------------
# MAIN EXECUTION
# ----------------------------

# Example JD
jd_text = """
We are looking for a Data Scientist with skills in Python, SQL, Machine Learning, NLP, and Django.
"""

# Define skill dictionary (can expand later)
skill_list = [
    "Python", "SQL", "Machine Learning", "NLP",
    "Django", "Java", "MySQL", "Pandas",
    "TensorFlow", "Power BI"
]

# Extract JD Skills
jd_skills = extract_skills(jd_text, skill_list)

# Extract Resume Text
resume_text = extract_text_from_pdf("C:/Users/vaish/Downloads/Farsana Resume.pdf")

# Extract Resume Skills
resume_skills = extract_skills(resume_text, skill_list)

# Score Resume
matched_skills, score = score_resume(resume_skills, jd_skills)

print("\nJD Skills:", jd_skills)
print("Resume Skills:", resume_skills)
print("Matched Skills:", matched_skills)
print("Resume Score:", score, "%")