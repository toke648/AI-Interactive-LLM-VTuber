# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app  

# Install system dependencies and clean up cache
RUN apt-get update && apt-get install -y gcc libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install the wheel package
RUN pip install --no-cache-dir wheel

# Copy requirements.txt and install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . . 

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python3", "server.py"]