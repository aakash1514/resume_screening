import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skill_extracter import load_skills, build_matcher, extract_known_skills


class TestSkillExtractor:
    """Test cases for skill_extracter module"""

    @pytest.fixture
    def skills_list(self):
        """Load skills for testing"""
        return load_skills("data/skills.txt")

    @pytest.fixture
    def matcher(self, skills_list):
        """Build matcher for testing"""
        return build_matcher(skills_list)

    def test_load_skills_returns_list(self):
        """Test that load_skills returns a list"""
        skills = load_skills("data/skills.txt")
        assert isinstance(skills, list)

    def test_load_skills_not_empty(self):
        """Test that skills list is not empty"""
        skills = load_skills("data/skills.txt")
        assert len(skills) > 0

    def test_load_skills_all_lowercase(self):
        """Test that all skills are lowercase"""
        skills = load_skills("data/skills.txt")
        for skill in skills:
            assert skill == skill.lower()

    def test_load_skills_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file"""
        with pytest.raises(FileNotFoundError):
            load_skills("data/nonexistent.txt")

    def test_build_matcher_returns_matcher(self, skills_list):
        """Test that build_matcher returns a PhraseMatcher"""
        matcher = build_matcher(skills_list)
        assert matcher is not None

    def test_extract_known_skills_returns_list(self, matcher):
        """Test that extract_known_skills returns a list"""
        text = "I know python, java, and sql"
        result = extract_known_skills(text, matcher)
        assert isinstance(result, list)

    def test_extract_known_skills_finds_skills(self, skills_list, matcher):
        """Test that extract_known_skills finds known skills"""
        text = "I am experienced in python and java development"
        result = extract_known_skills(text, matcher)
        assert len(result) > 0
