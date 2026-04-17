import os
import logging
import requests
import time

logger = logging.getLogger(__name__)

def compile_latex_to_pdf(tex_file_path: str, max_retries: int = 2) -> str:
    """Compile LaTeX to PDF using texlive.net API with retry logic."""
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Compiling LaTeX to PDF (attempt {attempt + 1}/{max_retries})...")
            
            # Read the tex file
            with open(tex_file_path, 'r', encoding='utf-8') as f:
                latex_code = f.read()
            
            logger.info(f"LaTeX file size: {len(latex_code)} bytes")
            
            # Use texlive.net API (free, no auth)
            url = "https://texlive.net/cgi-bin/latexcgi"
            
            # Prepare the request
            data = {
                'filecontents[]': latex_code,
                'filename[]': 'document.tex',
                'engine': 'pdflatex',
                'return': 'pdf'
            }
            
            response = requests.post(
                url,
                data=data,
                timeout=90,
                headers={'User-Agent': 'RoleFit/1.0'}
            )
            
            logger.info(f"API response status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if response is actually a PDF
                if response.content[:4] == b'%PDF':
                    pdf_path = tex_file_path.replace('.tex', '.pdf')
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"PDF compiled successfully: {pdf_path}")
                    return pdf_path
                else:
                    logger.error(f"Response is not a PDF. First 100 bytes: {response.content[:100]}")
                    raise RuntimeError("API returned invalid PDF")
            else:
                error_msg = response.text[:500] if response.text else "No error message"
                logger.error(f"API error {response.status_code}: {error_msg}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"API returned error {response.status_code}")
                
        except requests.Timeout:
            logger.error(f"API request timed out (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("PDF compilation timed out")
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    
    raise RuntimeError("PDF compilation failed after all retries")
