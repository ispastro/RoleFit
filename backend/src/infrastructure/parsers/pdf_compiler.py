import os
import logging
import requests
import time

logger = logging.getLogger(__name__)

def compile_latex_to_pdf(tex_file_path: str, max_retries: int = 2) -> str:
    """Compile LaTeX to PDF using latexonline.cc API with retry logic."""
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Compiling LaTeX to PDF (attempt {attempt + 1}/{max_retries})...")
            
            # Read the tex file
            with open(tex_file_path, 'r', encoding='utf-8') as f:
                latex_code = f.read()
            
            # Use latexonline.cc API
            url = "https://latexonline.cc/compile"
            
            response = requests.post(
                url,
                data={'text': latex_code},
                params={'command': 'pdflatex'},
                timeout=90,
                headers={'User-Agent': 'RoleFit/1.0'}
            )
            
            if response.status_code == 200:
                pdf_path = tex_file_path.replace('.tex', '.pdf')
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"PDF compiled successfully: {pdf_path}")
                return pdf_path
            else:
                logger.warning(f"API returned status {response.status_code}: {response.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise RuntimeError(f"PDF compilation failed after {max_retries} attempts")
                
        except requests.Timeout:
            logger.error(f"API request timed out (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("PDF compilation timed out. Please try again.")
        except requests.RequestException as e:
            logger.error(f"Network error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error during PDF compilation: {str(e)}")
        except Exception as e:
            logger.error(f"PDF compilation error: {e}")
            raise RuntimeError(f"Failed to compile PDF: {str(e)}")
    
    raise RuntimeError("PDF compilation failed after all retries")
