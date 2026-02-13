import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import extract_text_from_pdf


class TestParser:
    """Test cases for parser module"""

    def test_extract_text_from_pdf_returns_string(self):
        """Test that extract_text_from_pdf returns a string"""
        result = extract_text_from_pdf("data/resume/resume_aakash.pdf")
        assert isinstance(result, str)

    def test_extract_text_from_pdf_not_empty(self):
        """Test that extracted text is not empty"""
        result = extract_text_from_pdf("data/resume/resume_aakash.pdf")
        assert len(result) > 0

    def test_extract_text_from_pdf_lowercased(self):
        """Test that extracted text is lowercased"""
        result = extract_text_from_pdf("data/resume/resume_aakash.pdf")
        assert result == result.lower()

    def test_extract_text_from_pdf_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file"""
        with pytest.raises(Exception):  # PyMuPDF raises FileNotFoundError
            extract_text_from_pdf("data/resume/nonexistent.pdf")
