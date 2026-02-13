from collections import Counter
import re

CORE_TECH = {
    "python", "java", "c", "c++", "r",
    "machine learning", "deep learning",
    "natural language processing",
    "large language models",
    "data science",
    "sql", "postgresql", "mysql",
    "aws", "azure", "gcp"
}

FRAMEWORKS = {
    "tensorflow", "pytorch", "transformers",
    "fastapi", "flask", "django",
    "react", "node.js", "express.js",
    "spring boot"
}

TOOLS = {
    "docker", "kubernetes", "ci/cd",
    "git", "github", "postman",
    "tableau", "power bi",
    "bootstrap", "html", "css"
}


def get_weight(skill: str):

    if skill in CORE_TECH:
        return 3
    elif skill in FRAMEWORKS:
        return 2
    elif skill in TOOLS:
        return 1
    else:
        return 1  # default fallback


def frequency_boost(count):
    return 1 + (0.2 * (count - 1))






def calculate_jd_frequency(jd_text: str, jd_skills: set):
    jd_text = jd_text.lower()
    freq = {}

    for skill in jd_skills:
        # count exact occurrences
        pattern = r'\b' + re.escape(skill) + r'\b'
        count = len(re.findall(pattern, jd_text))
        freq[skill] = count if count > 0 else 1  # minimum 1

    return freq

def extract_experience_requirements(text: str, jd_skills: set):
    """Extract experience requirements for skills from JD text"""
    text = text.lower()
    requirements = {}

    for skill in jd_skills:
        # Pattern like: 3+ years of python
        pattern = rf'(\d+)\+?\s*(?:years|yrs).*?\b{re.escape(skill)}\b'
        match = re.search(pattern, text)

        if match:
            years = int(match.group(1))
            requirements[skill] = years

    return requirements

def extract_candidate_experience(text: str, resume_skills: set):
    """Extract experience for skills from resume text"""
    text = text.lower()
    experience = {}

    for skill in resume_skills:
        pattern = rf'(\d+)\+?\s*(?:years|yrs).*?\b{re.escape(skill)}\b'
        match = re.search(pattern, text)

        if match:
            years = int(match.group(1))
            experience[skill] = years

    return experience

def apply_experience_penalty(match_percentage,
                             jd_requirements,
                             candidate_experience):
    """Apply penalty to match percentage based on experience gaps"""
    penalty = 0

    for skill, required_years in jd_requirements.items():
        candidate_years = candidate_experience.get(skill, 0)

        if candidate_years < required_years:
            penalty += 5  # deduct 5% per unmet requirement

    adjusted_score = max(match_percentage - penalty, 0)

    return adjusted_score

def calculate_dynamic_match(jd_text: str, jd_skills, resume_skills):
    # Convert to sets if they're lists
    jd_skills_set = set(jd_skills) if isinstance(jd_skills, list) else jd_skills
    resume_skills_set = set(resume_skills) if isinstance(resume_skills, list) else resume_skills

    matched = jd_skills_set.intersection(resume_skills_set)
    missing = jd_skills_set.difference(resume_skills_set)

    freq_dict = calculate_jd_frequency(jd_text, jd_skills_set)

    total_weight = 0
    matched_weight = 0

    for skill in jd_skills_set:

        base_weight = get_weight(skill)
        boost = frequency_boost(freq_dict[skill])

        final_weight = base_weight * boost
        total_weight += final_weight

        if skill in matched:
            matched_weight += final_weight

    match_percentage = round((matched_weight / total_weight) * 100, 2) if total_weight > 0 else 0

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing
    }


def extract_project_section(resume_text: str):
    resume_text = resume_text.lower()

    start_keywords = ["projects"]
    end_keywords = ["experience", "education", "skills", "honors"]

    start_index = -1
    for keyword in start_keywords:
        if keyword in resume_text:
            start_index = resume_text.find(keyword)
            break

    if start_index == -1:
        return ""

    end_index = len(resume_text)

    for keyword in end_keywords:
        idx = resume_text.find(keyword, start_index + 8)
        if idx != -1:
            end_index = min(end_index, idx)

    return resume_text[start_index:end_index]

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def calculate_project_relevance(jd_text: str, project_text: str):

    if not project_text.strip():
        return 0

    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    project_embedding = model.encode(project_text, convert_to_tensor=True)

    similarity = util.cos_sim(jd_embedding, project_embedding)

    # Convert tensor to float
    score = float(similarity[0][0])

    # Normalize to 0–100 scale
    relevance_percentage = round(score * 100, 2)

    return relevance_percentage

def calculate_final_score(skill_score, project_score, experience_adjusted_score):
    """
    Calculate final composite score from multiple scoring components.
    
    Weights:
    - 60% skill match score
    - 20% project relevance score
    - 20% experience-adjusted score
    """
    final_score = (
        0.6 * skill_score +
        0.2 * project_score +
        0.2 * experience_adjusted_score
    )
    
    return round(final_score, 2)


def calculate_resume_similarity(jd_text: str, resume_text: str):

    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    similarity = util.cos_sim(jd_embedding, resume_embedding)

    score = float(similarity[0][0])

    # Convert to percentage
    similarity_percentage = round(score * 100, 2)

    return similarity_percentage
