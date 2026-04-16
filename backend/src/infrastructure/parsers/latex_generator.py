class LaTeXGenerator:
    def __init__(self, original_tex_path):
        with open(original_tex_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
    
    def replace_section(self, section_name, new_content):
        """Replace a section in the LaTeX template with new content"""
        import re
        pattern = rf'(\\section\{{{section_name}\}})(.*?)(?=\\section|\\end\{{document\}})'
        replacement = rf'\1\n{new_content}\n'
        self.template = re.sub(pattern, replacement, self.template, flags=re.DOTALL)
    
    def generate(self, output_path):
        """Write the tailored resume to a new file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.template)
    
    def generate_tailored_resume(self, tailored_sections, output_path):
        """Generate tailored resume with new sections"""
        for section_name, new_content in tailored_sections.items():
            self.replace_section(section_name.upper(), new_content)
        self.generate(output_path)
