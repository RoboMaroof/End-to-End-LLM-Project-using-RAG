from fastapi import APIRouter, HTTPException, Query
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
from app.models import SearchQuery, DocumentSearchResult
from typing import List

router = APIRouter()
vector_db = VectorDB()
summarizer = Summarizer()

@router.get("/search", response_model=List[DocumentSearchResult])
async def search_documents(query: str = Query(...)):
    try:
        query_embedding = summarizer.embed(query)
        results = vector_db.search_documents(query_embedding)
        return [DocumentSearchResult(**result) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
