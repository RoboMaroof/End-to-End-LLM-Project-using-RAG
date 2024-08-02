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

# React alternate, terraform, poetry, frontend backend database all options, langchain