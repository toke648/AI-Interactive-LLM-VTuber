# Base image
FROM python:3.11-slim

# Set noninteractive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    portaudio19-dev \
    ffmpeg \
    libasound2-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Set working directory
WORKDIR /app

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python3", "server.py"]
