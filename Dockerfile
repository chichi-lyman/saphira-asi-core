FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

# Expose port if needed
EXPOSE 8000

# Default command
CMD ["python", "-m", "pip", "list"]