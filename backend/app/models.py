from pydantic import BaseModel
from typing import List, Optional

class DocumentIngest(BaseModel):
    filename: str
    summary: str
    embedding: List[float]

class DocumentSearchResult(BaseModel):
    filename: str
    summary: str
    similarity: float

class SearchQuery(BaseModel):
    query: str
