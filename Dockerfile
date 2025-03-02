FROM python:3.9

# Set the working directory
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]