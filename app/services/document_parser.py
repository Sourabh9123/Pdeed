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
            
    elif filename.endswith(".docx"):
        logger.info(f"Extracting text from DOCX file: {filename}")
        try:
            import docx
            doc_file = io.BytesIO(content)
            doc = docx.Document(doc_file)
            extracted_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return extracted_text.strip()
        except ImportError:
            logger.error("python-docx is not installed.")
            raise RuntimeError("System configuration error for DOCX processing.")
        except Exception as e:
            logger.error(f"Failed to read DOCX: {e}")
            raise ValueError("Failed to parse the DOCX file.")
            
    elif filename.endswith(".doc"):
        logger.info(f"Extracting text from DOC file using antiword: {filename}")
        try:
            import subprocess
            import tempfile
            import os
            
            # Antiword requires a real file path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".doc") as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
                
            result = subprocess.run(['antiword', temp_file_path], capture_output=True, text=True)
            os.remove(temp_file_path)
            
            if result.returncode != 0:
                logger.error(f"Antiword failed: {result.stderr}")
                raise ValueError("Failed to parse the DOC file (antiword error).")
                
            return result.stdout.strip()
        except FileNotFoundError:
            logger.error("antiword binary is not installed on the system.")
            raise RuntimeError("System configuration error for DOC processing.")
        except Exception as e:
            logger.error(f"Failed to read DOC: {e}")
            raise ValueError("Failed to parse the DOC file.")
            
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        logger.warning(f"Image uploaded without OCR integration: {filename}")
        # COMMENT: This is where we would call OCR like Tesseract or xpad/xpdf OCR utilities.
        raise ValueError("Image OCR is not yet implemented. Please upload a .txt or .pdf file.")
        
    else:
        logger.warning(f"Unsupported file type: {filename}")
        raise ValueError("Unsupported file format. Please upload .txt or .pdf.")
