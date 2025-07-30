from flask import Flask, request, send_file
from pydub import AudioSegment
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_8d():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'Empty filename'}, 400

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'input.wav')
        output_path = os.path.join(tmpdir, 'output.wav')
        
        # Convert to WAV (if needed)
        audio = AudioSegment.from_file(file)
        audio.export(input_path, format='wav')

        # Apply 8D effect using SoX
        # Auto panner: synth panning movement
        # Reverb: simulate room
        cmd = [
            'sox', input_path, output_path,
            'remix', '1,2',
            'reverb', '50', '50', '100', '50', '0', '100',
            'synth', '0.08', 'sine', 'amod', '0.8', 'rate', '44100',
            'gain', '-n'
        ]

        subprocess.run(cmd, check=True)

        return send_file(output_path, as_attachment=True, download_name='8d_audio.wav')

if __name__ == '__main__':
    app.run(debug=True)
