from dataclasses import dataclass
from typing import Dict

@dataclass
class Resume:
    """Domain entity representing a resume"""
    experience: str
    projects: str
    skills: str
    education: str
    
    @classmethod
    def from_sections(cls, sections: Dict[str, str]):
        return cls(
            experience=sections.get('experience', ''),
            projects=sections.get('projects', ''),
            skills=sections.get('skills', ''),
            education=sections.get('education', '')
        )
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'experience': self.experience,
            'projects': self.projects,
            'skills': self.skills,
            'education': self.education
        }
