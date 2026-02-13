"""
AI Resume Screening System - Streamlit Application

A web-based interface for evaluating candidate resumes against job descriptions.
"""

import streamlit as st
import tempfile
import os
import sys

# Add src folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core_engine import process_application


# Configure page
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .score-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .matched-skills {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .missing-skills {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 📄 AI Resume Screening System", unsafe_allow_html=True)
st.markdown("---")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This AI-powered system evaluates resumes against job descriptions using:
    
    - **Skill Matching**: Extracts and matches technical skills
    - **Experience Analysis**: Considers years of experience requirements
    - **Project Relevance**: Analyzes project descriptions
    - **Semantic Similarity**: Uses NLP to understand resume-JD alignment
    
    All scores are normalized to 0-100.
    """)
    
    st.markdown("---")
    st.markdown("**Scoring Breakdown:**")
    st.markdown("""
    - 60% Skill Match (with experience penalty)
    - 20% Project Relevance
    - 20% Semantic Similarity
    """)

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Job Description")
    jd_text = st.text_area(
        label="Paste the Job Description here:",
        height=300,
        placeholder="Paste the full job description text...",
        key="jd_input"
    )

with col2:
    st.subheader("📤 Resume Upload")
    uploaded_resume = st.file_uploader(
        label="Upload Candidate Resume (PDF):",
        type="pdf",
        key="resume_upload"
    )
    
    if uploaded_resume is not None:
        st.success(f"✓ File uploaded: {uploaded_resume.name}")

# Evaluation button
st.markdown("---")
col_button = st.columns([1, 4])
with col_button[0]:
    evaluate_button = st.button(
        "🚀 Evaluate Candidate",
        use_container_width=True,
        type="primary"
    )

# Process evaluation
if evaluate_button:
    # Validation
    if not jd_text.strip():
        st.error("❌ Please paste a Job Description")
    elif uploaded_resume is None:
        st.error("❌ Please upload a Resume PDF")
    else:
        # Create temporary file for resume
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(uploaded_resume.read())
            tmp_resume_path = tmp_file.name
        
        try:
            # Show processing message with progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Analyzing resume and job description...")
            progress_bar.progress(25)
            
            # Call core engine
            result = process_application(
                jd_text=jd_text,
                resume_file=tmp_resume_path
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            status_text.empty()
            progress_bar.empty()
            
            # Display results
            st.markdown("---")
            st.markdown("## 📊 Evaluation Results")
            
            # Final Score - Large highlighted display with color coding
            st.markdown("### Overall Score")
            
            final_score = result['final_score']
            
            # Color-code the final score
            if final_score > 75:
                st.success(f"🟢 **STRONG MATCH** - Final Score: {final_score}%")
            elif final_score >= 50:
                st.warning(f"🟡 **MODERATE MATCH** - Final Score: {final_score}%")
            else:
                st.error(f"🔴 **WEAK MATCH** - Final Score: {final_score}%")
            
            # Score metrics
            col_scores = st.columns(4)
            
            with col_scores[0]:
                st.metric(
                    label="Final Score",
                    value=f"{result['final_score']}%",
                    delta=None,
                    label_visibility="visible"
                )
            
            with col_scores[1]:
                st.metric(
                    label="Skill Match",
                    value=f"{result['skill_score']}%"
                )
            
            with col_scores[2]:
                st.metric(
                    label="Project Relevance",
                    value=f"{result['project_score']}%"
                )
            
            with col_scores[3]:
                st.metric(
                    label="Semantic Similarity",
                    value=f"{result['semantic_score']}%"
                )
            
            # Experience adjusted score
            st.markdown("---")
            
            exp_score = result['experience_adjusted_score']
            if exp_score > 75:
                st.success(f"✅ Experience-Adjusted Skill Score: **{exp_score}%**")
            elif exp_score >= 50:
                st.info(f"ℹ️ Experience-Adjusted Skill Score: **{exp_score}%**")
            else:
                st.warning(f"⚠️ Experience-Adjusted Skill Score: **{exp_score}%**")
            
            # Skills Analysis
            st.markdown("---")
            st.markdown("### 🎯 Skills Analysis")
            
            skills_col1, skills_col2 = st.columns(2)
            
            with skills_col1:
                st.markdown("#### ✅ Matched Skills")
                if result['matched_skills']:
                    st.success(f"Found {len(result['matched_skills'])} matching skills")
                    for skill in result['matched_skills']:
                        st.markdown(f"✓ **{skill}**")
                else:
                    st.warning("No matched skills found")
            
            with skills_col2:
                st.markdown("#### ❌ Missing Skills")
                if result['missing_skills']:
                    st.error(f"Missing {len(result['missing_skills'])} required skills")
                    for skill in result['missing_skills']:
                        st.markdown(f"✗ {skill}")
                else:
                    st.success("All required skills present!")
            
            # Detailed Skills Information
            st.markdown("---")
            st.markdown("### 📚 Detailed Skills")
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown("**JD Skills Extracted:**")
                st.write(f"{len(result['jd_skills'])} skills found")
                with st.expander("View all JD skills"):
                    for skill in result['jd_skills']:
                        st.text(skill)
            
            with detail_col2:
                st.markdown("**Resume Skills Extracted:**")
                st.write(f"{len(result['resume_skills'])} skills found")
                with st.expander("View all resume skills"):
                    for skill in result['resume_skills']:
                        st.text(skill)
            
            # Recommendation
            st.markdown("---")
            st.markdown("### 💡 Recommendation")
            
            if final_score > 75:
                st.success(f"""
                🟢 **STRONG MATCH - Highly Recommended**
                
                Score: **{final_score}%**
                
                This candidate is an excellent fit for the position. 
                Recommend proceeding to interview.
                """)
            elif final_score >= 50:
                st.warning(f"""
                🟡 **MODERATE MATCH - Consider for Review**
                
                Score: **{final_score}%**
                
                This candidate has potential but may have some skill gaps.
                Consider for further evaluation.
                """)
            else:
                st.error(f"""
                🔴 **WEAK MATCH - Not Recommended**
                
                Score: **{final_score}%**
                
                This candidate does not meet the minimum requirements.
                Consider other applicants.
                """)
        
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
            st.info("Please check that:")
            st.markdown("- The resume is a valid PDF file")
            st.markdown("- The job description is properly formatted")
            st.markdown("- All required models are loaded")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_resume_path):
                os.remove(tmp_resume_path)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    AI Resume Screening System | Powered by NLP & Machine Learning
</div>
""", unsafe_allow_html=True)
