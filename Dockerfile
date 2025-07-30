FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y sox libsox-fmt-all \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000
CMD ["python", "app.py"]
