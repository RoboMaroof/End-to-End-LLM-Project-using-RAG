# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install curl for network debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
