import cv2
import time
import argparse
import torch
import numpy as np
import csv

from detector import build_detector
from deep_sort import build_tracker
from utils.draw import draw_boxes
from utils.parser import get_config

import os
from flask import Flask, request, redirect, escape, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename

import bcrypt

from shutil import make_archive

from yolov3_deepsort import VideoTracker

from Connection import insert_person, get_persons, get_videos, get_annotations_by_video, update_actor, get_actor, get_all_annotations, delete_image, update_image

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_args(video_path, tags):
    parser = argparse.ArgumentParser()
    parser.add_argument("--VIDEO_PATH", type=str, default=video_path)
    parser.add_argument("--tags", type=str, default=tags)
    parser.add_argument("--config_detection", type=str, default="./configs/yolov3.yaml")
    parser.add_argument("--config_deepsort", type=str, default="./configs/deep_sort.yaml")
    parser.add_argument("--ignore_display", dest="display", action="store_false", default=True)
    parser.add_argument("--frame_interval", type=int, default=20)
    parser.add_argument("--display_width", type=int, default=800)
    parser.add_argument("--display_height", type=int, default=600)
    parser.add_argument("--save_path", type=str, default="./demo/demo.avi")
    parser.add_argument("--cpu", dest="use_cuda", action="store_false", default=True)
    
    return parser.parse_args()

@app.route('/api/videos', methods=['POST'])
def get_file():
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

        args = parse_args(PATH_TO_VIDEO, tags)
        cfg = get_config()
        cfg.merge_from_file(args.config_detection)
        cfg.merge_from_file(args.config_deepsort)

        with VideoTracker(cfg, args) as vdo_trk:
            vdo_trk.run()

        make_archive('annotations', 'zip', app.config['UPLOAD_FOLDER'] + hash_filename)

        return send_file('annotations.zip', attachment_filename='annotations.zip', as_attachment=True)
    else:
        return 'Selecione um arquivo com extensão MP4.'


@app.route("/api/persons/", methods=["POST"])
def create_persons():
    name = request.form.get("name")
    email = request.form.get("email")

    insert_person(name, email)

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

    return jsonify(annotations)

@app.route('/api/clusters/annotations', methods=["POST"])
def api_get_annotations2():    
    annotations = get_all_annotations()

    return jsonify(annotations)

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
