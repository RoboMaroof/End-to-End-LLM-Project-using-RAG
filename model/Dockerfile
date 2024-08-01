# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app/model

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Set the PYTHONPATH environment variable to ensure the app module is found
ENV PYTHONPATH=/app

# Expose the port the model service is running on
EXPOSE 8501

# Run the model service
CMD ["python", "model_service.py"]