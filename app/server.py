import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOADS_PATH = 'uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'au'])

app = Flask(__name__, static_folder='assets')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lyrics/', methods=['GET'])
def lyrics():
    data = {'value': request.args.get('echoValue')}
    return jsonify(data)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/', methods=['POST'])
def upload_file():
    # file_info = request.files['filearg'][0]
    # file_name = file_info['filename']
    # file_extension = os.path.splitext(file_name)[1]
    # file_uuid = str(uuid.uuid4())
    # uploaded_name = file_uuid + file_extension

    # if not os.path.exists(UPLOADS_PATH):
    #     os.makedirs(UPLOADS_PATH)

    # uploaded_path = os.path.join(UPLOADS_PATH, uploaded_name)
    # with open(uploaded_path, 'w') as f:
    #     f.write(file_info['body'])
    # (predictions, duration) = genre_recognizer.recognize(
    #         uploaded_path)
    # genre_distributions = self.get_genre_distribution_over_time(
    #         predictions, duration)
    # json_path = os.path.join(UPLOADS_PATH, file_uuid + '.json')
    # with open(json_path, 'w') as f:
    #     f.write(json.dumps(genre_distributions))
    # self.finish('"{}"'.format(file_uuid))


    if not os.path.exists(UPLOADS_PATH):
        os.makedirs(UPLOADS_PATH)

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file'][0]
    # if user does not select a file, browser also
    # submits an empty part without filename
    if file['filename'] == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file['filename']):
        filename = secure_filename(file['filename'])

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w') as f:
            f.write(file['body']) 
        return redirect(url_for('uploaded_file',
                                filename=filename))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
