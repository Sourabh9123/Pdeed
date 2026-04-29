from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.document import DocumentAnalysisResponse
from app.services.llm_service import analyze_document_text
from app.services.document_parser import extract_text_from_file
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    try:
        # Extract text from the uploaded file (TXT or PDF)
        extracted_text = await extract_text_from_file(file)
        
        # Pass the extracted text to the LLM service
        analysis_result = await analyze_document_text(extracted_text)
        return DocumentAnalysisResponse(**analysis_result)
    except ValueError as e:
        logger.warning(f"Validation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Runtime Error during analysis: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected internal server error.")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")
