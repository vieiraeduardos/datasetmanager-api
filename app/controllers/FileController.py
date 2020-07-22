import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np

from app.Connection import getPersonCodeByName, createActor, createPerson, getVideoCodeByFilename, insert_actor, get_last_id, insert_video, insert_annotation, get_all_annotations, get_all_videos, update_actor

class FileControler():
    def __init__(self, file_path):
        self.file_path = file_path

    def saveVideos(self, videos):
        videos_name = []

        for video_path in videos:
            filename = video_path.split("/")[-1] 
            
            if not filename in videos_name:
                videos_name.append(filename)
                insert_video(filename=filename, path=video_path, duration=0, tags="")

    def savePersonsFound(self, dt_all_meta):
        ann = np.array(dt_all_meta)

        persons = []
        image_path = None
        i = 0
        for cluster in set(dt_all_meta['super_cluster']):
            dt_cluster = dt_all_meta.loc[dt_all_meta.super_cluster == cluster]
            cols = len(dt_cluster.faces_samples)

            for j, sample in enumerate(dt_cluster.faces_samples):
                image_path = "static/" + self.file_path.split("/")[-2] + "/{}-{}.jpg".format(cluster, i)

                cv2.imwrite(image_path, sample[:,:,::-1])

                if not cluster in persons:
                    persons.append(cluster)
                    createPerson(name="{}".format(cluster), profile_photo=image_path)

                videos = np.array(dt_cluster["video"])
                filename = videos[j].split("/")[-1]
                video_code = getVideoCodeByFilename(filename)
                person_code = getPersonCodeByName(cluster)

                actor_code = createActor(name="{}".format(i), email="", persons_code=person_code)
                insert_annotation(video_code, actor_code, 0, 0, 0, 0, 0, image_path)
                i = i + 1


    def handleFile(self):
        dt_all_meta = pd.read_pickle("./{}".format(self.file_path))

        self.saveVideos(dt_all_meta["video"])

        self.savePersonsFound(dt_all_meta)

        return "OK"
