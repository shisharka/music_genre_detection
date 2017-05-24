from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__, static_folder='assets')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lyrics/', methods=['GET'])
def lyrics():
    data = {'value': request.args.get('echoValue')}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)