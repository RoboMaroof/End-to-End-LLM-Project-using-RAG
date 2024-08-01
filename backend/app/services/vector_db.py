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
