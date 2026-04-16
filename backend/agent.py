from backend.latex_parser import LaTeXParser
from backend.job_analyzer import JobAnalyzer
from backend.resume_analyzer import ResumeAnalyzer
from backend.content_rewriter import ContentRewriter
from backend.latex_generator import LaTeXGenerator

class RoleFitAgent:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.parser = LaTeXParser(resume_path)
        self.job_analyzer = JobAnalyzer()
        self.resume_analyzer = ResumeAnalyzer()
        self.rewriter = ContentRewriter()
    
    def tailor_resume(self, job_description, output_path):
        """Main agent workflow: analyze job, analyze resume, rewrite sections, generate output"""
        
        print("🔍 Step 1: Analyzing job description...")
        job_analysis = self.job_analyzer.analyze(job_description)
        
        print("📄 Step 2: Analyzing your resume...")
        resume_sections = self.parser.get_all_sections()
        resume_analysis = self.resume_analyzer.analyze(resume_sections)
        
        print("✍️  Step 3: Tailoring EXPERIENCE section...")
        new_experience = self.rewriter.rewrite_section(
            resume_sections['experience'],
            job_analysis,
            resume_analysis,
            "EXPERIENCE"
        )
        
        print("✍️  Step 4: Tailoring PROJECTS section...")
        new_projects = self.rewriter.rewrite_section(
            resume_sections['projects'],
            job_analysis,
            resume_analysis,
            "PROJECTS"
        )
        
        print("✍️  Step 5: Tailoring SKILLS section...")
        new_skills = self.rewriter.rewrite_section(
            resume_sections['skills'],
            job_analysis,
            resume_analysis,
            "SKILLS"
        )
        
        print("📝 Step 6: Generating tailored resume...")
        generator = LaTeXGenerator(self.resume_path)
        generator.replace_section("EXPERIENCE", new_experience)
        generator.replace_section("PROJECTS", new_projects)
        generator.replace_section("SKILLS", new_skills)
        generator.generate(output_path)
        
        print(f"✅ Done! Tailored resume saved to: {output_path}")
        return output_path
