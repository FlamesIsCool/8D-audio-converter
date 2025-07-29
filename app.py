from flask import Flask, request, render_template, send_file
import os, uuid, subprocess

app = Flask(__name__)
os.makedirs("temp", exist_ok=True)

def process_audio_ffmpeg(input_path, output_path):
    # Apply auto-pan and reverb using FFmpeg
    command = [
        "ffmpeg", "-y", "-i", input_path,
        "-af",
        "apad,pan=stereo|c0=0.5*FL+0.5*FR|c1=0.5*FL-0.5*FR,asetrate=44100*0.999,aresample=44100,aecho=0.8:0.88:60:0.4",
        output_path
    ]
    subprocess.run(command, check=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["audio"]
        if not file: return "No file uploaded"

        uid = str(uuid.uuid4())
        input_path = f"temp/{uid}_in.wav"
        output_path = f"temp/{uid}_out.wav"

        file.save(input_path)
        process_audio_ffmpeg(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
