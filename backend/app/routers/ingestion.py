from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
from app.models import DocumentIngest
import fitz
import logging

logger = logging.getLogger(__name__)

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

# @router.post("/ingest", response_model=DocumentIngest)
@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
    try:
        # Read and process the file content based on type (PDF or text).
        if file.content_type == "application/pdf":
            content = extract_text_from_pdf(file)
        else:
            content = await file.read()
            content = content.decode('utf-8')
        logger.info(f"Content of length {len(content)} extracted")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    try:
        # Chunk the content.
        chunks = summarizer.chunk_text(content, max_length=512)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing document: {str(e)}")

    try:
        # Summarize the content.
        summary = summarizer.summarize(chunks)
        logger.info(f"{len(chunks)} chunks created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing document: {str(e)}")

    try:
        # Generate embedding for the content.
        embedding = summarizer.embed(chunks)
        logger.info(f"{len(embedding)} embeddings created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")

    try:
        # Store the document summary and embedding in the vector database.
        vector_db.store_document(file.filename, summary, embedding)
        logger.info(f"Summary and embeddings for {file.filename} stored in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing document in vector database: {str(e)}")

    logger.info("File ingestion completed")


