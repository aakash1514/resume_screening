from parser import extract_text_from_pdf
from matcher import (
    calculate_dynamic_match,
    extract_project_section,
    calculate_project_relevance,
    extract_experience_requirements,
    extract_candidate_experience,
    apply_experience_penalty,
    calculate_resume_similarity
)
from skill_extracter import (
    load_skills,
    build_matcher,
    extract_skills_hybrid,
)

# File paths
JD_FILE = "data/job_description.txt"
SKILLS_FILE = "data/skills.txt"
RESUME_FILE = "data/resume/resume_aakash.pdf"


def load_job_description():
    with open(JD_FILE, "r", encoding="utf-8") as f:
        return f.read()


def main():

    # ----------------------------
    # Load JD
    # ----------------------------
    jd_text = load_job_description()

    skills_list = load_skills(SKILLS_FILE)
    nlp_matcher = build_matcher(skills_list)

    jd_skills = extract_skills_hybrid(jd_text, nlp_matcher, skills_list)

    print("\n=== Extracted Skills from Job Description ===\n")
    for skill in sorted(jd_skills):
        print(skill)

    # ----------------------------
    # Load Resume
    # ----------------------------
    resume_text = extract_text_from_pdf(RESUME_FILE)

    resume_skills = extract_skills_hybrid(resume_text, nlp_matcher, skills_list)

    print("\n=== Extracted Resume Skills ===\n")
    for skill in sorted(resume_skills):
        print(skill)

    # ----------------------------
    # Skill Match
    # ----------------------------
    result = calculate_dynamic_match(jd_text, jd_skills, resume_skills)

    print("\n=== MATCH RESULTS ===")
    print(f"Skill Match Percentage: {result['match_percentage']}%")

    print("\nMatched Skills:")
    for s in sorted(result["matched_skills"]):
        print(s)

    print("\nMissing Skills:")
    for s in sorted(result["missing_skills"]):
        print(s)

    # ----------------------------
    # Project Relevance
    # ----------------------------
    project_text = extract_project_section(resume_text)
    project_score = calculate_project_relevance(jd_text, project_text)

    print("\nProject Relevance Score:", project_score, "%")

    # ----------------------------
    # Experience Analysis
    # ----------------------------
    jd_experience = extract_experience_requirements(jd_text, set(jd_skills))
    candidate_experience = extract_candidate_experience(resume_text, set(resume_skills))
    
    # Apply experience penalty to skill score (modifier, not separate component)
    adjusted_skill_score = apply_experience_penalty(
        result["match_percentage"],
        jd_experience,
        candidate_experience
    )
    
    print("\nExperience-Adjusted Skill Score:", adjusted_skill_score, "%")

    # ----------------------------
    # Final Combined Score
    # ----------------------------
    resume_similarity_score = calculate_resume_similarity(jd_text, resume_text)

    print("\nFull Resume Semantic Similarity:", resume_similarity_score, "%")
    
    # Experience is already applied to skill score, so final combines:
    # - Adjusted skill score (skill match with experience penalty applied)
    # - Project relevance score
    # - Resume semantic similarity
    final_score = (
        0.6 * adjusted_skill_score +
        0.2 * project_score +
        0.2 * resume_similarity_score
    )

    print("\n=== FINAL SCORE ===")
    print("Overall Candidate Score:", round(final_score, 2), "%")
    print("Overall Candidate Score:", round(final_score, 2), "%")



if __name__ == "__main__":
    main()
