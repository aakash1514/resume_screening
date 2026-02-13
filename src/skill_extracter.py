import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer, util
from typing import List
import torch

# Load models once
nlp = spacy.load("en_core_web_sm")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Generic non-technical terms to filter out
GENERIC_TERMS = {
    "oop",
    "object oriented programming",
    "programming",
    "software development",
    "problem solving",
    "communication",
    "teamwork",
    "collaboration",
    "leadership",
    "management",
    "development",
    "coding",
    "software",
    "application",
    "system",
    "data structures",
    "algorithms",
    "version control",
    "agile",
}


# -----------------------------
# Load predefined skill list
# -----------------------------
def load_skills(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        skills = []
        for line in f:
            skill = line.strip().lower()
            if not skill:
                continue
            # Remove extremely short skills unless explicitly allowed
            if len(skill) <= 2 and skill not in ["c", "r"]:
                continue
            # Filter out generic non-technical terms
            if skill in GENERIC_TERMS:
                continue
            skills.append(skill)
    return skills


# -----------------------------
# Build PhraseMatcher
# -----------------------------
def build_matcher(skills_list: List[str]) -> PhraseMatcher:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skills_list]
    matcher.add("SKILLS", patterns)
    return matcher


# -----------------------------
# Extract known skills
# -----------------------------
def extract_known_skills(text: str, matcher: PhraseMatcher) -> List[str]:
    doc = nlp(text.lower())
    matches = matcher(doc)

    found = set()
    for _, start, end in matches:
        found.add(doc[start:end].text.lower())

    return list(found)


# -----------------------------
# Extract candidate noun phrases
# -----------------------------
def extract_candidate_phrases(text: str) -> List[str]:
    doc = nlp(text.lower())
    phrases = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()

        # Remove long noisy phrases
        if len(phrase.split()) > 4:
            continue

        # Remove phrases containing common non-skill words
        blacklist = ["experience", "knowledge", "candidate", "plus", "required", "preferred"]

        if any(word in phrase for word in blacklist):
            continue

        phrases.add(phrase)

    return list(phrases)


# -----------------------------
# Clean and normalize phrases
# -----------------------------
def clean_phrase(phrase: str) -> str:
    phrase = phrase.lower()

    # Remove common trailing words
    phrase = phrase.replace("pipelines", "")
    phrase = phrase.replace("frameworks", "")
    phrase = phrase.replace("databases", "")
    phrase = phrase.replace("building", "")
    
    # Handle plural
    if phrase.endswith("apis"):
        phrase = phrase.replace("apis", "api")

    return phrase.strip()


# -----------------------------
# Extract known skills from phrase
# -----------------------------
def extract_known_skills_from_phrase(phrase: str, known_skills: List[str]):
    found = []
    for skill in known_skills:
        if skill in phrase:
            found.append(skill)
    return found


# -----------------------------
# Filter skill-like phrases using semantic similarity
# -----------------------------
def filter_skill_like_phrases(
    candidate_phrases: List[str],
    known_skills: List[str],
    threshold: float = 0.65,
) -> List[str]:

    if not candidate_phrases:
        return []

    skill_embeddings = embedding_model.encode(known_skills, convert_to_tensor=True)
    phrase_embeddings = embedding_model.encode(candidate_phrases, convert_to_tensor=True)

    discovered = set()

    for i, phrase_embedding in enumerate(phrase_embeddings):
        similarities = util.cos_sim(phrase_embedding, skill_embeddings)
        max_score = torch.max(similarities).item()

        if max_score > threshold:
            cleaned = clean_phrase(candidate_phrases[i])
            matches = extract_known_skills_from_phrase(cleaned, known_skills)
            
            if matches:
                for m in matches:
                    discovered.add(m)


    return list(discovered)


# -----------------------------
# Final Hybrid Extraction
# -----------------------------
def extract_skills_hybrid(text: str, matcher: PhraseMatcher, skills_list: List[str]) -> List[str]:
    """
    Extract skills using hybrid approach and apply normalization/filtering.
    
    Steps:
    1. Extract known skills using matcher
    2. Extract candidate phrases
    3. Discover new skills via semantic similarity
    4. Normalize all skills (lowercase, strip whitespace)
    5. Remove duplicates
    6. Filter out generic terms
    
    Returns:
        List of normalized, filtered skills
    """
    known = extract_known_skills(text, matcher)
    candidates = extract_candidate_phrases(text)
    discovered = filter_skill_like_phrases(candidates, skills_list)

    # Combine all skills
    all_skills = known + discovered
    
    # Normalize and deduplicate
    normalized_skills = set()
    for skill in all_skills:
        # Normalize: lowercase and strip whitespace
        normalized_skill = skill.lower().strip()
        
        # Filter out generic terms (case-insensitive)
        if normalized_skill not in GENERIC_TERMS:
            normalized_skills.add(normalized_skill)
    
    # Return as sorted list for consistency
    return sorted(list(normalized_skills))
