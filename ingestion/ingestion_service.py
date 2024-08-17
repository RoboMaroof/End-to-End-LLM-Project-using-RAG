from backend.app.services.db_init import initialize_db
import time

if __name__ == "__main__":
    initialize_db()
    while True:
        print("Ingestion service running .....")
        time.sleep(60)