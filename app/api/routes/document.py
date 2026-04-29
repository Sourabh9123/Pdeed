from fastapi import APIRouter, HTTPException
from app.models.document import DocumentRequest, DocumentAnalysisResponse
from app.services.llm_service import analyze_document_text

router = APIRouter()

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(request: DocumentRequest):
    try:
        analysis_result = await analyze_document_text(request.text)
        return DocumentAnalysisResponse(**analysis_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
