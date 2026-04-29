from pydantic import BaseModel
from typing import List

class DocumentRequest(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str

class DocumentAnalysisResponse(BaseModel):
    summary: str
    entities: List[Entity]
