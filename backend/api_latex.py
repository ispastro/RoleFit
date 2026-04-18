from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

from src.infrastructure.ai.latex_resume_generator import LatexResumeGenerator
from src.infrastructure.parsers.file_extractor import extract_text_from_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RoleFit API", version="2.0.0", description="LaTeX-powered resume tailoring")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "RoleFit API v2.0", "status": "running", "engine": "LaTeX"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RoleFit LaTeX API"}

@app.post("/api/tailor-latex")
async def tailor_resume_latex(
    job_description: str = Form(...),
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Tailor resume and return LaTeX code for Overleaf.
    """
    try:
        logger.info("Received LaTeX tailoring request")
        
        if not job_description or not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        # Get resume content
        resume_content = None
        
        if resume_file:
            logger.info(f"Processing uploaded file: {resume_file.filename}")
            file_content = await resume_file.read()
            resume_content = extract_text_from_file(file_content, resume_file.filename)
            logger.info(f"Extracted {len(resume_content)} characters from file")
            
            if not resume_content or len(resume_content.strip()) < 10:
                raise HTTPException(status_code=400, detail="Could not extract text from file")
        elif resume_text:
            logger.info("Processing pasted resume text")
            resume_content = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload or paste your resume")
        
        # Generate LaTeX code
        logger.info("Generating LaTeX code...")
        latex_generator = LatexResumeGenerator()
        latex_code = latex_generator.generate_tailored_latex(resume_content, job_description)
        
        logger.info("LaTeX code generated successfully")
        
        # Return LaTeX code as JSON
        return {
            "latex_code": latex_code,
            "message": "LaTeX code generated successfully. Copy to Overleaf to compile."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating LaTeX: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_latex:app", host="0.0.0.0", port=8000, reload=True)


@app.post("/api/evaluate-resume")
async def evaluate_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """
    Evaluate resume quality and provide scoring.
    """
    try:
        logger.info("Received resume evaluation request")
        
        if not resume_text or not resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is required")
        
        if not job_description or not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        # Evaluate resume
        logger.info("Evaluating resume...")
        latex_generator = LatexResumeGenerator()
        evaluation = latex_generator.evaluate_resume(resume_text, job_description)
        
        logger.info("Resume evaluated successfully")
        
        return evaluation
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluating resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
