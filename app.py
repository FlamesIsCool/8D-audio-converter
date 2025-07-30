from flask import Flask, request, send_file
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    audio_file = request.files['file']
    filename = audio_file.filename

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, filename)
        output_path = os.path.join(tmpdir, 'output_8d.wav')

        # Save uploaded file
        audio_file.save(input_path)

        # Apply SoX effects for 8D simulation
        sox_cmd = [
            'sox', input_path, output_path,
            'remix', '1,2',
            'reverb', '50', '50', '100', '50', '0', '100',
            'synth', '0.08', 'sine', 'amod', '0.85', 'rate', '44100',
            'gain', '-n'
        ]

        try:
            subprocess.run(sox_cmd, check=True)
        except subprocess.CalledProcessError:
            return {'error': 'Audio processing failed'}, 500

        return send_file(output_path, as_attachment=True, download_name='8d_audio.wav')

@app.route('/')
def health():
    return '8D Audio Converter Backend Running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
