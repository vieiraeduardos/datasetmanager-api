
import os
from flask import Flask, request, redirect, escape
from werkzeug.utils import secure_filename

import bcrypt

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/video', methods=['POST'])
def upload_file():
    file = request.files['file']
   
    if file.filename == '':
        return 'Selecione um arquivo com nome.'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "")

        os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.mp4'))

        return hash_filename
    else:
        return 'Selecione um arquivo com extensão MP4.'

app.run(debug=True)
