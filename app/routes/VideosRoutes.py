import os
from flask import Flask, request, redirect, escape, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import numpy as np
import bcrypt
import io
import csv
from app.Connection import updateAnnotations, getAnnotationsByPerson, getAllPersons, insert_person, get_persons, get_videos, get_annotations_by_video, update_actor, get_actor, get_all_annotations, delete_image, update_image

from flask_cors import CORS

from app.Clusterizacao import Clusterizacao
from app.controllers.FileController import FileControler

from app import app

UPLOAD_FOLDER = 'static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/v2/videos/', methods=['POST'])
def api_get_file():
    file = request.files['file']
    tags = request.form.get("tags")

    if file.filename == '':
        return 'Selecione um arquivo com nome.'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "").replace(".", "")

        os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

        PATH_TO_VIDEO = os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.mp4')

        file.save(PATH_TO_VIDEO)

        Clusterizacao().processing_video(filename, PATH_TO_VIDEO)

        return "OK"
    else:
        return 'Selecione um arquivo com extensão MP4.'



@app.route('/api/videos/', methods=["GET"])
def api_get_videos():
    result = get_videos()

    return jsonify(result)
