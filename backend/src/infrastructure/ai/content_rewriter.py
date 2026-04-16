from .groq_client import GroqClient

class ContentRewriter:
    def __init__(self):
        self.client = GroqClient()
    
    def rewrite_section(self, section_name: str, original_content: str, 
                       job_analysis: dict, resume_analysis: dict) -> str:
        system_prompt = f"""You are an expert resume writer. Rewrite the {section_name} section to match the job requirements.

CRITICAL RULES:
1. Maintain the EXACT LaTeX formatting and structure
2. Keep the original writing style and tone
3. Emphasize relevant skills and experiences
4. Add keywords naturally
5. Keep it concise and impactful
6. Return ONLY the rewritten LaTeX content, no explanations"""
        
        user_message = f"""Job Requirements:
{job_analysis.get('analysis', '')}

Original {section_name}:
{original_content}

Rewrite this section to better match the job while maintaining the LaTeX structure and original voice."""
        
        return self.client.chat(system_prompt, user_message)
