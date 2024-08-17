import logging
from flask import Flask, request, jsonify, render_template
import requests
import os
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')

def wait_for_backend(url, retries=5, delay=5):
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(delay)
    return False

@app.route('/')
def index():
    if wait_for_backend(f"{BACKEND_URL}/health"):
        return render_template('index.html')
    else:
        return "Backend service is unavailable. Please try again later.", 503

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Upload route accessed")
    try:
        if 'file' not in request.files:
            logger.warning("No file part in request")
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            logger.warning("No selected file")
            return jsonify({"error": "No selected file"}), 400

        logger.info(f"File received: {file.filename}")
        files = {'file': (file.filename, file.read(), file.content_type)}
        logger.info(f"Sending request to backend: {BACKEND_URL}/api/v1/ingest")
        response = requests.post(f"{BACKEND_URL}/api/v1/ingest", files=files)
        logger.info(f"Backend response status: {response.status_code}")

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            logger.error(f"Backend error: {response.text}")
            return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.exception("Error in upload_file")
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    logger.info("Search route accessed")
    query = request.args.get('query')
    if not query:
        logger.warning("No query provided")
        return jsonify({"error": "No query provided"}), 400

    logger.info(f"Sending search request to backend: {BACKEND_URL}/v1/search")
    response = requests.get(f"{BACKEND_URL}/v1/search", params={'query': query})
    logger.info(f"Backend response status: {response.status_code}")

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        logger.error(f"Backend error: {response.text}")
        return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)