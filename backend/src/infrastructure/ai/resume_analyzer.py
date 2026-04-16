from .groq_client import GroqClient

class ResumeAnalyzer:
    def __init__(self):
        self.client = GroqClient()
    
    def analyze(self, resume_sections: dict) -> dict:
        system_prompt = """You are an expert resume analyzer. Analyze the resume content and identify:
- Writing style and tone
- Key strengths and achievements
- Technical skills
- Experience level"""
        
        resume_text = "\n\n".join([f"{k}:\n{v}" for k, v in resume_sections.items()])
        response = self.client.chat(system_prompt, resume_text)
        return {"analysis": response}
