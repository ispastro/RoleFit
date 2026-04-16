from src.domain.entities.resume import Resume
from src.domain.entities.job import Job

class TailorResumeUseCase:
    def __init__(self, job_analyzer, resume_analyzer, content_rewriter, latex_generator):
        self.job_analyzer = job_analyzer
        self.resume_analyzer = resume_analyzer
        self.content_rewriter = content_rewriter
        self.latex_generator = latex_generator
    
    def execute(self, resume: Resume, job: Job, output_path: str) -> str:
        # Step 1: Analyze job
        job_analysis = self.job_analyzer.analyze(job.description)
        
        # Step 2: Analyze resume
        resume_analysis = self.resume_analyzer.analyze(resume.sections)
        
        # Step 3: Tailor sections
        tailored_sections = {}
        
        # Keep preamble and heading as-is
        tailored_sections['preamble'] = resume.sections.get('preamble', '')
        tailored_sections['heading'] = resume.sections.get('heading', '')
        
        # Rewrite main sections
        for section in ['experience', 'projects', 'skills']:
            if section in resume.sections:
                tailored_sections[section] = self.content_rewriter.rewrite_section(
                    section, 
                    resume.sections[section],
                    job_analysis,
                    resume_analysis
                )
        
        # Keep education as-is (usually doesn't need tailoring)
        tailored_sections['education'] = resume.sections.get('education', '')
        
        # Step 4: Generate new resume
        return self.latex_generator.generate(tailored_sections, output_path)
