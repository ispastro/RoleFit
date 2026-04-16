from ..entities.resume import Resume
from ..entities.job import Job

class TailorResumeUseCase:
    """Use case: Tailor resume to match job requirements"""
    
    def __init__(self, job_analyzer, resume_analyzer, content_rewriter, latex_generator):
        self.job_analyzer = job_analyzer
        self.resume_analyzer = resume_analyzer
        self.content_rewriter = content_rewriter
        self.latex_generator = latex_generator
    
    def execute(self, resume: Resume, job: Job, output_path: str) -> str:
        """Execute the resume tailoring workflow"""
        
        # Step 1: Analyze job
        job.analysis = self.job_analyzer.analyze(job.description)
        
        # Step 2: Analyze resume
        resume_analysis = self.resume_analyzer.analyze(resume.to_dict())
        
        # Step 3: Rewrite sections
        tailored_sections = {}
        for section_name in ['experience', 'projects', 'skills']:
            original_content = getattr(resume, section_name)
            tailored_content = self.content_rewriter.rewrite_section(
                original_content,
                job.analysis,
                resume_analysis,
                section_name.upper()
            )
            tailored_sections[section_name] = tailored_content
        
        # Step 4: Generate output
        self.latex_generator.generate_tailored_resume(tailored_sections, output_path)
        
        return output_path
