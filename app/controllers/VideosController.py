from app.Connection import createPerson, getAllPersons, get_last_id, insert_video, insert_annotation, get_all_annotations, get_all_videos

class VideosController():
    def __init__(self, filename="video.mp4", file_path=""):
        self.file_path = file_path

    def save(self):
        video_code = insert_video(filename=filename, path=video_path, duration=0, tags="")

        