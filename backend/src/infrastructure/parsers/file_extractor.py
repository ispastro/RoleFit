import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extract plain text from uploaded file (PDF, DOCX, or TXT).
    
    Args:
        file_content: Raw file bytes
        filename: Original filename with extension
        
    Returns:
        Extracted plain text
    """
    file_lower = filename.lower()
    
    try:
        if file_lower.endswith('.pdf'):
            return extract_from_pdf(file_content)
        elif file_lower.endswith('.docx'):
            return extract_from_docx(file_content)
        elif file_lower.endswith(('.txt', '.md', '.tex')):
            return file_content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file format: {filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from {filename}: {str(e)}")


def extract_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    pdf_file = io.BytesIO(file_content)
    reader = PdfReader(pdf_file)
    
    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)
    
    return '\n\n'.join(text_parts)


def extract_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file."""
    docx_file = io.BytesIO(file_content)
    doc = Document(docx_file)
    
    text_parts = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)
    
    return '\n\n'.join(text_parts)
