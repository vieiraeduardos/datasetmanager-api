import os
from flask import Flask, request, redirect, escape, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import numpy as np
import bcrypt
import io
import csv
from Connection import updateAnnotations, getAnnotationsByPerson, getAllPersons, insert_person, get_persons, get_videos, get_annotations_by_video, update_actor, get_actor, get_all_annotations, delete_image, update_image

from flask_cors import CORS

from Clusterizacao import Clusterizacao
from controllers.FileController import FileControler

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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

@app.route('/api/clusterizar/', methods=['POST'])
def api_clusterizar():
    Clusterizacao().clusterizar()

    return "OK"

@app.route("/api/persons/", methods=["POST"])
def api_create_persons():
    name = request.form.get("name")
    email = request.form.get("email")
    actor = request.form.get("actor")

    insert_person(name, email, actor)

    return "User {} ({}) was created successfully!".format(name, email)

@app.route("/api/persons/<string:name>/", methods=["GET"])
def search(name):
    persons = get_persons(name)

    return jsonify(persons)

@app.route('/api/image/')
def get_image():
    path = "static/$2b$14$1E3be8L0k3WaP22jhMy6reFBRYE66wD4n7I2aSmig4VI8Plv13qS/19/200.jpg"
    #path = request.form.get("path")
    
    return send_file(path, attachment_filename="image.jpg")


@app.route('/api/image/', methods=["POST"])
def get_post_image():
    path = request.form.get("path")
    
    return send_file(path, attachment_filename="image.jpg")

@app.route('/api/videos/', methods=["GET"])
def api_get_videos():
    result = get_videos()

    return jsonify(result)

@app.route('/api/annotations', methods=["POST"])
def api_get_annotations():

    video = request.form.get("video")
    
    annotations = get_annotations_by_video(video)

    print(annotations)

    return jsonify(annotations)


@app.route('/api/persons/<int:person_code>/annotations/', methods=["GET"])
def api_get_annotations_by_person(person_code):
    annotations = getAnnotationsByPerson(person_code)

    return jsonify(annotations)

@app.route('/api/annotations/', methods=["PUT"])
def api_update_annotations():
    wrongAnnotations = request.form.getlist('wrongAnnotations[]')

    wrongAnnotations = str(wrongAnnotations[0]).split(",")
    print(wrongAnnotations)
    n = len(wrongAnnotations)

    for i in range(n):
        print(wrongAnnotations[i])
        updateAnnotations(wrongAnnotations[i])

    return "OK"

@app.route('/api/clusters/annotations', methods=["POST"])
def api_get_annotations2():    
    annotations = get_all_annotations()

    return jsonify(annotations)

@app.route('/api/persons/', methods=["GET"])
def api_get_persons():    
    persons = getAllPersons()

    return jsonify(persons)

@app.route('/api/actors/', methods=["PUT"])
def api_update_actor():
    person = request.form.get("option")
    actor = request.form.get("actor")

    update_actor(actor, person)

    return "OK"

@app.route('/api/actors/<int:code>', methods=["GET"])
def api_get_name_actor(code):
    actor = get_actor(code)

    return jsonify(actor)

@app.route('/api/images/<int:code>', methods=["DELETE"])
def api_delete_image(code):
    delete_image(code)

    return "OK"

@app.route('/api/images/', methods=["PUT"])
def api_update_image():
    person = request.form.get("person")
    image = request.form.get("image")

    update_image(image, person)

    return "OK"

if __name__== "__main__":
    app.run(debug=True)
