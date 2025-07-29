from flask import Flask, request, render_template, send_file
from pydub import AudioSegment
import os, math, uuid, subprocess

app = Flask(__name__)

def apply_auto_pan(audio, freq=0.08, amount=0.85, step_ms=50):
    result = []
    steps = len(audio) // step_ms
    for i in range(steps):
        pan = amount * math.sin(2 * math.pi * freq * (i * step_ms / 1000))
        segment = audio[i * step_ms:(i + 1) * step_ms].pan(pan)
        result.append(segment)
    return sum(result)

def apply_reverb(input_path, output_path):
    subprocess.run([
        "sox", input_path, output_path,
        "reverb", "50", "100", "50", "0", "100", "0"
    ], check=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["audio"]
        if not file: return "No file uploaded"

        uid = str(uuid.uuid4())
        panned = f"temp/{uid}_panned.wav"
        final = f"temp/{uid}_8d.wav"

        os.makedirs("temp", exist_ok=True)
        audio = AudioSegment.from_file(file).set_channels(2)
        audio = apply_auto_pan(audio)
        audio.export(panned, format="wav")
        apply_reverb(panned, final)

        os.remove(panned)
        return send_file(final, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
