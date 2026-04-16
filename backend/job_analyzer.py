from backend.groq_client import GroqClient

class JobAnalyzer:
    def __init__(self):
        self.groq = GroqClient()
    
    def analyze(self, job_description):
        """Extract key requirements, skills, and priorities from job description"""
        prompt = f"""Analyze this job description and extract:
1. Required technical skills (must-have)
2. Preferred skills (nice-to-have)
3. Key responsibilities
4. Experience level required
5. Industry/domain focus
6. Company culture signals
7. Top 5 keywords to emphasize

Job Description:
{job_description}

Provide structured analysis in JSON format."""

        messages = [
            {"role": "system", "content": "You are an expert job description analyzer. Extract key requirements and priorities."},
            {"role": "user", "content": prompt}
        ]
        
        return self.groq.chat(messages, temperature=0.3)
