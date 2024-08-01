from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
from app.models import DocumentIngest

router = APIRouter()
vector_db = VectorDB()
summarizer = Summarizer()

@router.post("/ingest", response_model=DocumentIngest)
async def ingest_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        summary = summarizer.summarize(content.decode('utf-8'))
        embedding = summarizer.embed(content.decode('utf-8')).tolist()
        vector_db.store_document(file.filename, summary, embedding)
        return DocumentIngest(filename=file.filename, summary=summary, embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
