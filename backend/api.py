from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging
from pathlib import Path

from src.domain.entities.resume import Resume
from src.domain.entities.job import Job
from src.domain.use_cases.tailor_resume import TailorResumeUseCase
from src.infrastructure.ai.job_analyzer import JobAnalyzer
from src.infrastructure.ai.resume_analyzer import ResumeAnalyzer
from src.infrastructure.ai.content_rewriter import ContentRewriter
from src.infrastructure.parsers.latex_parser import LaTeXParser
from src.infrastructure.parsers.latex_generator import LaTeXGenerator
from src.infrastructure.parsers.pdf_compiler import compile_latex_to_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RoleFit API", version="1.0.0", description="AI-powered resume tailoring")

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

class TailorRequest(BaseModel):
    job_description: str

class TailorResponse(BaseModel):
    message: str
    download_url: str

@app.get("/")
def root():
    return {"message": "RoleFit API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RoleFit API"}

@app.post("/api/tailor", response_model=TailorResponse)
async def tailor_resume(request: TailorRequest):
    try:
        logger.info("Received tailoring request")
        
        if not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        resume_path = os.path.join("latex", "haile_resume.tex")
        if not os.path.exists(resume_path):
            logger.error(f"Resume template not found at {resume_path}")
            raise HTTPException(status_code=404, detail="Resume template not found")
        
        logger.info("Parsing resume...")
        parser = LaTeXParser(resume_path)
        resume_sections = parser.get_all_sections()
        resume = Resume.from_sections(resume_sections)
        job = Job(description=request.job_description)
        
        logger.info("Initializing AI services...")
        use_case = TailorResumeUseCase(
            job_analyzer=JobAnalyzer(),
            resume_analyzer=ResumeAnalyzer(),
            content_rewriter=ContentRewriter(),
            latex_generator=LaTeXGenerator(resume_path)
        )
        
        output_path = os.path.join("output", "tailored_resume.tex")
        os.makedirs("output", exist_ok=True)
        
        logger.info("Tailoring resume...")
        result = use_case.execute(resume, job, output_path)
        
        # Compile to PDF
        logger.info("Compiling to PDF...")
        final_file = compile_latex_to_pdf(result)
        logger.info(f"Resume tailored successfully: {final_file}")
        
        return TailorResponse(
            message="Resume tailored successfully",
            download_url=f"/api/download/{Path(final_file).name}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tailoring resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/download/{filename}")
async def download_resume(filename: str):
    # Only allow PDF downloads
    if not filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF downloads are supported")
    
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
