from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/api/v1')

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    files = {'file': (file.filename, file.read(), file.content_type)}
    response = requests.post(f"{BACKEND_URL}/ingest", files=files)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = requests.get(f"{BACKEND_URL}/search", params={'query': query})

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
