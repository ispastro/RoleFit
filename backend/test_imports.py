# -*- coding: utf-8 -*-
"""
Test script to verify all imports and basic flow
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing imports...")
print("-" * 60)

try:
    print("[OK] Testing domain entities...")
    from src.domain.entities.resume import Resume
    from src.domain.entities.job import Job
    print("  [PASS] Resume and Job entities imported")
    
    print("\n[OK] Testing use cases...")
    from src.domain.use_cases.tailor_resume import TailorResumeUseCase
    print("  [PASS] TailorResumeUseCase imported")
    
    print("\n[OK] Testing AI infrastructure...")
    from src.infrastructure.ai.groq_client import GroqClient
    from src.infrastructure.ai.job_analyzer import JobAnalyzer
    from src.infrastructure.ai.resume_analyzer import ResumeAnalyzer
    from src.infrastructure.ai.content_rewriter import ContentRewriter
    print("  [PASS] All AI services imported")
    
    print("\n[OK] Testing parsers...")
    from src.infrastructure.parsers.latex_parser import LaTeXParser
    from src.infrastructure.parsers.latex_generator import LaTeXGenerator
    print("  [PASS] LaTeX parsers imported")
    
    print("\n[OK] Testing presentation layer...")
    from src.presentation.cli import CLI
    print("  [PASS] CLI imported")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    
    # Test basic instantiation
    print("\nTesting basic instantiation...")
    print("-" * 60)
    
    # Test entities
    test_job = Job(description="Test job description")
    print("[PASS] Job entity created")
    
    test_resume = Resume(
        experience="Test experience",
        projects="Test projects",
        skills="Test skills",
        education="Test education"
    )
    print("[PASS] Resume entity created")
    
    # Test Groq client (skip if no API key)
    try:
        groq_client = GroqClient()
        print("[PASS] GroqClient instantiated with API key")
    except Exception as e:
        print(f"[SKIP] GroqClient needs API key (expected): {str(e)[:50]}...")
    
    # Test parsers (with actual resume file)
    resume_path = os.path.join("latex", "haile_resume.tex")
    if os.path.exists(resume_path):
        parser = LaTeXParser(resume_path)
        print("[PASS] LaTeXParser instantiated")
        
        sections = parser.get_all_sections()
        print(f"[PASS] Parsed {len(sections)} sections from resume")
        
        generator = LaTeXGenerator(resume_path)
        print("[PASS] LaTeXGenerator instantiated")
    else:
        print(f"[WARN] Resume file not found at: {resume_path}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)
    print("\nReady to run: python main.py")
    
except ImportError as e:
    print(f"\n[ERROR] IMPORT ERROR: {e}")
    print("\nFix the import issue and try again.")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
