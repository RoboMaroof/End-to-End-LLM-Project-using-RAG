# Document Processing and Search Backend

## Overview

The backend of this application is designed to handle document ingestion (upload and processing), search through the ingested documents using natural language queries, and return summarized results. It is built using FastAPI, a modern web framework for building APIs with Python.

## Key Components

- **FastAPI**: The web framework used to create the API.
- **SQLite**: A lightweight database to store documents and their embeddings.
- **Transformers**: A library to handle natural language processing tasks such as summarization and creating embeddings.
- **Docker**: Used to containerize the application, making it easy to deploy.
- **Pydantic**: Used for data validation and serialization.

## Backend Directory Structure

* `main.py`: Entry point of the FastAPI application.
* `models.py`: Defines the data models for the API.
* `routers/`: Contains the routes (endpoints) for the API.
   * `ingestion.py`: Handles document ingestion.
   * `search.py`: Handles searching through documents.
* `services/`: Contains the service logic.
   * `db_init.py`: Initializes the SQLite database.
   * `vector_db.py`: Manages storing and retrieving documents from the database.
   * `summarizer.py`: Handles summarization and embedding creation.
* `requirements.txt`: Lists the dependencies needed for the project.
* `Dockerfile`: Instructions to containerize the application.
* `tests/`: Contains tests for the API.

## How It Works

### 1. Starting the Application - `main.py`
```python
from fastapi import FastAPI
from app.routers import ingestion, search
from app.services.db_init import initialize_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(ingestion.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    logger.info("Starting up...")
    initialize_db()

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
* **FastAPI** initializes and sets up the routes (endpoints) for ingestion and search.
* When the application starts, it initializes the database.

### 2. Defining Data Models - `models.py`
```python
from pydantic import BaseModel
from typing import List

class DocumentIngest(BaseModel):
    filename: str
    summary: str
    embedding: List[float]

class DocumentSearchResult(BaseModel):
    filename: str
    summary: str
    similarity: float
```
* Defines the structure of data for ingestion and search responses using Pydantic.

### 3. Document Ingestion - `ingestion.py`
```python
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
import fitz  # PyMuPDF

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

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        if file.content_type == "application/pdf":
            content = extract_text_from_pdf(file)
        else:
            content = await file.read()
            content = content.decode('utf-8')
            
        summary = summarizer.summarize(content)
        embedding = summarizer.embed(content)
        vector_db.store_document(file.filename, summary, embedding)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
* **Route**: `/api/v1/ingest` for document upload.
* **Process**:
   1. Reads the uploaded file.
   2. Summarizes the content using the summarizer service.
   3. Creates an embedding for the content.
   4. Stores the filename, summary, and embedding in the database.

### 4. Document Search - `search.py`
```python
from fastapi import APIRouter, HTTPException, Query
from app.services.vector_db import VectorDB
from app.services.summarizer import Summarizer
from app.models import DocumentSearchResult
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
```
* **Route**: `/api/v1/search` for searching documents.
* **Process**:
   1. Embeds the search query using the summarizer.
   2. Searches the database for similar document embeddings.
   3. Returns the most relevant documents with their summaries and similarity scores.

### 5. Database Initialization - `db_init.py`
```python
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vector_db.sqlite")

def initialize_db():
    conn = sqlite3.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            summary TEXT,
            embedding BLOB
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
```
* **Function**: Creates the SQLite database and the `documents` table if it doesn't exist.

### 6. Managing the Database - `vector_db.py`
```python
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class VectorDB:
    def __init__(self):
        self.conn = sqlite3.connect('vector_db.sqlite', check_same_thread=False)
        self.c = self.conn.cursor()

    def store_document(self, filename: str, summary: str, embedding):
        embedding_blob = pickle.dumps(embedding)
        self.c.execute('''
            INSERT INTO documents (filename, summary, embedding)
            VALUES (?, ?, ?)
        ''', (filename, summary, embedding_blob))
        self.conn.commit()

    def search_documents(self, query_embedding):
        self.c.execute('SELECT id, filename, summary, embedding FROM documents')
        documents = self.c.fetchall()
        embeddings = [pickle.loads(doc[3]) for doc in documents]
        similarities = cosine_similarity(query_embedding, np.vstack(embeddings))
        ranked_indices = np.argsort(similarities[0])[::-1]
        results = [{
            "filename": documents[idx][1],
            "summary": documents[idx][2],
            "similarity": similarities[0][idx]
        } for idx in ranked_indices]
        return results
```
**Functions**:
1. `store_document()`: Stores a document's filename, summary, and embedding in the database.
2. `search_documents()`: Searches for documents based on the similarity of their embeddings to the query embedding.

### 7. Summarization and Embedding - `summarizer.py`
```python
from transformers import pipeline, AutoTokenizer, AutoModel

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization")
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def summarize(self, text: str) -> str:
        summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def embed(self, text: str):
        inputs = self.tokenizer(text, return_tensors='pt')
        outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.detach().numpy()
```
**Functions**:
1. `summarize()`: Generates a summary for a given text.
2. `embed()`: Creates an embedding for a given text.

## Summary

- **Document Ingestion**: Users upload documents, which are summarized and stored in the database with their embeddings.
- **Document Search**: Users search for documents using natural language queries, which are embedded and compared to stored document embeddings to find and return the most relevant documents with summaries.

## Docker and Deployment

The Dockerfile and docker-compose.yml help in containerizing the application, making it easier to deploy on any environment that supports Docker.
By following these steps, the backend is designed to handle document upload, processing, storage, and search efficiently using FastAPI, SQLite, and machine learning models from the transformers library.