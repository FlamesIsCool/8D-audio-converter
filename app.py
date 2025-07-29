from flask import Flask, request, send_file, render_template
import os, uuid, soundfile as sf
import numpy as np
from audiomentations import Compose, Gain, Shift, PitchShift, HighPassFilter

app = Flask(__name__)
os.makedirs("temp", exist_ok=True)

AUG = Compose([
    PitchShift(min_semitones=-0.5, max_semitones=0.5, p=0.8),
    HighPassFilter(min_cutoff_freq=1000.0, max_cutoff_freq=3000.0, p=0.6),
    Gain(min_gain_in_db=-5.0, max_gain_in_db=5.0, p=1.0),
    Shift(min_fraction=-0.1, max_fraction=0.1, p=0.9),
])

def apply_8d_effect(input_path, output_path):
    audio, sr = sf.read(input_path)
    if audio.ndim == 1:
        audio = np.stack([audio, audio], axis=0).T
    elif audio.shape[1] == 1:
        audio = np.concatenate([audio, audio], axis=1)

    pan = np.linspace(-1, 1, audio.shape[0])
    audio[:, 0] *= (1 - pan) / 2
    audio[:, 1] *= (1 + pan) / 2

    processed = AUG(samples=audio, sample_rate=sr)
    sf.write(output_path, processed, sr)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["audio"]
        if not file:
            return "No file uploaded", 400

        uid = str(uuid.uuid4())
        input_path = f"temp/{uid}_input.wav"
        output_path = f"temp/{uid}_output.wav"
        file.save(input_path)

        apply_8d_effect(input_path, output_path)
        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
