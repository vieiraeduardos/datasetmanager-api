import os
from flask import Flask, request, redirect, escape, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import numpy as np
import bcrypt
import io
import csv
from app.Connection import updateAnnotations, getAnnotationsByPerson, getAllPersons, insert_person, get_persons, get_videos, get_annotations_by_video, update_actor, get_actor, get_all_annotations, delete_image, update_image

from app.models.ScenesModel import ScenesModel

from app.Clusterizacao import Clusterizacao
from app.controllers.VideosController import VideosController

from app import app

UPLOAD_FOLDER = 'app/static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/videos/example/", methods=["GET"])
def return_video_example():
    path = "static/profile_photos/nba.mp4"
    return send_file(path, attachment_filename="video.mp4")


@app.route('/api/v2/videos/', methods=['POST'])
def api_get_file():
    file = request.files['file']
    tags = request.form.get("tags")

    if file.filename == '':
        return 'Selecione um arquivo com nome.'

    if file:
        filename = secure_filename(file.filename)

        hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "").replace(".", "")

        os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

        PATH_TO_VIDEO = os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.mp4')

        file.save(PATH_TO_VIDEO)

        Clusterizacao().processing_video(filename, PATH_TO_VIDEO)

        return "OK"
    else:
        return 'Selecione um arquivo.'



@app.route('/api/videos/', methods=["GET"])
def api_get_videos():
    result = get_videos()

    return jsonify(result)

# separa video em trechos
@app.route("/api/videos/scenes/", methods=["POST"])
def api_videos_to_scenes():
    video = request.files['file']

    if video:
        filename = secure_filename(video.filename)

        hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "").replace(".", "")

        os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

        PATH_TO_VIDEO = os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.mp4')

        video.save(PATH_TO_VIDEO)

        controller = VideosController(file_path=PATH_TO_VIDEO)

        controller.video_to_scenes()

        return "OK"
    else:
        return 'Selecione um arquivo.'


# adiciona descrição a trecho de vídeo
@app.route("/api/videos/<int:video>/scenes/", methods=["POST"])
def api_add_description_to_scenes(video):
    description = request.form.get("description")
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")

    sm = ScenesModel(
            videosCode=video, 
            description=description, 
            startTime=startTime,
            endTime=endTime)

    scene_code = sm.createDescription()

    print(scene_code)

    return jsonify({"scene_code": scene_code})


# exporta descrições de trechos do vídeo
@app.route("/api/videos/<int:video>/scenes/", methods=["GET"])
def api_get_all_scenes_by_video(video):
    sm = ScenesModel(videosCode=video)

    scenes = sm.getAllScenesByVideo()

    return jsonify(scenes)


# apaga descrição a trecho de vídeo
@app.route("/api/scenes/<int:code>", methods=["DELETE"])
def api_delete_scene_by_code(code):
    sm = ScenesModel()

    sm.deleteSceneByCode(code)

    return "OK"

