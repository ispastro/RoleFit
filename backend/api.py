from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import os
import logging
from pathlib import Path

from src.domain.entities.resume import Resume
from src.domain.entities.job import Job
from src.domain.use_cases.tailor_resume import TailorResumeUseCase
from src.infrastructure.ai.job_analyzer import JobAnalyzer
from src.infrastructure.ai.resume_analyzer import ResumeAnalyzer
from src.infrastructure.ai.content_rewriter import ContentRewriter
from src.infrastructure.parsers.plaintext_parser import PlainTextParser
from src.infrastructure.parsers.markdown_generator import MarkdownGenerator
from src.infrastructure.parsers.file_extractor import extract_text_from_file

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

from pydantic import BaseModel

class TailorRequest(BaseModel):
    job_description: str

class TailorResponse(BaseModel):
    message: str
    download_url: str
    tex_content: str

@app.get("/")
def root():
    return {"message": "RoleFit API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RoleFit API"}

@app.post("/api/tailor", response_model=TailorResponse)
async def tailor_resume(
    job_description: str = Form(...),
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    try:
        logger.info("Received tailoring request")
        
        if not job_description or not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        # Get resume content (file upload, pasted text, or default template)
        resume_content = None
        
        if resume_file:
            # File uploaded
            logger.info(f"Processing uploaded file: {resume_file.filename}")
            file_content = await resume_file.read()
            resume_content = extract_text_from_file(file_content, resume_file.filename)
        elif resume_text:
            # Text pasted
            logger.info("Processing pasted resume text")
            resume_content = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload or paste your resume")
        
        # Parse and tailor
        parser = PlainTextParser(resume_content)
        generator = MarkdownGenerator()
        
        logger.info("Parsing resume...")
        resume_sections = parser.get_all_sections()
        resume = Resume.from_sections(resume_sections)
        job = Job(description=job_description)
        
        logger.info("Initializing AI services...")
        use_case = TailorResumeUseCase(
            job_analyzer=JobAnalyzer(),
            resume_analyzer=ResumeAnalyzer(),
            content_rewriter=ContentRewriter(),
            latex_generator=generator
        )
        
        output_path = os.path.join("output", "tailored_resume.md")
        os.makedirs("output", exist_ok=True)
        
        logger.info("Tailoring resume...")
        result = use_case.execute(resume, job, output_path)
        
        # Read the content for preview
        if not os.path.exists(result):
            raise RuntimeError("Failed to generate tailored resume")
            
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"Resume tailored successfully: {result}")
        
        return TailorResponse(
            message="Resume tailored successfully",
            download_url=f"/api/download/{Path(result).name}",
            tex_content=content
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tailoring resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/download/{filename}")
async def download_resume(filename: str):
    try:
        # Only allow MD downloads
        if not filename.endswith('.md'):
            raise HTTPException(status_code=400, detail="Only Markdown downloads are supported")
        
        # Sanitize filename to prevent directory traversal
        filename = os.path.basename(filename)
        file_path = os.path.join("output", filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine media type
        media_type = "text/markdown"
        
        logger.info(f"Serving file: {filename}")
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to download file")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
