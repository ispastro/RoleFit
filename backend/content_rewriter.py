from backend.groq_client import GroqClient

class ContentRewriter:
    def __init__(self):
        self.groq = GroqClient()
    
    def rewrite_section(self, section_content, job_analysis, resume_analysis, section_name):
        """Rewrite resume section to match job requirements while keeping candidate's voice"""
        prompt = f"""Rewrite this {section_name} section to perfectly match the job requirements.

CRITICAL RULES:
1. Keep the EXACT LaTeX structure and formatting
2. Maintain the candidate's writing style and voice
3. Emphasize skills and experiences that match job requirements
4. Use keywords from the job description naturally
5. Keep all \\resumeItem, \\resumeSubheading commands intact
6. Quantify achievements when possible
7. Make it ATS-friendly

Job Requirements:
{job_analysis}

Candidate Profile:
{resume_analysis}

Original {section_name} Section:
{section_content}

Return ONLY the rewritten LaTeX code, nothing else."""

        messages = [
            {"role": "system", "content": "You are an expert resume writer. Rewrite content to match job requirements while preserving LaTeX structure and candidate's voice."},
            {"role": "user", "content": prompt}
        ]
        
        return self.groq.chat(messages, temperature=0.7, max_tokens=3000)
