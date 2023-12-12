from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from mongoengine import (
    connect,
    NotUniqueError,
    ValidationError as ME_ValidationError,
    DoesNotExist,
)
from marshmallow import ValidationError as MMW_ValidationError
from app.config import Config, LOGGING_CONFIG
from logging.config import dictConfig

from app.resources.root import RootResource
from app.resources.user import UserResource
from app.resources.post import PostResource, ShowPostResource
from app.resources.feed import FeedResource
from app.resources.vote import VoteResource
from app.resources.comment import CommentResource
from app.resources.auth import LoginView, RegisterView

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

CORS(app=app)

dictConfig(LOGGING_CONFIG)
connect(host=Config.MONGODB_SETTINGS["host"])


@app.errorhandler(MMW_ValidationError)  # Marshmallow Validation Error
def handle_validation_error(error):
    # return {"error": "Unallowed attribute."}, 400
    return {"error": "Validation error"}, 400


@app.errorhandler(ME_ValidationError)  # MongoEngine Validation Error
def handle_validation_error(error):
    return {"error": "Unsupported ID value."}, 400


@app.errorhandler(NotUniqueError)
def handle_notunique_error(error):
    # TODO(ahmet): Catch keyPattern and return it.
    return {"error": "Bad request."}, 400


@app.errorhandler(DoesNotExist)
def handle_doesnotexists_error(error):
    return {"error": "Not found."}, 404


@app.errorhandler(KeyError)
def handle_key_error(error):
    app.logger.error(error)
    return {"error": "An error occurred."}, 500


# TODO(ahmet): Add rate limiting.

api.add_resource(RootResource, "/")
api.add_resource(UserResource, "/user", "/user/<string:id>")
api.add_resource(ShowPostResource, "/post/<string:id>")
api.add_resource(PostResource, "/post", "/post/<string:id>")
api.add_resource(CommentResource, "/comment", "/comment/<string:id>")
api.add_resource(VoteResource, "/vote")
api.add_resource(FeedResource, "/feed")
app.add_url_rule("/auth/login", "login", LoginView, methods=["POST"])
app.add_url_rule("/auth/register", "register", RegisterView, methods=["POST"])
