from flask import Flask
from flask_restful import Api
from mongoengine import connect
from marshmallow import ValidationError
from app.config import Config, LOGGING_CONFIG
from logging.config import dictConfig

from app.resources.root import RootResource
from app.resources.user import UserResource
from app.resources.post import PostResource
from app.resources.feed import FeedResource
from app.resources.comment import CommentResource
from app.resources.auth import LoginView, RegisterView

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
dictConfig(LOGGING_CONFIG)

connect(host=Config.MONGODB_SETTINGS["host"])


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    # return {"error": "Unallowed attribute."}, 400
    return {"error": "Validation error", "error_code": 1002}, 400


@app.errorhandler(KeyError)
def handle_key_error(error):
    app.logger.error(error)
    return {"error": "An error occurred.", "error_code": 1001}, 500


# TODO(ahmet): Add rate limiting.

api.add_resource(RootResource, "/")
api.add_resource(UserResource, "/user", "/user/<string:id>")
api.add_resource(PostResource, "/post", "/post/<string:id>")
api.add_resource(CommentResource, "/comment")
api.add_resource(FeedResource, "/feed")
app.add_url_rule("/auth/login", "login", LoginView, methods=["POST"])
app.add_url_rule("/auth/register", "register", RegisterView, methods=["POST"])
