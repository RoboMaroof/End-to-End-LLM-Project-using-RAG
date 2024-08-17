from transformers import pipeline, AutoTokenizer, AutoModel

class Summarizer:
    def __init__(self):
        self.max_input_length = 512
        self.summarizer_model = "Falconsai/text_summarization"
        self.embed_model= "intfloat/multilingual-e5-base"
        # Explicitly specify the model name for summarization
        print("<<<<<<<<<<<<<<< SUMMARIZER INIT >>>>>>>>>>>>>>>>>>>")

        self.summarizer = pipeline("summarization", model=self.summarizer_model)
        print("<<<<<<<<<<<<<<< SUMMARIZER PIPELINE >>>>>>>>>>>>>>>>>>>")
        # Explicitly specify the model name for embeddings
        self.tokenizer = AutoTokenizer.from_pretrained(self.embed_model)
        self.model = AutoModel.from_pretrained(self.embed_model)
        print("<<<<<<<<<<<<<<< SUMMARIZER MODEL >>>>>>>>>>>>>>>>>>>")

    def chunk_text(self, text, max_length=512):
        """
        Splits the input text into chunks that the model can handle.
        """
        print("<<<<<<<<<<<<<<< CHUNKING >>>>>>>>>>>>>>>>>>>")
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(current_chunk) + len(word) + 1 > max_length:
                chunks.append(" ".join(current_chunk))
                print("Chunk size:", len(current_chunk))
                current_chunk = []
            current_chunk.append(word)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        print("<<<<<<<<<<<<<<< CHUNKING DONE >>>>>>>>>>>>>>>>>>>")
        return chunks

    def summarize_chunks(self, chunks):
        """
        Summarizes each chunk and combines the summaries into a final summary.
        """
        summaries = []
        for chunk in chunks:
            summary = self.summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        return " ".join(summaries)

    def summarize(self, chunks) -> str:
        print("<<<<<<<<<<<<<<< SUMMARIZER SUMMARIZE >>>>>>>>>>>>>>>>>>>")
        print("Number of chunks:", len(chunks))
        summary = self.summarize_chunks(chunks)
        print("Summary length:", len(summary))
        print("Summary:", summary)
        print("<<<<<<<<<<<<<<< SUMMARIZER SUMMARY >>>>>>>>>>>>>>>>>>>")
        return summary

    def embed(self, chunks):
        print("<<<<<<<<<<<<<<< IN EMBED >>>>>>>>>>>>>>>>>>>")
        embeddings = []
        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors='pt', truncation=True, padding=True)
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1)
            embeddings.append(embedding)
        print("<<<<<<<<<<<<<<< EMBED DONE >>>>>>>>>>>>>>>>>>>")
        return embeddings

    """
    def embed(self, text: str):
        print("<<<<<<<<<<<<<<< SUMMARIZER EMBED >>>>>>>>>>>>>>>>>>>")
        inputs = self.tokenizer(text, return_tensors='pt')
        print("<<<<<<<<<<<<<<< SUMMARIZER INPUTS >>>>>>>>>>>>>>>>>>>")
        outputs = self.model(**inputs)
        print("<<<<<<<<<<<<<<< SUMMARIZER OUTPUTS >>>>>>>>>>>>>>>>>>>")
        embedding = outputs.last_hidden_state.mean(dim=1)
        print("<<<<<<<<<<<<<<< SUMMARIZER EMBEDDING >>>>>>>>>>>>>>>>>>>")
        return embedding.detach().numpy()
    """