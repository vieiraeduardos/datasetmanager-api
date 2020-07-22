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

@app.route('/api/clusterizar/', methods=['POST'])
def api_clusterizar():
    Clusterizacao().clusterizar()

    return "OK"

@app.route('/api/annotations', methods=["POST"])
def api_get_annotations():

    video = request.form.get("video")
    
    annotations = get_annotations_by_video(video)

    print(annotations)

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