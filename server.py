import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import numpy as np
from genre_recognizer import GenreRecognizer
from dataset_config import GENRES

UPLOADS_PATH = 'uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'au'])
MODEL_PATH = 'models/crnn_model.yaml'
WEIGHTS_PATH = 'models/crnn_weights.h5'

app = Flask(__name__, static_folder='assets')

if not os.path.exists(UPLOADS_PATH):
    os.makedirs(UPLOADS_PATH)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_genre_distribution_over_time(predictions, duration, merged_predictions):
    '''
    Turns the matrix of predictions given by a model into a dict mapping
    time in the song to a music genre distribution.
    '''
    predictions = np.reshape(predictions, predictions.shape[1:])
    n_steps = predictions.shape[0]
    delta_t = duration / n_steps

    def get_genre_distribution(step):
        return {genre_name: float(predictions[step, genre_index])
                for (genre_index, genre_name) in enumerate(GENRES)}

    def get_merged_genre():
        print(merged_predictions)
        print(merged_predictions[0, 1])
        return {genre_name: float(merged_predictions[0, genre_index])
                for (genre_index, genre_name) in enumerate(GENRES)}

    return [((step + 1) * delta_t, get_genre_distribution(step))
            for step in xrange(n_steps - 2)] + [(n_steps - 1) * delta_t, get_merged_genre()]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/lyrics', methods=['GET'])
def lyrics():
    data = {'value': request.args.get('echoValue')}
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        path = os.path.join(UPLOADS_PATH, filename)
        uploaded_file.save(path)

        genre_recognizer = GenreRecognizer(MODEL_PATH, WEIGHTS_PATH)
        (predictions, duration) = genre_recognizer.recognize_realtime(path)
        merged_prediction = genre_recognizer.recognize_merged()
        genre_distributions = get_genre_distribution_over_time(
            predictions, duration, merged_prediction)
        json_path = os.path.join(UPLOADS_PATH, filename + '.json')
        with open(json_path, 'w') as f:
            f.write(json.dumps(genre_distributions))

        return redirect(url_for('play',
                                filename=filename))
    else:
        return redirect(url_for('index'))


@app.route('/play', methods=['GET'])
def play():
    return jsonify({'filename': request.args.get('filename')})

if __name__ == '__main__':
    app.run(port=8080, debug=True)
