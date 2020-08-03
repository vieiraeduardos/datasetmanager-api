import os
from flask import Flask, request, redirect, escape, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import numpy as np
import bcrypt
import io
import csv
from app.Connection import updateAnnotations, getAnnotationsByPerson, getAllPersons, insert_person, get_persons, get_videos, get_annotations_by_video, update_actor, get_actor, get_all_annotations, delete_image, update_image

from app.Clusterizacao import Clusterizacao
from app.controllers.FileController import FileControler

from app import app

UPLOAD_FOLDER = 'app/static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/image/', methods=["POST"])
def get_post_image():
    path = request.form.get("path")
    
    return send_file(path, attachment_filename="image.jpg")


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