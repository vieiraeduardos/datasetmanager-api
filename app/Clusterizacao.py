import sys
import numpy as np
import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt

from app.faces_clustering import get_files_folder, FeatureExtractor
from tqdm import tqdm
from app.faces_clustering import silhuoette
import keras.backend.tensorflow_backend as tb

from app.Connection import createPerson, getAllPersons, get_last_id, insert_video, insert_annotation, get_all_annotations, get_all_videos

from app.models.ActorsModel import ActorsModel

class Clusterizacao:

    def processing_video(self, filename, video_path):
        tb._SYMBOLIC_SCOPE.value = True

        dir_path = video_path.split('.')[0]

        video_code = insert_video(filename=filename, path=video_path, duration=0, tags="")
        
        #extract video frames
        cap=cv2.VideoCapture(video_path)
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))

        if os.path.isdir(dir_path):
            os.rmdir(dir_path)
        os.mkdir(dir_path)

        i=1
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            if i%fps == 0:
                path = "{}\\imagem{}.jpg".format(dir_path, i)
                cv2.imwrite(path, frame)
            i+=1

        #Get urls
        extractor = FeatureExtractor('senet50')
        frames_url = get_files_folder(dir_path)

        faces_dict = {}
        for url in tqdm(frames_url):
            faces_dict[url] = extractor.get_embeddings(url)

        all_urls = []
        all_faces = []
        all_embs = []
        all_bounds = []
        for url in frames_url:
            embs, faces, bounds = faces_dict[url]
            for emb, face, bound in zip(embs, faces,bounds):
                all_urls.append(url)
                all_faces.append(face)
                all_embs.append(emb)
                all_bounds.append(bound)

        dt_sw = pd.DataFrame(all_urls, columns=['urls'])
        dt_sw['embeddings'] = all_embs
        dt_sw['faces'] = all_faces
        dt_sw['bounds'] = all_bounds

        dt_sw.to_pickle('{}.pkl'.format(video_path))

        #clustering
        dt_sw = pd.read_pickle('{}.pkl'.format(video_path))

        valid = dt_sw.embeddings.apply(lambda x: str(x) != '-')
        dt_sw = dt_sw.loc[valid]

        embs = [list(emb) for emb in dt_sw.embeddings.values]

        clusters_silhouette = silhuoette(embs,alg = "agglomerative")

        alg = 'agglomerative'
        clusters = dt_sw.copy()
        clusters['cluster_{}'.format(alg)] = clusters_silhouette

        num = self.get_number_clusters(clusters)

        actors = []
        for i in range(num):
            am = ActorsModel()
            am.create()
            #insert_actor()
            last_id = get_last_id()

            actors.append(last_id)

        tmp = np.array(clusters[['urls', 'cluster_agglomerative']])

        for i in range(len(tmp)):
            url = tmp[i][0]
            identity = tmp[i][1]

            vetor = url.split("/")

            new_path = vetor[1] + "/" + vetor[2] + "/" + vetor[3]

            insert_annotation(video_code, actors[identity], 0, 0, 0, 0, 0, new_path)

        if getAllPersons():
            self.clusterizar()
        else:
            vetor = tmp[0][0].split("/")

            new_path = vetor[1] + "/" + vetor[2] + "/" + vetor[3]
            persons_code = createPerson(name="Fulano", email="fulano@example.com", profile_photo=new_path)

            for code in actors:
                am = ActorsModel(code=code, Persons_code=persons_code)
                am.update()


    def get_number_clusters(self, clusters):
        num = []

        for item in clusters['cluster_agglomerative']:
            if not item in num:
                num.append(item)

        return len(num)

    def get_maximo(self, clusters):
        num = 0

        for item in clusters['cluster_agglomerative']:
            if item > num:
                num = item

        return num

    def clusterizar(self):
        tb._SYMBOLIC_SCOPE.value = True
        all_urls = []
        all_faces = []
        all_embs = []
        all_bounds = []
        faces_dict = {}
        frames_url = []

        annotations = get_all_annotations()

        for annotation in annotations:
            frames_url.append("app/" + annotation[1])

        # Getting URLs
        extractor = FeatureExtractor('senet50')

        for url in tqdm(frames_url):
            faces_dict[url] = extractor.get_embeddings(url)

        for url in frames_url:
            embs, faces, bounds = faces_dict[url]
            for emb, face, bound in zip(embs, faces,bounds):
                all_urls.append(url)
                all_faces.append(face)
                all_embs.append(emb)
                all_bounds.append(bound)

        dt_sw = pd.DataFrame(all_urls, columns=['urls'])
        dt_sw['embeddings'] = all_embs
        dt_sw['faces'] = all_faces
        dt_sw['bounds'] = all_bounds

        dt_sw.to_pickle('{}.pkl'.format("annotations"))

        #clustering
        dt_sw = pd.read_pickle('{}.pkl'.format("annotations"))

        valid = dt_sw.embeddings.apply(lambda x: str(x) != '-')
        dt_sw = dt_sw.loc[valid]

        embs = [list(emb) for emb in dt_sw.embeddings.values]

        clusters_silhouette = silhuoette(embs,alg = "agglomerative")

        alg = 'agglomerative'
        clusters = dt_sw.copy()
        clusters['cluster_{}'.format(alg)] = clusters_silhouette

        print(clusters[['cluster_agglomerative']])

        print("---------")

        tmp = np.array(clusters[['cluster_agglomerative']])

        for i in range(len(annotations)):
            actor = annotations[i][4]
            person_code = annotations[i][3]

            if person_code == None:
                person = self.get_name(tmp[i], annotations[i], annotations, tmp)
                
                if(person != None):
                    print("Actor = {} e Person = {}".format(actor, person))
                    am = ActorsModel(code=actor, Persons_code=person)

                    am.update()
                    #update(actor, person)

    def get_name(self, target, annotation, annotations, clusters):

        for i in range(len(annotations)):
            if clusters[i] == target and annotations[i][3] != None:
                return annotations[i][3]

        return None