from app.Connection import createPerson, getAllPersons, insert_actor, get_last_id, insert_video, insert_annotation, get_all_annotations, get_all_videos, update_actor

class VideosController():
    def __init__(self, filename="video.mp4", file_path=""):
        self.file_path = file_path

    def save(self):
        video_code = insert_video(filename=filename, path=video_path, duration=0, tags="")

        