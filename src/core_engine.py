"""
Core Resume Screening Engine

Orchestrates the entire resume screening workflow.
"""

from parser import extract_text_from_pdf
from skill_extracter import (
    load_skills,
    build_matcher,
    extract_skills_hybrid,
)
from matcher import (
    calculate_dynamic_match,
    extract_experience_requirements,
    extract_candidate_experience,
    apply_experience_penalty,
    extract_project_section,
    calculate_project_relevance,
    calculate_resume_similarity,
)


def process_application(jd_text: str, resume_file: str, skills_file: str = "data/skills.txt") -> dict:
    """
    Process a resume against a job description and return comprehensive scoring.
    
    Args:
        jd_text (str): Full text of the job description
        resume_file (str): Path to the resume PDF file
        skills_file (str): Path to the skills list file (default: data/skills.txt)
    
    Returns:
        dict: Contains:
            - final_score: Overall combined score (0-100)
            - skill_score: Weighted skill match score
            - experience_adjusted_score: Skill score after experience penalty
            - project_score: Project relevance score
            - semantic_score: Full resume semantic similarity score
            - matched_skills: Set of skills found in both JD and resume
            - missing_skills: Set of skills required but not in resume
            - jd_skills: All skills extracted from JD
            - resume_skills: All skills extracted from resume
    """
    
    # ----------------------------
    # Load Skills List
    # ----------------------------
    skills_list = load_skills(skills_file)
    nlp_matcher = build_matcher(skills_list)
    
    # ----------------------------
    # Extract JD Skills
    # ----------------------------
    jd_skills = extract_skills_hybrid(jd_text, nlp_matcher, skills_list)
    
    # ----------------------------
    # Extract Resume Text and Skills
    # ----------------------------
    resume_text = extract_text_from_pdf(resume_file)
    resume_skills = extract_skills_hybrid(resume_text, nlp_matcher, skills_list)
    
    # ----------------------------
    # Calculate Weighted Skill Match
    # ----------------------------
    skill_match_result = calculate_dynamic_match(jd_text, jd_skills, resume_skills)
    skill_score = skill_match_result["match_percentage"]
    matched_skills = skill_match_result["matched_skills"]
    missing_skills = skill_match_result["missing_skills"]
    
    # ----------------------------
    # Apply Experience Penalty
    # ----------------------------
    jd_experience = extract_experience_requirements(jd_text, set(jd_skills))
    candidate_experience = extract_candidate_experience(resume_text, set(resume_skills))
    
    experience_adjusted_score = apply_experience_penalty(
        skill_score,
        jd_experience,
        candidate_experience
    )
    
    # ----------------------------
    # Calculate Project Relevance
    # ----------------------------
    project_text = extract_project_section(resume_text)
    project_score = calculate_project_relevance(jd_text, project_text)
    
    # ----------------------------
    # Calculate Semantic Similarity
    # ----------------------------
    semantic_score = calculate_resume_similarity(jd_text, resume_text)
    
    # ----------------------------
    # Compute Final Score
    # ----------------------------
    final_score = (
        0.5 * experience_adjusted_score +
        0.2 * project_score +
        0.3 * semantic_score
    )
    
    # Ensure score is between 0-100
    final_score = min(100, max(0, round(final_score, 2)))
    
    # ----------------------------
    # Return Results
    # ----------------------------
    return {
        "final_score": final_score,
        "skill_score": round(skill_score, 2),
        "experience_adjusted_score": round(experience_adjusted_score, 2),
        "project_score": round(project_score, 2),
        "semantic_score": round(semantic_score, 2),
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "jd_skills": sorted(jd_skills),
        "resume_skills": sorted(resume_skills),
    }
