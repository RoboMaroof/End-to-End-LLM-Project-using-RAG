# Document Processing and Search Frontend

## Overview
The frontend of this application is designed to provide a user interface for document upload, search through the ingested documents using natural language queries, and display summarized results. It is built using Flask, a lightweight web framework for Python, and interacts with the backend service for document ingestion and search.

## Key Components
- Flask: The web framework used to create the frontend.
- HTML/CSS/JavaScript: The core technologies used to build the user interface.
- Docker: Used to containerize the application, making it easy to deploy.
- Requests: Library for making HTTP requests to the backend service.

## Frontend Directory Structure
- `app.py`: Entry point of the Flask application.
- `templates/`: Contains the HTML templates.
  - `index.html`: Main page of the application.
- `static/`: Contains static files (CSS and JavaScript).
  - `css/styles.css`: Styles for the application.
  - `js/scripts.js`: JavaScript for handling client-side interactions.
- `requirements.txt`: Lists the dependencies needed for the project.
- `Dockerfile`: Instructions to containerize the application.

## How It Works

### 1. Starting the Application - app.py

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
backend_url = os.getenv("BACKEND_URL", "http://backend:8000")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        response = requests.post(f"{backend_url}/api/v1/ingest", files={'file': file})
        if response.status_code == 200:
            flash('File successfully uploaded and processed')
        else:
            flash('Failed to process file')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    response = requests.get(f"{backend_url}/api/v1/search", params={'query': query})
    if response.status_code == 200:
        results = response.json()
        return render_template('index.html', results=results)
    else:
        flash('Search failed')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

- Flask initializes and sets up routes for the main page, file upload, and search.
- Routes:
  - `/`: Renders the main HTML page.
  - `/upload`: Handles file uploads and sends them to the backend for processing.
  - `/search`: Handles search queries and retrieves results from the backend.

### 2. HTML Template - templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Search</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Document Search</h1>
        <form action="{{ url_for('upload_file') }}" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
        <form action="{{ url_for('search') }}" method="get">
            <input type="text" name="query" placeholder="Search..." required>
            <button type="submit">Search</button>
        </form>
        {% if results %}
        <h2>Search Results</h2>
        <ul>
            {% for result in results %}
            <li>
                <strong>{{ result.filename }}</strong>: {{ result.summary }} (Similarity: {{ result.similarity }})
            </li>
            {% endfor %}
        </ul>
        {% endif %}
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}
    </div>
    <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
</body>
</html>
```
- Provides a form for file upload and search.
- Displays search results and flash messages.

### 3. CSS Styles - static/css/styles.css
```css
body {
    font-family: Arial, sans-serif;
}

.container {
    width: 80%;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
}

form {
    margin-bottom: 20px;
}

input[type="file"],
input[type="text"] {
    padding: 10px;
    margin-right: 10px;
}

button {
    padding: 10px 20px;
}
```
- Basic styles for the application.

### 4. JavaScript - static/js/scripts.js

The `scripts.js` file contains client-side logic for handling search requests asynchronously. Here's a breakdown of its functionality:

```javascript
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let query = document.getElementById('query').value;

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            let results = document.getElementById('results');
            results.innerHTML = '';
            data.forEach(item => {
                let li = document.createElement('li');
                li.textContent = `Filename: ${item.filename}, Summary: ${item.summary}, Similarity: ${item.similarity}`;
                results.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
});
```
1. **Event Listener**:
   - Attaches to the form with id 'searchForm'.
   - Listens for the 'submit' event.

2. **Prevent Default Behavior**:
   - `event.preventDefault()` stops the form from submitting traditionally.

3. **Query Retrieval**:
   - Extracts the search query from the input field with id 'query'.

4. **Fetch API**:
   - Uses `fetch()` to make an asynchronous GET request to the `/search` endpoint.
   - Passes the query as a URL parameter.

5. **Response Handling**:
   - Converts the response to JSON.

6. **Results Display**:
   - Clears the existing results.
   - Iterates through the returned data.
   - Creates a new list item for each result.
   - Populates each item with filename, summary, and similarity score.
   - Appends the items to the results list.

7. **Error Handling**:
   - Catches and logs any errors that occur during the fetch operation.

This script enables a smoother user experience by updating search results dynamically without reloading the entire page.

## Interaction with Backend

The frontend interacts with the backend service through the following endpoints:

### File Upload

- Route: `/upload`
- Method: POST
- Function: Sends the uploaded file to the backend's `/api/v1/ingest` endpoint for processing.
- Backend URL: Configured in the `BACKEND_URL` environment variable.

### Search Queries

- Route: `/search`
- Method: GET
- Function: Sends search queries to the backend's `/api/v1/search` endpoint and displays the results.
- Backend URL: Configured in the `BACKEND_URL` environment variable.

## Docker and Deployment

The Dockerfile and docker-compose.yml help in containerizing the application, making it easier to deploy on any environment that supports Docker.

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```
- Sets up the Python environment, installs dependencies, and runs the Flask application.

### Docker Compose Configuration

In the docker-compose.yml file, the frontend service is defined as follows:

```yaml
frontend:
  build:
    context: ./frontend
  container_name: frontend
  ports:
    - "5000:5000"
  environment:
    - BACKEND_URL=http://backend:8000
  depends_on:
    - backend
```
- `context: ./frontend`: Builds the Docker image for the frontend from the frontend directory.
- `ports: "5000:5000"`: Maps port 5000 on the host to port 5000 in the container, making the frontend accessible at http://localhost:5000.
- `environment`: Sets the BACKEND_URL environment variable, pointing to the backend service.
- `depends_on`: Ensures the frontend starts after the backend service.

## Summary

- **File Upload**: Users can upload documents through the web interface. The documents are sent to the backend for processing.
- **Document Search**: Users can search for documents using natural language queries. The queries are sent to the backend, and the results are displayed on the web interface.