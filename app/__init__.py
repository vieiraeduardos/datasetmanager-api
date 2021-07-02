from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app.routes import VideosRoutes
from app.routes import ImagesRoutes
from app.routes import PersonsRoutes
from app.routes import ActorsRoutes
from app.routes import FacesRoutes