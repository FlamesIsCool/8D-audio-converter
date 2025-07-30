from flask import Flask, request, send_file, render_template
import os, tempfile, subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # this shows your HTML

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    audio_file = request.files['file']
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'input.wav')
        output_path = os.path.join(tmpdir, 'output_8d.wav')
        audio_file.save(input_path)

        cmd = [
            'sox', input_path, output_path,
            'remix', '1,2',
            'reverb', '50', '50', '100', '50', '0', '100',
            'synth', '0.08', 'sine', 'amod', '0.85', 'rate', '44100',
            'gain', '-n'
        ]

        subprocess.run(cmd, check=True)
        return send_file(output_path, as_attachment=True, download_name='8d_audio.wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
