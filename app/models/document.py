from pydantic import BaseModel
from typing import List, Optional

class Entity(BaseModel):
    text: str
    label: str

class DocumentAnalysisResponse(BaseModel):
    document_type: str
    language: str
    summary: str
    key_themes: List[str]
    entities: List[Entity]
    sentiment: str
    action_items: List[str]
