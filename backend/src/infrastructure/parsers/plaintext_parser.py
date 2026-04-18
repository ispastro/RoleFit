import re

class PlainTextParser:
    """Parse resume sections from plain text (works with any format)."""
    
    def __init__(self, text: str):
        self.text = text
    
    def get_section(self, section_name: str) -> str:
        """Extract a section from plain text resume."""
        # Common section headers
        patterns = {
            'heading': self._extract_heading,
            'experience': lambda: self._extract_by_keywords(['experience', 'work history', 'employment', 'work experience']),
            'projects': lambda: self._extract_by_keywords(['projects', 'portfolio']),
            'education': lambda: self._extract_by_keywords(['education', 'academic', 'qualifications']),
            'skills': lambda: self._extract_by_keywords(['skills', 'technical skills', 'competencies', 'expertise'])
        }
        
        extractor = patterns.get(section_name.lower())
        if extractor:
            return extractor()
        return ""
    
    def get_all_sections(self) -> dict:
        """Extract all sections from plain text resume."""
        return {
            'heading': self.get_section('heading'),
            'experience': self.get_section('experience'),
            'projects': self.get_section('projects'),
            'education': self.get_section('education'),
            'skills': self.get_section('skills')
        }
    
    def _extract_heading(self) -> str:
        """Extract name and contact info (first few lines)."""
        lines = self.text.split('\n')
        heading_lines = []
        
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            line = line.strip()
            if line and (i < 5 or '@' in line or 'phone' in line.lower() or 'email' in line.lower()):
                heading_lines.append(line)
            elif len(heading_lines) > 0 and not line:
                break
        
        return '\n'.join(heading_lines)
    
    def _extract_by_keywords(self, keywords: list) -> str:
        """Extract section by finding keyword headers."""
        lines = self.text.split('\n')
        section_lines = []
        in_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            if any(keyword in line_lower for keyword in keywords):
                in_section = True
                continue
            
            # Check if we hit another section (stop)
            if in_section and self._is_section_header(line):
                break
            
            # Collect lines in this section
            if in_section and line.strip():
                section_lines.append(line)
        
        return '\n'.join(section_lines)
    
    def _is_section_header(self, line: str) -> bool:
        """Check if line looks like a section header."""
        line_lower = line.lower().strip()
        common_headers = [
            'experience', 'education', 'skills', 'projects', 'summary',
            'objective', 'certifications', 'awards', 'publications',
            'languages', 'interests', 'references'
        ]
        
        # Short line that matches common headers
        if len(line.strip()) < 30 and any(header in line_lower for header in common_headers):
            return True
        
        # All caps or title case (likely header)
        if line.strip().isupper() or (line.strip() and line.strip()[0].isupper() and ':' not in line):
            words = line.strip().split()
            if len(words) <= 3:
                return True
        
        return False
