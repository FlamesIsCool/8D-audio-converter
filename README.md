# 8D-audio-converter
Simple Flask based API and frontend for converting audio files to a basic
"8D" effect using SoX. The app accepts an uploaded audio file and returns the
processed result.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

The service listens on port `10000`.

## Docker

You can also build the image locally or deploy it to platforms such as
Render using the provided `Dockerfile` and `render.yaml`.

```bash
docker build -t 8d-audio .
docker run -p 10000:10000 8d-audio
```
