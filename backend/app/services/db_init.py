import sqlite3
import os

DATABASE_URL = os.getenv("DATABASE_URL", "vector_db.sqlite")

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
