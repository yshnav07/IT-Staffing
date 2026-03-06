def match_candidate(cv_data, jd_skills):
    cv_skills = set(cv_data["skills"])
    jd_skills = set(jd_skills)

    matched = cv_skills.intersection(jd_skills)

    score = (len(matched) / len(jd_skills)) * 100

    return {
        "matched_skills": list(matched),
        "score": round(score, 2)
    }