from backend.agent import RoleFitAgent
import os

def main():
    print("=" * 60)
    print("🎯 RoleFit - AI Resume Tailoring Agent")
    print("=" * 60)
    print()
    
    # Resume path
    resume_path = os.path.join("latex", "haile_resume.tex")
    
    # Get job description
    print("📋 Paste the job description below (press Enter twice when done):")
    print("-" * 60)
    
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)
    
    job_description = "\n".join(lines)
    
    if not job_description.strip():
        print("❌ No job description provided. Exiting.")
        return
    
    print()
    print("🚀 Starting AI agent...")
    print()
    
    # Create agent and tailor resume
    agent = RoleFitAgent(resume_path)
    output_path = os.path.join("output", "tailored_resume.tex")
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    agent.tailor_resume(job_description, output_path)
    
    print()
    print("=" * 60)
    print("🎉 Your tailored resume is ready!")
    print(f"📁 Location: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
