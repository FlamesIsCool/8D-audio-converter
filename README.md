# 8D-audio-converter
A tool you can convert boring old music to 8D that spins around your head
Simple Flask based API and frontend for converting audio files to a basic
"8D" effect using SoX. The app accepts an uploaded audio file and returns the
processed result.

The converter relies on the `sox` command line utility. When running locally
outside of Docker make sure SoX and the optional format libraries are
installed and available on your `PATH`. On Debian/Ubuntu you can install them
with:

```bash
sudo apt-get install sox libsox-fmt-all
```

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

The service listens on port `10000`.

## Docker

You can also build the image locally or deploy it to platforms such as
Render using the provided `Dockerfile` and `render.yaml`.

When deploying on Render make sure to choose the **Docker** environment so that
SoX is installed as part of the container build. Using the "Python" environment
will not include the required system packages.

```bash
docker build -t 8d-audio .
docker run -p 10000:10000 8d-audio
```
