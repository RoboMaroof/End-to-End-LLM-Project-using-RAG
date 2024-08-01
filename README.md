# End to End LLM Project using Retrieval Augmented Generation (RAG) for Document Search and Summarization System

## Overview
The Intelligent Document Search and Summarization System is a web-based application that allows users to upload documents, search through them using natural language queries, and receive summarized results. It leverages state-of-the-art language models and vector databases to provide accurate and efficient document search and summarization.

## Features
- **Document Upload:** Upload documents for ingestion into the system.
- **Document Search:** Search through uploaded documents using natural language queries.
- **Summarization:** Receive summarized results of the searched documents.
- **Scalable Backend:** Built with FastAPI and Docker for scalability and ease of deployment.
- **Sophisticated Language Processing:** Utilizes Hugging Face Transformers and LangChain for advanced language model interactions.

## Installation

### Prerequisites
- Docker
- Docker Compose

### Setup

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/RoboMaroof/End-to-End-LLM-Project-using-RAG.git
    cd your-repo
    ```

2. **Create Environment File:**
    Create a `.env` file in the project root with the following content:
    ```plaintext
    DATABASE_URL=/data/vector_db.sqlite
    ```

3. **Build and Start the Docker Containers:**
    ```sh
    docker-compose up --build
    ```

### Directory Structure
```plaintext
project-root/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── ingestion.py
│   │   │   ├── search.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── db_init.py
│   │       ├── vector_db.py
│   │       ├── summarizer.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       ├── test_ingestion.py
│       ├── test_search.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DocumentUpload.js
│   │   │   ├── SearchInput.js
│   │   │   ├── SearchResult.js
│   │   ├── App.js
│   │   ├── index.js
│   ├── Dockerfile
│   ├── package.json
│   └── README.md
│
├── ingestion/
│   ├── ingestion_service.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── model/
│   ├── model_service.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingestion-deployment.yaml
│   ├── ingestion-service.yaml
│   ├── model-deployment.yaml
│   ├── model-service.yaml
│   ├── kustomization.yaml
│
├── .github/
│   ├── workflows/
│   │   ├── build-and-deploy.yml
│
└── docker-compose.yml
```


## Usage

### Upload a Document
1. Open the web application.
2. Navigate to the document upload section.
3. Select a document to upload and click the "Upload" button.

### Search Documents
1. Navigate to the search section.
2. Enter a natural language query in the search input.
3. Click the "Search" button.
4. View the summarized results of the documents matching your query.

## Development

### Backend
The backend is built with FastAPI and includes routes for document ingestion and search. It uses a SQLite database for storing document embeddings and summaries.

### Frontend
The frontend is built with React and includes components for document upload, search input, and search results display.

### Ingestion Service
The ingestion service handles document processing and storage. It uses LangChain and Hugging Face Transformers for text summarization and embedding.

### Model Service
The model service provides access to the language models used for summarization and embedding.

### Kubernetes Deployment
Kubernetes manifests are provided for deploying the application in a Kubernetes cluster. The configuration includes deployments and services for the backend, frontend, ingestion, and model services.

## Testing
Unit tests are included for the backend services. To run the tests:

1. Navigate to the `backend` directory.
2. Run the tests using `pytest`:
    ```sh
    pytest
    ```


