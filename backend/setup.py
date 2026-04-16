# -*- coding: utf-8 -*-
"""
Setup script for RoleFit
"""
import os
import sys

print("=" * 60)
print("RoleFit Setup")
print("=" * 60)

# Check if .env exists
env_path = os.path.join(os.path.dirname(__file__), '.env')
env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')

if os.path.exists(env_path):
    print("\n[OK] .env file already exists")
else:
    print("\n[SETUP] Creating .env file...")
    if os.path.exists(env_example_path):
        with open(env_example_path, 'r') as f:
            content = f.read()
        with open(env_path, 'w') as f:
            f.write(content)
        print("[PASS] .env file created from .env.example")
    else:
        with open(env_path, 'w') as f:
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
        print("[PASS] .env file created")

# Check if output directory exists
output_dir = os.path.join(os.path.dirname(__file__), 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("[PASS] output/ directory created")
else:
    print("[OK] output/ directory exists")

# Check if latex directory and resume exist
latex_dir = os.path.join(os.path.dirname(__file__), 'latex')
resume_path = os.path.join(latex_dir, 'haile_resume.tex')

if os.path.exists(resume_path):
    print("[OK] Resume template found")
else:
    print("[WARN] Resume template not found at latex/haile_resume.tex")

print("\n" + "=" * 60)
print("Setup Instructions:")
print("=" * 60)
print("\n1. Get Groq API Key:")
print("   - Visit: https://console.groq.com")
print("   - Sign up and create an API key")
print("\n2. Configure API Key:")
print(f"   - Open: {env_path}")
print("   - Replace 'your_groq_api_key_here' with your actual key")
print("\n3. Install Dependencies:")
print("   - Run: pip install -r requirements.txt")
print("\n4. Test Setup:")
print("   - Run: python test_imports.py")
print("\n5. Run RoleFit:")
print("   - Run: python main.py")
print("\n" + "=" * 60)
print("Setup complete!")
print("=" * 60)
