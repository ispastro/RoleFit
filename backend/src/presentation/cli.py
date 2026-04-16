import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.domain.entities.resume import Resume
from src.domain.entities.job import Job
from src.domain.use_cases.tailor_resume import TailorResumeUseCase
from src.infrastructure.ai.job_analyzer import JobAnalyzer
from src.infrastructure.ai.resume_analyzer import ResumeAnalyzer
from src.infrastructure.ai.content_rewriter import ContentRewriter
from src.infrastructure.parsers.latex_parser import LaTeXParser
from src.infrastructure.parsers.latex_generator import LaTeXGenerator

class CLI:
    """Presentation layer - CLI interface"""
    
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.parser = LaTeXParser(resume_path)
    
    def run(self):
        print("=" * 60)
        print("🎯 RoleFit - AI Resume Tailoring Agent")
        print("=" * 60)
        print()
        
        # Get job description
        job_description = self._get_job_description()
        
        if not job_description.strip():
            print("❌ No job description provided. Exiting.")
            return
        
        print()
        print("🚀 Starting AI agent...")
        print()
        
        # Parse resume
        resume_sections = self.parser.get_all_sections()
        resume = Resume.from_sections(resume_sections)
        job = Job(description=job_description)
        
        # Create use case with dependencies
        use_case = TailorResumeUseCase(
            job_analyzer=JobAnalyzer(),
            resume_analyzer=ResumeAnalyzer(),
            content_rewriter=ContentRewriter(),
            latex_generator=LaTeXGenerator(self.resume_path)
        )
        
        # Execute
        output_path = os.path.join("output", "tailored_resume.tex")
        os.makedirs("output", exist_ok=True)
        
        print("🔍 Step 1: Analyzing job description...")
        print("📄 Step 2: Analyzing your resume...")
        print("✍️  Step 3: Tailoring sections...")
        print("📝 Step 4: Generating tailored resume...")
        
        result = use_case.execute(resume, job, output_path)
        
        print()
        print("=" * 60)
        print("🎉 Your tailored resume is ready!")
        print(f"📁 Location: {result}")
        print("=" * 60)
    
    def _get_job_description(self) -> str:
        print("📋 Paste the job description below (press Enter twice when done):")
        print("-" * 60)
        
        lines = []
        empty_count = 0
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        
        return "\n".join(lines)
