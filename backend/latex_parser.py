import re

class LaTeXParser:
    def __init__(self, tex_file_path):
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def extract_section(self, section_name):
        """Extract content between \\section{NAME} and next \\section or \\end{document}"""
        pattern = rf'\\section\{{{section_name}\}}(.*?)(?=\\section|\\end\{{document\}})'
        match = re.search(pattern, self.content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def extract_experience(self):
        return self.extract_section("EXPERIENCE")
    
    def extract_projects(self):
        return self.extract_section("PROJECTS")
    
    def extract_skills(self):
        return self.extract_section("SKILLS")
    
    def extract_education(self):
        return self.extract_section("EDUCATION")
    
    def get_all_sections(self):
        return {
            "experience": self.extract_experience(),
            "projects": self.extract_projects(),
            "skills": self.extract_skills(),
            "education": self.extract_education()
        }
