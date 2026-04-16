from .groq_client import GroqClient

class JobAnalyzer:
    def __init__(self):
        self.client = GroqClient()
    
    def analyze(self, job_description: str) -> dict:
        system_prompt = """You are an expert job description analyzer. Extract key information from job descriptions.
Return a JSON object with: required_skills, preferred_skills, key_responsibilities, keywords."""
        
        response = self.client.chat(system_prompt, job_description)
        return {"analysis": response}
