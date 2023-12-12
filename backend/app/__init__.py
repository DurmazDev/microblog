from flask import Flask
from flask_restful import Api
from app.config import Config

from app.resources.root import RootResource

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

api.add_resource(RootResource, "/")
