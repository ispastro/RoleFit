from backend.groq_client import GroqClient

class ResumeAnalyzer:
    def __init__(self):
        self.groq = GroqClient()
    
    def analyze(self, resume_sections):
        """Analyze resume to understand candidate's strengths and experience"""
        prompt = f"""Analyze this resume and identify:
1. Core technical skills and expertise
2. Key achievements and quantifiable results
3. Experience level and seniority
4. Domain expertise
5. Unique value propositions
6. Writing style and tone

Resume Content:
Experience: {resume_sections['experience']}
Projects: {resume_sections['projects']}
Skills: {resume_sections['skills']}

Provide structured analysis."""

        messages = [
            {"role": "system", "content": "You are an expert resume analyzer. Identify strengths and unique value."},
            {"role": "user", "content": prompt}
        ]
        
        return self.groq.chat(messages, temperature=0.3)
