from fastapi import FastAPI
from backend.app.services.summarizer import Summarizer

app = FastAPI()
summarizer = Summarizer()

@app.get("/summarize")
async def summarize(text: str):
    return {"summary": summarizer.summarize(text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
