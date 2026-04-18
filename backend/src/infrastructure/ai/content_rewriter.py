from .groq_client import GroqClient

class ContentRewriter:
    def __init__(self):
        self.client = GroqClient()
    
    def rewrite_section(self, section_name: str, original_content: str, 
                       job_analysis: dict, resume_analysis: dict) -> str:
        system_prompt = f"""You are an expert resume writer. Rewrite the {section_name} section to match the job requirements.

CRITICAL RULES FOR EXPERIENCE:
- DO NOT add new technologies, frameworks, or tools not in the original
- ONLY add relevant keywords from the job description naturally into existing bullet points
- Keep all original tech stacks and project details unchanged
- Reword sentences to emphasize relevance to the job
- Make existing accomplishments sound more aligned with job requirements

CRITICAL RULES FOR SKILLS:
- Reorder existing skills to prioritize job-relevant ones first
- ADD new skills from the job description that are missing (user is applying, so they can learn these)
- Group related skills together (e.g., Frontend, Backend, DevOps)
- Put most relevant skills at the top
- Format: Keep the same structure as original (bullet points, comma-separated, etc.)

GENERAL RULES:
- Maintain original structure and formatting
- Keep the original writing style
- Return ONLY the rewritten content, no explanations"""
        
        user_message = f"""Job Requirements:
{job_analysis.get('analysis', '')}

Original {section_name}:
{original_content}

Rewrite this section to better match the job while maintaining the LaTeX structure and original voice."""
        
        return self.client.chat(system_prompt, user_message)
