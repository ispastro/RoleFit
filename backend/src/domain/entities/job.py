from dataclasses import dataclass

@dataclass
class Job:
    """Domain entity representing a job description"""
    description: str
    analysis: str = ""
    
    def __post_init__(self):
        if not self.description.strip():
            raise ValueError("Job description cannot be empty")
