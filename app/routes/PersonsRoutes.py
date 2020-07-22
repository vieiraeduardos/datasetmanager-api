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


@app.route('/api/persons/<int:person_code>/annotations/', methods=["GET"])
def api_get_annotations_by_person(person_code):
    annotations = getAnnotationsByPerson(person_code)

    return jsonify(annotations)


@app.route('/api/persons/', methods=["GET"])
def api_get_persons():    
    persons = getAllPersons()

    return jsonify(persons)