from fastapi import APIRouter, HTTPException
from app.models.document import DocumentRequest, DocumentAnalysisResponse
from app.services.llm_service import analyze_document_text
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(request: DocumentRequest):
    try:
        analysis_result = await analyze_document_text(request.text)
        return DocumentAnalysisResponse(**analysis_result)
    except ValueError as e:
        logger.warning(f"Validation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Runtime Error during analysis: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e)) # 502 Bad Gateway is appropriate since we are calling an external service
    except Exception as e:
        logger.exception("Unexpected internal server error.")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")
