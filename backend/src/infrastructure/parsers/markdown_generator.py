class MarkdownGenerator:
    def __init__(self, template_path: str = None):
        self.template_path = template_path
    
    def generate(self, sections: dict, output_path: str) -> str:
        """Generate markdown resume from sections."""
        markdown_content = []
        
        # Add heading
        if sections.get('heading'):
            markdown_content.append(sections['heading'])
            markdown_content.append('')
        
        # Add experience
        if sections.get('experience'):
            markdown_content.append('## Experience')
            markdown_content.append(sections['experience'])
            markdown_content.append('')
        
        # Add projects
        if sections.get('projects'):
            markdown_content.append('## Projects')
            markdown_content.append(sections['projects'])
            markdown_content.append('')
        
        # Add education
        if sections.get('education'):
            markdown_content.append('## Education')
            markdown_content.append(sections['education'])
            markdown_content.append('')
        
        # Add skills
        if sections.get('skills'):
            markdown_content.append('## Skills')
            markdown_content.append(sections['skills'])
            markdown_content.append('')
        
        # Write to file
        final_content = '\n'.join(markdown_content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return output_path
