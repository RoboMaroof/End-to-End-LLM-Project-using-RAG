from transformers import pipeline, AutoTokenizer, AutoModel

class Summarizer:
    def __init__(self):
        # Explicitly specify the model name for summarization
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        
        # Explicitly specify the model name for embeddings
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
