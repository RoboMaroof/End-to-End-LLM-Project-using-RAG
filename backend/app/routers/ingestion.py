from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
from app.models import DocumentIngest
import fitz

router = APIRouter()
vector_db = VectorDB()
summarizer = Summarizer()

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_document = fitz.open(stream=file.file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text

@router.post("/ingest", response_model=DocumentIngest)
async def ingest_document(file: UploadFile = File(...)):
    try:
        if file.content_type == "application/pdf":
            content = extract_text_from_pdf(file)
        else:
            content = await file.read()
            content = content.decode('utf-8')
        summary = summarizer.summarize(content.decode('utf-8'))
        embedding = summarizer.embed(content.decode('utf-8')).tolist()
        vector_db.store_document(file.filename, summary, embedding)
        return DocumentIngest(filename=file.filename, summary=summary, embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
