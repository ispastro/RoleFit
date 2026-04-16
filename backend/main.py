import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.cli import CLI

def main():
    resume_path = os.path.join("latex", "haile_resume.tex")
    cli = CLI(resume_path)
    cli.run()

if __name__ == "__main__":
    main()
