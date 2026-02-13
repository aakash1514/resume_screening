# AI Resume Screening System

An intelligent, NLP-powered Applicant Tracking System (ATS) that automatically screens resumes against job descriptions using machine learning and semantic analysis.

## 🎯 Features

- **Intelligent Skill Matching**: Extracts and matches technical skills from resumes and job descriptions
- **Experience-Aware Scoring**: Considers years of experience requirements and penalties for gaps
- **Semantic Analysis**: Uses transformer models to understand resume-JD alignment beyond keyword matching
- **Project Relevance Scoring**: Analyzes project descriptions for relevance to the role
- **Weighted Scoring System**: Combines multiple factors (50% skills, 20% projects, 30% semantics)
- **Interactive Web UI**: Professional Streamlit interface for easy resume evaluation
- **PDF Support**: Directly processes PDF resumes using PyMuPDF
- **Comprehensive Results**: Detailed breakdown of matched/missing skills and scoring components

## 📊 Scoring Breakdown

- **50%** - Experience-Adjusted Skill Match (with experience penalty for gaps)
- **20%** - Project Relevance Score
- **30%** - Full Resume Semantic Similarity

Final Score: **0-100** with color-coded recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/resume-screening-nlp.git
cd resume-screening-nlp
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

5. **Run the Streamlit app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
resume-screening-nlp/
├── app.py                          # Streamlit web application
├── conftest.py                     # Pytest configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── src/
│   ├── core_engine.py             # Main orchestration engine
│   ├── parser.py                  # PDF text extraction
│   ├── skill_extracter.py         # Skill extraction & filtering
│   ├── matcher.py                 # Skill matching & scoring
│   └── main.py                    # Command-line interface
│
├── data/
│   ├── job_description.txt        # Sample job description
│   ├── skills.txt                 # Predefined skills list
│   └── resume/                    # Resume storage directory
│
└── tests/
    ├── test_parser.py             # Parser unit tests
    └── test_skill_extracter.py    # Skill extraction tests
```

## 🔧 Usage

### Web Interface (Recommended)

1. Start the Streamlit app: `streamlit run app.py`
2. Paste the job description in the left panel
3. Upload a PDF resume
4. Click "Evaluate Candidate"
5. View comprehensive scoring and recommendations

### Command Line

```python
from src.core_engine import process_application

# Process a resume
jd_text = open("data/job_description.txt").read()
result = process_application(
    jd_text=jd_text,
    resume_file="data/resume/resume.pdf"
)

# Access results
print(f"Final Score: {result['final_score']}%")
print(f"Matched Skills: {result['matched_skills']}")
print(f"Missing Skills: {result['missing_skills']}")
```

## 📊 API Reference

### `process_application(jd_text, resume_file, skills_file)`

Main function for resume screening.

**Parameters:**
- `jd_text` (str): Job description text
- `resume_file` (str): Path to PDF resume file
- `skills_file` (str): Path to skills list file (default: "data/skills.txt")

**Returns:**
```python
{
    "final_score": float,                    # 0-100
    "skill_score": float,                    # Weighted skill match
    "experience_adjusted_score": float,      # After experience penalty
    "project_score": float,                  # Project relevance
    "semantic_score": float,                 # Semantic similarity
    "matched_skills": list,                  # Skills found in both
    "missing_skills": list,                  # Required but missing
    "jd_skills": list,                       # All JD skills
    "resume_skills": list                    # All resume skills
}
```

## 🎓 How It Works

### 1. Skill Extraction
- Uses spaCy NLP for entity recognition
- PhraseMatcher for known skill detection
- Semantic similarity for skill discovery

### 2. Experience Analysis
- Regex patterns to extract "X years of skill" requirements
- Penalty system (5% per unmet requirement)
- Adjusts skill score based on experience gaps

### 3. Semantic Matching
- Sentence Transformers for deep semantic understanding
- Calculates resume-JD similarity using cosine distance
- Identifies semantic alignment beyond keywords

### 4. Project Relevance
- Extracts project section from resume
- Measures project-JD semantic similarity
- Scores based on relevance of candidate projects

### 5. Final Scoring
- Combines all components with weighted formula
- Normalizes to 0-100 scale
- Provides color-coded recommendations

## 🧪 Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src
```

## 📦 Dependencies

Key packages:
- **PyMuPDF** - PDF text extraction
- **spaCy** - NLP & entity recognition
- **sentence-transformers** - Semantic similarity
- **scikit-learn** - ML utilities
- **Streamlit** - Web UI framework
- **pandas, numpy** - Data processing
- **regex** - Advanced pattern matching
- **torch** - Deep learning backend

See `requirements.txt` for complete list with versions.

## ⚙️ Configuration

### Customize Skills List

Edit `data/skills.txt` to add/remove skills:
```
python
java
machine learning
aws
docker
...
```

### Adjust Scoring Weights

In `src/core_engine.py`, modify the final_score calculation:
```python
final_score = (
    0.5 * experience_adjusted_score +   # Skill weight
    0.2 * project_score +               # Project weight
    0.3 * semantic_score                # Semantic weight
)
```

### Filter Generic Terms

Edit `GENERIC_TERMS` in `src/skill_extracter.py` to exclude vague skills:
```python
GENERIC_TERMS = {
    "programming",
    "software development",
    "problem solving",
    ...
}
```

## 🔐 Privacy & Security

- ✅ No permanent storage of uploaded resumes
- ✅ Temporary files cleaned immediately after processing
- ✅ No external API calls for data
- ✅ All processing done locally

## 🚧 Future Enhancements

- [ ] Batch resume processing
- [ ] Database integration for resume history
- [ ] Custom scoring profiles per role
- [ ] Multi-language support
- [ ] Resume recommendations
- [ ] Integration with HRIS systems
- [ ] Advanced analytics dashboard

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact & Support

For questions or issues, please create a GitHub issue or contact the maintainer.

---

**Built with ❤️ for smarter hiring**
