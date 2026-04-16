class LaTeXGenerator:
    def __init__(self, original_file_path: str):
        self.original_file_path = original_file_path
    
    def generate(self, sections: dict, output_path: str):
        # Build the complete LaTeX document
        latex_content = sections.get('preamble', '') + '\\begin{document}\n\n'
        
        # Add heading
        if 'heading' in sections:
            latex_content += '%----------HEADING----------\n'
            latex_content += sections['heading'] + '\n\n'
        
        # Add experience
        if 'experience' in sections:
            latex_content += '%-----------EXPERIENCE-----------\n'
            latex_content += sections['experience'] + '\n\n'
        
        # Add projects
        if 'projects' in sections:
            latex_content += '%-----------PROJECTS-----------\n'
            latex_content += sections['projects'] + '\n\n'
        
        # Add education
        if 'education' in sections:
            latex_content += '%-----------EDUCATION-----------\n'
            latex_content += sections['education'] + '\n\n'
        
        # Add skills
        if 'skills' in sections:
            latex_content += '%-----------SKILLS-----------\n'
            latex_content += sections['skills'] + '\n\n'
        
        latex_content += '\\end{document}'
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        return output_path
