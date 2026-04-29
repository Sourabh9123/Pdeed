import io
from fastapi import UploadFile
from pypdf import PdfReader
from app.core.logging import get_logger

logger = get_logger(__name__)

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from the uploaded file.
    Currently supports .txt and basic .pdf.
    
    TODO / FUTURE OPTIMIZATION:
    For production, we can integrate the `xpdf` binary (`pdftotext`) 
    which is extremely fast and robust for PDF processing.
    
    For images (png, jpeg, etc.) or scanned PDFs, we should integrate OCR
    (like Tesseract or a cloud OCR service).
    """
    filename = file.filename.lower()
    
    # Read the file content into memory
    content = await file.read()
    
    if filename.endswith(".txt"):
        logger.info(f"Extracting text from plain text file: {filename}")
        return content.decode("utf-8")
        
    elif filename.endswith(".pdf"):
        logger.info(f"Extracting text from PDF file: {filename}")
        # Doing the 'easy' way with PyPDF for now
        # COMMENT: We can use xpdf binary (pdftotext) here for much faster extraction
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            extracted_text = ""
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
            return extracted_text.strip()
        except Exception as e:
            logger.error(f"Failed to read PDF: {e}")
            raise ValueError("Failed to parse the PDF file.")
            
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        logger.warning(f"Image uploaded without OCR integration: {filename}")
        # COMMENT: This is where we would call OCR like Tesseract or xpad/xpdf OCR utilities.
        raise ValueError("Image OCR is not yet implemented. Please upload a .txt or .pdf file.")
        
    else:
        logger.warning(f"Unsupported file type: {filename}")
        raise ValueError("Unsupported file format. Please upload .txt or .pdf.")
