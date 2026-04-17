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
3. For EXPERIENCE: DO NOT add new technologies, frameworks, or tools not already in the original content - ONLY emphasize existing ones
4. For EXPERIENCE: ONLY reword bullet points to highlight relevance - keep all tech stacks truthful
5. For SKILLS: ONLY reorder existing skills to prioritize job-relevant ones - DO NOT add new skills
6. Focus on emphasizing keywords from job description that ALREADY exist in the content
7. Rewrite descriptions for impact, but never fabricate technical details
8. Return ONLY the rewritten LaTeX content, no explanations"""
        
        user_message = f"""Job Requirements:
{job_analysis.get('analysis', '')}

Original {section_name}:
{original_content}

Rewrite this section to better match the job while maintaining the LaTeX structure and original voice."""
        
        return self.client.chat(system_prompt, user_message)
