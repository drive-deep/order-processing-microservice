# Use Python 3.11 as base image
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /backend

# Set PYTHONPATH so Python can find the backend module
ENV PYTHONPATH=/backend

# Install necessary system dependencies
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first (improves caching)
COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /backend/
RUN chmod +x /backend/wait_for_services.sh

# Expose the port the application runs on
EXPOSE 8000

# Run the application (Ensure 'backend.main' is correct)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
