from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok"}


@router.post("/generate", tags=["documents"])
def generate_document(request: DocumentRequest) -> dict:
    try:
        content = generator.generate_document(request)
        return {
            "document_type": request.document_type,
            "content": content,
            "model": generator.model_name,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc
