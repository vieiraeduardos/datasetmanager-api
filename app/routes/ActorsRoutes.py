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


from app.models.ActorsModel import ActorsModel

from app import app

@app.route('/api/actors/', methods=["PUT"])
def api_update_actor():
    person = request.form.get("option")
    actor = request.form.get("actor")

    am = ActorsModel(code=actor, Persons_code=person)

    am.update()
    
    #update_actor(actor, person)

    return "OK"

@app.route('/api/actors/<int:code>', methods=["GET"])
def api_get_name_actor(code):
    am = ActorsModel()
    actor = am.getPersonByCode(code)

    return jsonify(actor)