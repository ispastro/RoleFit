from dataclasses import dataclass
from typing import Dict

@dataclass
class Resume:
    sections: Dict[str, str]
    
    @classmethod
    def from_sections(cls, sections: Dict[str, str]):
        return cls(sections=sections)
