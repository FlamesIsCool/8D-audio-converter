FROM python:3.11-slim

# Install SoX
RUN apt-get update && apt-get install -y sox && apt-get clean

# Create app directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 10000

# Start Flask server
CMD ["python", "app.py"]
