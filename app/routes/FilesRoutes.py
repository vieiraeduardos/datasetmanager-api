import os
from flask import Flask, request, redirect, escape, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import numpy as np
import bcrypt
import io
import csv
from app.Connection import updateAnnotations, getAnnotationsByPerson, getAllPersons, insert_person, get_persons, get_videos, get_annotations_by_video, get_all_annotations, delete_image, update_image

from app.Clusterizacao import Clusterizacao
from app.controllers.FileController import FileControler

from app import app

UPLOAD_FOLDER = 'app/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/reports/csv')
def download_report():
    result = get_all_annotations()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ['Annotations_code, path, name, Persons_code, Actors_code, isRight']
    writer.writerow(line)

    for row in result:
        line = [str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5])]
        writer.writerow(line)

    output.seek(0)

    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})

@app.route("/api/imports/", methods=["POST"])
def api_upload_pkl():
    file = request.files['file']
    
    filename = secure_filename(file.filename)
    
    hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "").replace(".", "")

    os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

    PATH_TO_PKL = os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.pkl')

    file.save(PATH_TO_PKL)

    fileController = FileControler(file_path=PATH_TO_PKL)

    if fileController.handleFile():
        return "OK"
