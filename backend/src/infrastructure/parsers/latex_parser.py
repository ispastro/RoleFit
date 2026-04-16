import re

class LaTeXParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def get_all_sections(self) -> dict:
        sections = {}
        
        # Extract preamble (everything before \begin{document})
        preamble_match = re.search(r'(.*?)\\begin\{document\}', self.content, re.DOTALL)
        if preamble_match:
            sections['preamble'] = preamble_match.group(1)
        
        # Extract heading
        heading_match = re.search(r'%----------HEADING----------(.*?)(?=%----------|\Z)', 
                                 self.content, re.DOTALL)
        if heading_match:
            sections['heading'] = heading_match.group(1).strip()
        
        # Extract EXPERIENCE section
        exp_match = re.search(r'%-----------EXPERIENCE-----------(.*?)(?=%-----------[A-Z]|\\end\{document\})', 
                             self.content, re.DOTALL)
        if exp_match:
            sections['experience'] = exp_match.group(1).strip()
        
        # Extract PROJECTS section
        proj_match = re.search(r'%-----------PROJECTS-----------(.*?)(?=%-----------[A-Z]|\\end\{document\})', 
                              self.content, re.DOTALL)
        if proj_match:
            sections['projects'] = proj_match.group(1).strip()
        
        # Extract EDUCATION section
        edu_match = re.search(r'%-----------EDUCATION-----------(.*?)(?=%-----------[A-Z]|\\end\{document\})', 
                             self.content, re.DOTALL)
        if edu_match:
            sections['education'] = edu_match.group(1).strip()
        
        # Extract SKILLS section
        skills_match = re.search(r'%-----------SKILLS-----------(.*?)(?=\\end\{document\})', 
                                self.content, re.DOTALL)
        if skills_match:
            sections['skills'] = skills_match.group(1).strip()
        
        return sections
