import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import json
import numpy as np
from genre_detector import GenreDetector
from helper import get_genre_distribution_over_time
# allow YouTube download if necessary lybraries are present
import imp
try:
    imp.find_module('pafy')
    imp.find_module('youtube_dl')
    allow_yt = True
except ImportError:
    allow_yt = False
if allow_yt:
    import pafy

UPLOADS_PATH = 'uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'webm', 'ogg'])
MODEL_PATH = 'models/crnn_model.yaml'
WEIGHTS_PATH = 'models/crnn_weights.h5'

app = Flask(__name__, static_folder='assets')

if not os.path.exists(UPLOADS_PATH):
    os.makedirs(UPLOADS_PATH)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predictions_to_json(filename):
    path = os.path.join(UPLOADS_PATH, filename)
    genre_detector = GenreDetector(MODEL_PATH, WEIGHTS_PATH)
    predictions, duration = genre_detector.detect_realtime(path)
    merged_predictions = genre_detector.detect_merged()
    genre_distributions = get_genre_distribution_over_time(
        predictions, duration, merged_predictions)
    json_path = os.path.join(UPLOADS_PATH, filename + '.json')
    with open(json_path, 'w') as f:
        json_data = json.dumps(genre_distributions)
        f.write(json_data)

    return json_data


def download_yt_audio(url):
    video = pafy.new(url)
    title = secure_filename(video.title)
    bestaudio = video.getbestaudio(preftype='webm')
    filename = title + '.' + bestaudio.extension
    path = os.path.join(UPLOADS_PATH, filename)
    bestaudio.download(filepath=path)

    json_data = predictions_to_json(filename)

    return filename, json_data


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', allow_yt = allow_yt)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if not allowed_file(uploaded_file.filename):
        return 'Unsupported media type', 415

    try:
        filename = secure_filename(uploaded_file.filename)
        path = os.path.join(UPLOADS_PATH, filename)
        uploaded_file.save(path)
        json_data = predictions_to_json(filename)
    except:
        return 'Internal server error', 500

    return redirect(url_for('play',
                            filename=filename,
                            json_data=json_data))


if allow_yt:
    @app.route('/yt_download', methods=['POST'])
    def yt_download():
        url = request.form.get('youtube_url')

        try:
            filename, json_data = download_yt_audio(url)
        except:
            return 'Internal server error', 500

        return redirect(url_for('play',
                                filename=filename,
                                json_data=json_data))


@app.route('/play', methods=['GET'])
def play():
    data = {
        'filename': request.args.get('filename'),
        'json_data': request.args.get('json_data')
    }
    return jsonify(data)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_PATH,
                               filename)


@app.errorhandler(404)
def page_not_fount(e):
    return render_template('page_not_found.html')


@app.route('/error')
def internal_server_error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
