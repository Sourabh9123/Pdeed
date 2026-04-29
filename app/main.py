from fastapi import FastAPI
from app.api.routes import document

app = FastAPI(title="Document Intelligence Platform API", version="1.0.0")

app.include_router(document.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
