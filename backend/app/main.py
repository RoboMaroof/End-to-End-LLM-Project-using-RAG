from fastapi import FastAPI, Request
import uvicorn
from app.routers import ingestion, search
from app.services.db_init import initialize_db
import logging
from starlette.middleware.base import BaseHTTPMiddleware
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Received request: {request.method} {request.url}")
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request processed in {process_time:.2f} seconds")
        return response

app = FastAPI()
app.add_middleware(LoggingMiddleware)

app.include_router(ingestion.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    logger.info("Starting up...")
    initialize_db()

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down...")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# React alternate, terraform, poetry, frontend backend database all options, langchain