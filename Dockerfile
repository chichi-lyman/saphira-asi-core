# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Install system dependencies that might be needed for AI/audio modules
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# 5. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of Saphira's application code into the container
COPY . .

# 7. Run the main script when the container launches
CMD ["python", "main.py"]
