import os
import logging
import requests

logger = logging.getLogger(__name__)

def compile_latex_to_pdf(tex_file_path: str) -> str:
    """Compile LaTeX to PDF using latexonline.cc API (free, no auth required)."""
    try:
        logger.info("Compiling LaTeX to PDF using online API...")
        
        # Read the tex file
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            latex_code = f.read()
        
        # Use latexonline.cc API
        url = "https://latexonline.cc/compile"
        
        response = requests.post(
            url,
            data={'text': latex_code},
            params={'command': 'pdflatex'},
            timeout=60
        )
        
        if response.status_code == 200:
            pdf_path = tex_file_path.replace('.tex', '.pdf')
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"PDF compiled successfully: {pdf_path}")
            return pdf_path
        else:
            logger.error(f"API returned status {response.status_code}")
            raise RuntimeError(f"PDF compilation failed. Please try again.")
            
    except requests.Timeout:
        logger.error("API request timed out")
        raise RuntimeError("PDF compilation timed out. Please try again.")
    except Exception as e:
        logger.error(f"PDF compilation error: {e}")
        raise RuntimeError(f"Failed to compile PDF: {str(e)}")
