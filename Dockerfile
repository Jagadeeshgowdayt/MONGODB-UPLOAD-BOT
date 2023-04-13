# Base image
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the script
CMD ["python", "script.py"]
