import os
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

from Connection import insert_actor, get_last_id, insert_video, insert_annotation

ids_in_memory = []
map_to_dataset = []

class VideoTracker(object):
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args
        use_cuda = False
        #use_cuda = args.use_cuda and torch.cuda.is_available()
        #if not use_cuda:
        #    raise UserWarning("Running in cpu mode!")

        #if args.display:
            #cv2.namedWindow("test", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("test", args.display_width, args.display_height)

        self.vdo = cv2.VideoCapture()
        self.detector = build_detector(cfg, use_cuda=use_cuda)
        self.deepsort = build_tracker(cfg, use_cuda=use_cuda)
        self.class_names = self.detector.class_names

    def __enter__(self):
        assert os.path.isfile(self.args.VIDEO_PATH), "Error: path error"
        self.vdo.open(self.args.VIDEO_PATH)
        self.im_width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if self.args.save_path:
            fourcc =  cv2.VideoWriter_fourcc(*'MJPG')
            self.writer = cv2.VideoWriter(self.args.save_path, fourcc, 20, (self.im_width,self.im_height))

        assert self.vdo.isOpened()
        return self

    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(exc_type, exc_value, exc_traceback)

    def posprocessing(self, writer, idx_frame, im, outputs, start, video_code):
        face_cascade = cv2.CascadeClassifier('demo/haarcascade_frontalface_default.xml')

        for row in outputs:
            x = row[0]
            y = row[1]
            w = row[2]
            h = row[3]
            identity = row[4]



            if(not (identity in ids_in_memory)):
                insert_actor()
                last_id = get_last_id()
                map_to_dataset.append({'ID': last_id, 'Identity': identity})
                ids_in_memory.append(identity)

            video_name = self.args.VIDEO_PATH.split("/")[-2]

            crop_image = im[int(y):int(h), int(x):int(w)]

            gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.6, 2, minSize=(20, 20))

            face = None
            for (i, j, k, l) in faces:
                face = crop_image[int(j):int(j + l), int(i):int(i + k)]

                try:
                    path = os.getcwd()
                    os.mkdir(path + "/static/{}/{}".format(video_name, map_to_dataset[identity - 1]['ID']))
                except:
                    print("")
                    
                if(face.any()):
                    path_image = "static/{}/{}/{}.jpg".format(video_name, map_to_dataset[identity - 1]['ID'], idx_frame)
                    actor_video = map_to_dataset[identity - 1]['ID']

                    # Insert annotations to database

                    insert_annotation(video_code, actor_video, x, y, w, h, idx_frame, path_image)

                    cv2.imwrite(path_image, face)

            writer.writerow({'x': x, 'y': y, 'w': w, 'h': h, 'time': idx_frame, 'code': map_to_dataset[identity - 1]['ID']})
        

    def run(self):
        idx_frame = 0
        
        path = os.getcwd()

        with open(path + '/static/{}/annotations.csv'.format(self.args.VIDEO_PATH.split("/")[-2]), 'w', newline='') as csvfile:
            fieldnames = ['x', 'y', 'w', 'h', 'time', 'code']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Insert video to database
            filename_video = self.args.VIDEO_PATH.split("/")[-2]
            path_video = self.args.VIDEO_PATH
            duration_video = 1

            video_code = insert_video(filename=filename_video, path=path_video, duration=duration_video)

            while self.vdo.grab():
                idx_frame += 1
                if idx_frame % self.args.frame_interval:
                    continue

                start = time.time()
                _, ori_im = self.vdo.retrieve()
                im = cv2.cvtColor(ori_im, cv2.COLOR_BGR2RGB)

                # do detection
                bbox_xywh, cls_conf, cls_ids = self.detector(im)
                if bbox_xywh is not None:
                    # select person class
                    mask = cls_ids==0

                    bbox_xywh = bbox_xywh[mask]
                    bbox_xywh[:,3:] *= 1.2 # bbox dilation just in case bbox too small
                    cls_conf = cls_conf[mask]

                    # do tracking
                    outputs = self.deepsort.update(bbox_xywh, cls_conf, im)

                    fps = self.vdo.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
                    frame_count = int(self.vdo.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = frame_count/fps

                    self.posprocessing(writer, idx_frame, ori_im, outputs, duration, video_code)

                    # draw boxes for visualization
                    if len(outputs) > 0:
                        bbox_xyxy = outputs[:,:4]
                        identities = outputs[:,-1]

                        ori_im = draw_boxes(ori_im, bbox_xyxy, identities)

                end = time.time()

                if self.args.save_path:
                    self.writer.write(ori_im)