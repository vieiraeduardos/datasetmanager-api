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

#server
import os
from flask import Flask, request, redirect, escape, send_file
from werkzeug.utils import secure_filename

import bcrypt

from shutil import make_archive


from yolov3_deepsort import VideoTracker


app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_args(video_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--VIDEO_PATH", type=str, default=video_path)
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
def upload_file():
    file = request.files['file']
   
    if file.filename == '':
        return 'Selecione um arquivo com nome.'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        hash_filename = bcrypt.hashpw(filename.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8').replace("/", "").replace(".", "")

        os.mkdir(app.config['UPLOAD_FOLDER'] + hash_filename)

        PATH_TO_VIDEO = os.path.join(app.config['UPLOAD_FOLDER'], hash_filename + '/' + hash_filename + '.mp4')

        file.save(PATH_TO_VIDEO)

        args = parse_args(PATH_TO_VIDEO)
        cfg = get_config()
        cfg.merge_from_file(args.config_detection)
        cfg.merge_from_file(args.config_deepsort)

        with VideoTracker(cfg, args) as vdo_trk:
            vdo_trk.run()

        make_archive('annotations', 'zip', app.config['UPLOAD_FOLDER'] + hash_filename)

        return send_file('annotations.zip', attachment_filename='annotations.zip')
    else:
        return 'Selecione um arquivo com extensão MP4.'

if __name__== "__main__":
    app.run(debug=True)