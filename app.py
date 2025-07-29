import os
import math
from flask import Flask, request, send_file, render_template
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def apply_8d_effect(audio: AudioSegment, frequency: float = 0.08) -> AudioSegment:
    segment_duration_ms = 100  # Split into chunks of 100ms
    total_segments = int(len(audio) / segment_duration_ms)
    new_audio = AudioSegment.silent(duration=0)

    for i in range(total_segments):
        start = i * segment_duration_ms
        end = start + segment_duration_ms
        chunk = audio[start:end]

        pan_amount = math.sin(2 * math.pi * frequency * i)
        chunk = chunk.pan(pan_amount)  # Pans from -1 (left) to +1 (right)

        new_audio += chunk

    return new_audio

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["audio"]
        if file.filename == "":
            return "No selected file", 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        audio = AudioSegment.from_file(filepath)
        output = apply_8d_effect(audio)

        output_path = os.path.join(OUTPUT_FOLDER, "8d_" + file.filename)
        output.export(output_path, format="mp3")

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
