from flask import Flask, request, send_file, render_template
from audiomentations import Compose, Gain, RoomSimulator, Rotate
from audiomentations import RoomSimulator, Rotate
import soundfile as sf
import numpy as np
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Define 8D-style audio effects
augment = Compose([
    Rotate(rotation_rate=0.08, p=1.0),  # Simulates 8D movement
    Gain(min_gain_db=-5.0, max_gain_db=5.0, p=1.0),
    RoomSimulator(p=1.0)  # Simulates reverb / space
])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "No file uploaded", 400

        filename = f"{uuid.uuid4().hex}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load audio
        samples, sample_rate = sf.read(filepath)

        if samples.ndim > 1:
            samples = np.mean(samples, axis=1)  # convert to mono if stereo

        # Apply 8D effects
        augmented_samples = augment(samples=samples, sample_rate=sample_rate)

        # Save result
        output_filename = f"8d_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        sf.write(output_path, augmented_samples, sample_rate)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
