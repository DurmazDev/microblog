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
from app.config import Config
from datetime import timedelta
import redis
import logging

from app.resources.root import RootResource
from app.resources.user import UserResource
from app.resources.post import PostResource, ShowPostResource
from app.resources.feed import FeedResource
from app.resources.vote import VoteResource
from app.resources.comment import CommentResource
from app.resources.auth import LoginView, RegisterView, LogOutView, RefreshView

logging.basicConfig(filename="app/log/flask-debug.log", level=logging.DEBUG)
app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
app.config["REDIS_TOKEN_EXPIRES"] = timedelta(days=1)

CORS(app=app)

app.config["jwt_redis_blocklist"] = redis.StrictRedis(
    host=Config.REDIS_SETTINGS["host"],
    port=Config.REDIS_SETTINGS["port"],
    db=Config.REDIS_SETTINGS["db"],
    decode_responses=True,
)

connect(host=Config.MONGODB_SETTINGS["host"])


@app.errorhandler(MMW_ValidationError)  # Marshmallow Validation Error
def handle_validation_error(error):
    app.logger.error(error)
    return {"error": "Validation error"}, 400


@app.errorhandler(ME_ValidationError)  # MongoEngine Validation Error
def handle_validation_error(error):
    app.logger.error(error)
    return {"error": "Unsupported ID value."}, 400


@app.errorhandler(NotUniqueError)
def handle_notunique_error(error):
    app.logger.error(error)
    return {"error": "Bad request."}, 400


@app.errorhandler(DoesNotExist)
def handle_doesnotexists_error(error):
    app.logger.error(error)
    return {"error": "Not found."}, 404


@app.errorhandler(KeyError)
def handle_key_error(error):
    app.logger.error(error)
    return {"error": "An error occurred."}, 500


@app.errorhandler(404)
def handle_not_found_error(error):
    app.logger.error(error)
    return {"error": "Not found."}, 404


@app.errorhandler(Exception)
def handle_other_errors(error):
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
app.add_url_rule("/auth/logout", "logout", LogOutView, methods=["DELETE"])
app.add_url_rule("/auth/refresh", "refresh", RefreshView, methods=["POST"])
