# Dockerfile for SummaBrowser Backend - Render Compatible
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY summary/requirements-ocr.txt requirements.txt

# Install Python dependencies only (no system packages)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY summary/ .

# Create necessary directories
RUN mkdir -p uploads output

# Expose port
EXPOSE 10000

# Set environment variables
ENV FLASK_APP=app-ocr.py
ENV FLASK_ENV=production
ENV PORT=10000
ENV OCR_API_KEY=helloworld

# Run the application
CMD ["python", "app-ocr.py"]
